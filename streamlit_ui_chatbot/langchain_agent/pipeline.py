import os
from datetime import datetime

import uvicorn
from fastapi import FastAPI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools.render import render_text_description
from langchain_ollama import OllamaLLM
from models.tool_request import ToolRequest
from pydantic import ValidationError
from tools import create_event, delete_event, get_event_by_date_time, get_event_by_id, get_events_by_date

llm_name = os.environ.get("LLM_NAME")
llm_url = os.environ.get("LLM_URL")

model = OllamaLLM(model=llm_name, base_url=llm_url)
tools = [create_event, get_event_by_id, get_events_by_date, get_event_by_date_time, delete_event]
rendered_tools = render_text_description(tools)

system_prompt = f""" 
    Eres un asistente conversacional cuya tarea principal es manejar una agenda de eventos
    la agenda de eventos se controla a través de un conjunto de herramientas. En caso que el usuario 
    no diga el año de busqueda, usa {datetime.now().year}.
    ## herramientas: 
    Las herramientas y su descripción son: 
    {rendered_tools}
    ## Instrucciones
    Dada la entrada de datos del usuario, retorne el nombre y los datos de entrada que la herramienta 
    va a utilizar. Tu respuesta debe ser un JSON blob con las claves 'name' y 'arguments' como llaves del diccionario
    El valor asociado a los argumentos 'arguments' debe ser un diccionario de parámetros
    """

response_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Eres un asistente conversacional. "
            "Convierte el resultado de una acción sobre una agenda de un calendario "
            "en una respuesta clara, natural y amigable para el usuario. "
            "No muestres JSON ni estructuras técnicas."
            " Haz un resumen de las estructuras recibidas para el usuario"
            "al final pregunta si el usuario necesita ayuda con algo mas de forma cordial,"
            " intenta que la pregunta tenga "
            "en cuenta una siguiente acción basada en el resultado. Al final del mensaje, dile al usuario cuál era el ID del evento encontrado, si hubo varios ids, pon en el texto cada evento como una tabla con su id , fecha, hora, y nombre",
        ),
        ("user", "Resultado de la acción: {tool_result}"),
    ]
)

prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("user", "{input}")])


def run_tool(model_output):
    tool_map = {tool.name: tool for tool in tools}
    tool = tool_map[model_output["name"]]
    return tool.invoke(model_output["arguments"])


chain = prompt | model | JsonOutputParser() | run_tool
response_chain = response_prompt | model

app = FastAPI(title="LangChain Tools API")


@app.post("/invoke")
def invoke_tool(req: ToolRequest):
    try:
        result = chain.invoke({"input": req.input})
        natural_response = response_chain.invoke({"tool_result": result})
        return {"message": natural_response}

    except ValidationError as e:
        missing = [err["loc"][-1] for err in e.errors() if err["type"] == "missing"]

        return {"message": f"Para continuar necesito: {', '.join(missing)}"}

    except Exception as e:
        return {
            "message": "Ocurrió un error interno al procesar tu solicitud.",
            "raw": str(e),
        }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
