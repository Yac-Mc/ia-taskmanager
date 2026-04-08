import json
import unittest
from unittest.mock import patch, mock_open

from task_manager import Task, TaskManager


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_manager(tasks: list | None = None) -> TaskManager:
    """Return a TaskManager with simulated task data. No file is ever touched.

    Args:
        tasks: lista opcional de dicts con claves id, description, completed
               (mismo formato que tasks.json). Si se omite, comienza sin tareas.
    """
    with patch.object(TaskManager, "load_tasks", return_value=None):
        manager = TaskManager()
    if tasks:
        manager._tasks = [Task(**t) for t in tasks]
        manager._next_id = manager._tasks[-1].id + 1
    else:
        manager._tasks = []
        manager._next_id = 1
    return manager


# ─────────────────────────────────────────────────────────────────────────────
# Task
# ─────────────────────────────────────────────────────────────────────────────

class TestTask(unittest.TestCase):

    def test_init_stores_attributes(self):
        task = Task(1, "Buy milk")
        self.assertEqual(task.id, 1)
        self.assertEqual(task.description, "Buy milk")

    def test_init_default_completed_is_false(self):
        task = Task(1, "Buy milk")
        self.assertFalse(task.completed)

    def test_init_completed_true(self):
        task = Task(2, "Write report", completed=True)
        self.assertTrue(task.completed)

    def test_str_pending_task(self):
        task = Task(1, "Buy milk")
        self.assertEqual(str(task), "[ ] #1: Buy milk")

    def test_str_completed_task(self):
        task = Task(3, "Buy milk", completed=True)
        self.assertEqual(str(task), "[OK] #3: Buy milk")


# ─────────────────────────────────────────────────────────────────────────────
# TaskManager – add_task
# ─────────────────────────────────────────────────────────────────────────────

