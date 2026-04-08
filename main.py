from task_manager import TaskManager
from ia_services import create_simple_tasks

def print_menu():
    print("\n-- Gestor de Tareas inteligente --")
    print("1. Añadir tarea")
    print("2. Añadir tarea con IA")
    print("3. Listar tareas")
    print("4. Completar tarea")
    print("5. Eliminar tarea")
    print("6. Salir")
def main():

    task_manager = TaskManager()

    while True:
        print_menu()

        try:

            choice = int(input("Selecciona una opción: "))

            match choice:
                case 1:
                    description = input("Descripción de la tarea: ")
                    task_manager.add_task(description)

                case 2:
                    description = input("Describe una tarea compleja: ")
                    subtasks = create_simple_tasks(description)
                    for subtask in subtasks:
                        if not subtask.startswith("Error:"):
                            task_manager.add_task(subtask)
                        else:
                            print(subtask)
                            break

                case 3:
                    task_manager.list_tasks()

                case 4: 
                    id = int(input("ID de la tarea a completar: "))
                    task_manager.complete_task(id)

                case 5: 
                    id = int(input("ID de la tarea a eliminar: "))
                    task_manager.delete_task(id)

                case 6: 
                    print("Saliendo...")
                    break
                case _: 
                    print("Opción no válida. Inténtalo de nuevo.")
                    
        except ValueError:
            print("Entrada no válida. Por favor, ingresa un número.")

if __name__ == "__main__":
    main()