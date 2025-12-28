# 🗓️ Asistente Conversacional para Gestión de Agenda de Eventos

## 1. Descripción General

Este proyecto implementa un **asistente conversacional de agenda** cuyo objetivo es permitir a un usuario **crear, consultar y eliminar eventos** utilizando **lenguaje natural**.

El asistente está diseñado como un **reto técnico**, priorizando simplicidad, modularidad y separación de responsabilidades, haciendo uso de **LangChain como framework principal de orquestación**, junto con **FastAPI, Streamlit y Docker Compose**.

La información de la agenda se almacena en un **archivo Excel (`.xlsx`)**, utilizado como fuente de datos persistente.

---

## 2. Objetivo del Asistente

El asistente debe permitir interactuar en lenguaje natural para realizar las siguientes operaciones:

-  **Agregar un evento**
- **Consultar eventos programados para una fecha**
- **Eliminar un evento existente**

Ejemplos de interacción:
- “Agrega una reunión mañana a las 10 AM”
- “¿Qué eventos tengo el 2025-01-10?”
- “Elimina el evento con ID 3”

---

## 3. Modelo de Datos (Agenda en Excel)

La agenda se almacena en un archivo `agenda.xlsx`, el cual funciona como una base de datos simple.

| Campo | Tipo | Descripción |
|------|------|------------|
| id_evento | int | Identificador único del evento |
| tipo_evento | char | Tipo de evento (reunión, fiesta, salida, etc.) |
| fecha_evento | YYYY-MM-DD | Fecha del evento |
| hora_evento | HH:MM | Hora del evento |
| fecha_creado | YYYY-MM-DD | Fecha de creación |
| fecha_modificado | YYYY-MM-DD | Fecha de modificación |

---

## 4. Arquitectura General

Arquitectura basada en microservicios orquestados con Docker Compose:

Usuario → Streamlit → LangChain → FastAPI → Excel
https://github.com/Robert-2533/Prueba-_tecnica_Ingeniero_IA/issues/1#issue-3765878738
---

## 5. Componentes

### Streamlit
Interfaz gráfica para el usuario.

### LangChain
Orquesta la lógica conversacional y decide qué endpoint ejecutar.

### LLM
Procesa lenguaje natural y extrae intención y entidades.

### FastAPI
Expone tres endpoints:
- Crear evento
- Consultar evento
- Eliminar evento

### Excel
Persistencia de datos.

---

## 6. Docker Compose

Todos los servicios se ejecutan en contenedores separados, facilitando despliegue y escalabilidad.

---

## 7. Flujo de Ejecución

1. Usuario escribe solicitud.
2. Streamlit envía a LangChain.
3. LangChain consulta al LLM.
4. Se ejecuta el endpoint correspondiente.
5. Se responde al usuario.

---

## 8. Ejecución
Ingresar a la carpeta streamlit_ui_chatbot allí
correr el comando:
```python
docker-compose up --build
```