class TestAddTask(unittest.TestCase):

    def test_add_task_appends_to_list(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks"):
            manager.add_task("Do laundry")
        self.assertEqual(len(manager._tasks), 1)
        self.assertEqual(manager._tasks[0].description, "Do laundry")

    def test_add_task_assigns_sequential_ids(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks"):
            manager.add_task("First")
            manager.add_task("Second")
        self.assertEqual(manager._tasks[0].id, 1)
        self.assertEqual(manager._tasks[1].id, 2)

    def test_add_task_increments_next_id(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks"):
            manager.add_task("Task A")
            manager.add_task("Task B")
        self.assertEqual(manager._next_id, 3)

    def test_add_task_new_task_is_not_completed(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks"):
            manager.add_task("Fresh task")
        self.assertFalse(manager._tasks[0].completed)

    def test_add_task_prints_confirmation(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks"), patch("builtins.print") as mock_print:
            manager.add_task("Walk the dog")
        mock_print.assert_called_once_with("Tarea añadida: Walk the dog")

    def test_add_task_calls_save(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks") as mock_save:
            manager.add_task("Something")
        mock_save.assert_called_once()


# ─────────────────────────────────────────────────────────────────────────────
# TaskManager – list_tasks
# ─────────────────────────────────────────────────────────────────────────────

class TestListTasks(unittest.TestCase):

    def test_list_tasks_empty_prints_no_tasks_message(self):
        manager = make_manager()
        with patch("builtins.print") as mock_print:
            manager.list_tasks()
        mock_print.assert_called_once_with("No hay tareas pendientes.")

    def test_list_tasks_prints_each_task(self):
        manager = make_manager([
            {"id": 1, "description": "Alpha", "completed": False},
            {"id": 2, "description": "Beta",  "completed": False},
        ])
        with patch("builtins.print") as mock_print:
            manager.list_tasks()
        # print(task) passes the object itself; convert to str before comparing
        printed = [str(call.args[0]) for call in mock_print.call_args_list]
        self.assertIn("[ ] #1: Alpha", printed)
        self.assertIn("[ ] #2: Beta",  printed)

    def test_list_tasks_does_not_print_no_tasks_when_not_empty(self):
        manager = make_manager([{"id": 1, "description": "Something", "completed": False}])
        with patch("builtins.print") as mock_print:
            manager.list_tasks()
        printed = [call.args[0] for call in mock_print.call_args_list]
        self.assertNotIn("No hay tareas pendientes.", printed)


# ─────────────────────────────────────────────────────────────────────────────
# TaskManager – complete_task
# ─────────────────────────────────────────────────────────────────────────────

class TestCompleteTask(unittest.TestCase):

    def test_complete_task_marks_completed(self):
        manager = make_manager([{"id": 1, "description": "Read book", "completed": False}])
        with patch.object(manager, "save_tasks"):
            manager.complete_task(1)
        self.assertTrue(manager._tasks[0].completed)

    def test_complete_task_prints_confirmation(self):
        manager = make_manager([{"id": 1, "description": "Read book", "completed": False}])
        with patch.object(manager, "save_tasks"), patch("builtins.print") as mock_print:
            manager.complete_task(1)
        mock_print.assert_called_once_with("Tarea completada: Read book")

    def test_complete_task_calls_save(self):
        manager = make_manager([{"id": 1, "description": "Read book", "completed": False}])
        with patch.object(manager, "save_tasks") as mock_save:
            manager.complete_task(1)
        mock_save.assert_called_once()

    def test_complete_task_not_found_prints_message(self):
        manager = make_manager()
        with patch("builtins.print") as mock_print:
            manager.complete_task(99)
        mock_print.assert_called_once_with("No se encontró la tarea con ID 99.")

    def test_complete_task_not_found_does_not_save(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks") as mock_save:
            manager.complete_task(99)
        mock_save.assert_not_called()

    def test_complete_task_does_not_affect_other_tasks(self):
        manager = make_manager([
            {"id": 1, "description": "First",  "completed": False},
            {"id": 2, "description": "Second", "completed": False},
        ])
        with patch.object(manager, "save_tasks"):
            manager.complete_task(1)
        self.assertFalse(manager._tasks[1].completed)


# ─────────────────────────────────────────────────────────────────────────────
# TaskManager – delete_task
# ─────────────────────────────────────────────────────────────────────────────

class TestDeleteTask(unittest.TestCase):

    def test_delete_task_removes_task_from_list(self):
        manager = make_manager([
            {"id": 1, "description": "Clean house",  "completed": False},
            {"id": 2, "description": "Cook dinner", "completed": False},
        ])
        with patch.object(manager, "save_tasks"):
            manager.delete_task(1)
        self.assertEqual(len(manager._tasks), 1)
        self.assertEqual(manager._tasks[0].id, 2)

    def test_delete_task_prints_confirmation(self):
        manager = make_manager([{"id": 1, "description": "Clean house", "completed": False}])
        with patch.object(manager, "save_tasks"), patch("builtins.print") as mock_print:
            manager.delete_task(1)
        mock_print.assert_called_once_with("Tarea con ID 1 eliminada - Clean house")

    def test_delete_task_calls_save(self):
        manager = make_manager([{"id": 1, "description": "Clean house", "completed": False}])
        with patch.object(manager, "save_tasks") as mock_save:
            manager.delete_task(1)
        mock_save.assert_called_once()

    def test_delete_task_not_found_prints_message(self):
        manager = make_manager()
        with patch("builtins.print") as mock_print:
            manager.delete_task(42)
        mock_print.assert_called_once_with("No se encontró la tarea con ID 42.")

    def test_delete_task_not_found_does_not_save(self):
        manager = make_manager()
        with patch.object(manager, "save_tasks") as mock_save:
            manager.delete_task(42)
        mock_save.assert_not_called()

    def test_delete_task_leaves_list_empty_when_last_task_removed(self):
        manager = make_manager([{"id": 1, "description": "Only task", "completed": False}])
        with patch.object(manager, "save_tasks"):
            manager.delete_task(1)
        self.assertEqual(manager._tasks, [])


# ─────────────────────────────────────────────────────────────────────────────
# TaskManager – load_tasks
# ─────────────────────────────────────────────────────────────────────────────

class TestLoadTasks(unittest.TestCase):

    def test_load_tasks_populates_tasks(self):
        data = [
            {"id": 1, "description": "Task one", "completed": False},
            {"id": 2, "description": "Task two", "completed": True},
        ]
        manager = make_manager()
        with patch("builtins.open", mock_open(read_data=json.dumps(data))):
            manager.load_tasks()
        self.assertEqual(len(manager._tasks), 2)
        self.assertEqual(manager._tasks[0].description, "Task one")
        self.assertTrue(manager._tasks[1].completed)

    def test_load_tasks_creates_task_instances(self):
        data = [{"id": 1, "description": "Type check", "completed": False}]
        manager = make_manager()
        with patch("builtins.open", mock_open(read_data=json.dumps(data))):
            manager.load_tasks()
        self.assertIsInstance(manager._tasks[0], Task)

    def test_load_tasks_sets_next_id_to_last_id_plus_one(self):
        data = [{"id": 5, "description": "X", "completed": False}]
        manager = make_manager()
        with patch("builtins.open", mock_open(read_data=json.dumps(data))):
            manager.load_tasks()
        self.assertEqual(manager._next_id, 6)

    def test_load_tasks_empty_json_resets_tasks_and_next_id(self):
        manager = make_manager()
        with patch("builtins.open", mock_open(read_data=json.dumps([]))):
            manager.load_tasks()
        self.assertEqual(manager._tasks, [])
        self.assertEqual(manager._next_id, 1)

    def test_load_tasks_file_not_found_prints_message(self):
        manager = make_manager()
        with patch("builtins.open", side_effect=FileNotFoundError), \
             patch("builtins.print") as mock_print:
            manager.load_tasks()
        mock_print.assert_called_once_with(
            f"No se encontró el archivo {TaskManager.FILENAME}."
        )

    def test_load_tasks_file_not_found_leaves_tasks_empty(self):
        manager = make_manager()
        with patch("builtins.open", side_effect=FileNotFoundError):
            manager.load_tasks()
        self.assertEqual(manager._tasks, [])

    def test_load_tasks_invalid_json_prints_message(self):
        manager = make_manager()
        with patch("builtins.open", mock_open(read_data="NOT_VALID_JSON")), \
             patch("builtins.print") as mock_print:
            manager.load_tasks()
        mock_print.assert_called_once_with(
            f"Error al leer el archivo {TaskManager.FILENAME}."
        )

    def test_load_tasks_invalid_json_leaves_tasks_empty(self):
        manager = make_manager()
        with patch("builtins.open", mock_open(read_data="NOT_VALID_JSON")):
            manager.load_tasks()
        self.assertEqual(manager._tasks, [])


# ─────────────────────────────────────────────────────────────────────────────
# TaskManager – save_tasks
# ─────────────────────────────────────────────────────────────────────────────

class TestSaveTasks(unittest.TestCase):

    def test_save_tasks_writes_correct_json(self):
        manager = make_manager([{"id": 1, "description": "Save me", "completed": False}])
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            manager.save_tasks()
        written = "".join(call.args[0] for call in mock_file().write.call_args_list)
        parsed = json.loads(written)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["id"], 1)
        self.assertEqual(parsed[0]["description"], "Save me")
        self.assertFalse(parsed[0]["completed"])

    def test_save_tasks_empty_list_writes_empty_array(self):
        manager = make_manager()
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            manager.save_tasks()
        written = "".join(call.args[0] for call in mock_file().write.call_args_list)
        parsed = json.loads(written)
        self.assertEqual(parsed, [])

    def test_save_tasks_io_error_prints_message(self):
        manager = make_manager()
        with patch("builtins.open", side_effect=IOError), \
             patch("builtins.print") as mock_print:
            manager.save_tasks()
        mock_print.assert_called_once_with(
            f"Error al guardar el archivo {TaskManager.FILENAME}."
        )

    def test_save_tasks_multiple_tasks_all_persisted(self):
        manager = make_manager([
            {"id": 1, "description": "Alpha", "completed": False},
            {"id": 2, "description": "Beta",  "completed": True},
        ])
        mock_file = mock_open()
        with patch("builtins.open", mock_file):
            manager.save_tasks()
        written = "".join(call.args[0] for call in mock_file().write.call_args_list)
        parsed = json.loads(written)
        self.assertEqual(len(parsed), 2)
        self.assertEqual(parsed[1]["description"], "Beta")
        self.assertTrue(parsed[1]["completed"])


if __name__ == "__main__":
    unittest.main()
