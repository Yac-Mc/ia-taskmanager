# IA TaskManager 🤖✅

Gestor de tareas de línea de comandos con integración de inteligencia artificial. Permite administrar tareas del día a día y, opcionalmente, descomponer tareas complejas en subtareas simples y accionables usando la API de OpenAI.

---

## Características

- **Añadir tareas** manualmente con una descripción libre.
- **Descomponer tareas complejas con IA**: genera entre 3 y 5 subtareas accionables usando GPT-3.5-turbo.
- **Listar tareas** pendientes y completadas.
- **Completar tareas** marcándolas como realizadas.
- **Eliminar tareas** por ID.
- **Persistencia automática** en un archivo `tasks.json` local.

---

## Estructura del proyecto

```
ia-taskmanager/
├── main.py              # Punto de entrada, menú interactivo
├── task_manager.py      # Clases Task y TaskManager (lógica principal)
├── ia_services.py       # Integración con la API de OpenAI
├── test_task_manager.py # Suite de tests unitarios (38 tests)
├── tasks.json           # Persistencia de tareas (se genera automáticamente)
├── requirements.txt     # Dependencias del proyecto
└── .env                 # Variables de entorno (no incluido en el repo)
```

---

## Requisitos

- Python 3.10 o superior
- Una API Key de OpenAI (solo necesaria para la funcionalidad de IA)

---

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone https://github.com/tu-usuario/ia-taskmanager.git
   cd ia-taskmanager
   ```

2. **Crear y activar el entorno virtual**

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la API Key de OpenAI**

   Crear un archivo `.env` en la raíz del proyecto:

   ```env
   OPENAI_API_KEY=sk-...tu-clave-aqui...
   ```

---

## Uso

```bash
python main.py
```

Se mostrará el menú interactivo:

```
-- Gestor de Tareas inteligente --
1. Añadir tarea
2. Añadir tarea con IA
3. Listar tareas
4. Completar tarea
5. Eliminar tarea
6. Salir
```

### Ejemplo de flujo

```
Selecciona una opción: 2
Describe una tarea compleja: Organizar una mudanza

Tarea añadida: Hacer un inventario de todos los muebles y objetos del hogar
Tarea añadida: Contratar una empresa de mudanzas o reservar un vehículo de transporte
Tarea añadida: Embalar y etiquetar todas las cajas por habitación
Tarea añadida: Notificar el cambio de dirección a servicios y contactos
Tarea añadida: Limpiar el piso de origen antes de entregarlo
```

---

## Tests

La suite de tests cubre todas las funcionalidades principales de `task_manager.py` sin tocar el archivo `tasks.json` de producción (aislamiento total mediante mocks).

```bash
python -m pytest test_task_manager.py -v
```

### Cobertura de tests

| Clase               | Tests | Descripción                                              |
|---------------------|-------|----------------------------------------------------------|
| `TestTask`          | 4     | Inicialización y representación en string                |
| `TestAddTask`       | 6     | Añadir tareas, IDs secuenciales, persistencia            |
| `TestListTasks`     | 3     | Listado de tareas y mensajes de estado                   |
| `TestCompleteTask`  | 6     | Completar tareas, ID no encontrado                       |
| `TestDeleteTask`    | 6     | Eliminar tareas, ID no encontrado                        |
| `TestLoadTasks`     | 8     | Carga desde JSON, errores de archivo y formato           |
| `TestSaveTasks`     | 4     | Escritura correcta en JSON, errores de I/O               |
| **Total**           | **38**| ✅ 38/38 passing                                         |

---

## Dependencias principales

| Paquete        | Versión   | Uso                              |
|----------------|-----------|----------------------------------|
| `openai`       | 2.30.0    | Cliente para la API de OpenAI    |
| `python-dotenv`| 1.2.2     | Carga de variables de entorno    |
| `pytest`       | ≥ 9.0     | Framework de tests               |

---

## Licencia

MIT
