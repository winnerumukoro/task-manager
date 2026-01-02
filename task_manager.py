import json
import os
import datetime
from typing import List, Dict

DATA_FILE = "tasks.json"


class Task:
    def __init__(self, title: str, description: str, priority: int):
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.datetime.now().isoformat()

    def mark_completed(self):
        self.completed = True

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data: Dict):
        task = Task(
            title=data["title"],
            description=data["description"],
            priority=data["priority"]
        )
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        return task


class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.load_tasks()

    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    def delete_task(self, index: int):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()

    def mark_task_completed(self, index: int):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            self.save_tasks()

    def list_tasks(self):
        if not self.tasks:
            print("\nNo tasks available.\n")
            return

        print("\nYour Tasks:")
        print("-" * 50)
        for i, task in enumerate(self.tasks):
            status = "✔" if task.completed else "✘"
            print(f"{i + 1}. [{status}] {task.title}")
            print(f"   Priority: {task.priority}")
            print(f"   Created: {task.created_at}")
            print(f"   Description: {task.description}")
            print("-" * 50)

    def task_statistics(self):
        total = len(self.tasks)
        completed = sum(task.completed for task in self.tasks)
        pending = total - completed

        print("\nTask Statistics")
        print("-" * 30)
        print(f"Total Tasks    : {total}")
        print(f"Completed      : {completed}")
        print(f"Pending        : {pending}")
        print("-" * 30)

    def save_tasks(self):
        with open(DATA_FILE, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def load_tasks(self):
        if not os.path.exists(DATA_FILE):
            return

        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            self.tasks = [Task.from_dict(task) for task in data]


def print_menu():
    print("\n=== TASK MANAGER ===")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Mark Task as Completed")
    print("4. Delete Task")
    print("5. Task Statistics")
    print("6. Exit")


def get_priority() -> int:
    while True:
        try:
            priority = int(input("Enter priority (1–5): "))
            if 1 <= priority <= 5:
                return priority
            else:
                print("Priority must be between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")


def main():
    manager = TaskManager()

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task Title: ").strip()
            description = input("Task Description: ").strip()
            priority = get_priority()
            task = Task(title, description, priority)
            manager.add_task(task)
            print("Task added successfully.")

        elif choice == "2":
            manager.list_tasks()

        elif choice == "3":
            manager.list_tasks()
            try:
                index = int(input("Enter task number to mark completed: ")) - 1
                manager.mark_task_completed(index)
                print("Task marked as completed.")
            except ValueError:
                print("Invalid input.")

        elif choice == "4":
            manager.list_tasks()
            try:
                index = int(input("Enter task number to delete: ")) - 1
                manager.delete_task(index)
                print("Task deleted.")
            except ValueError:
                print("Invalid input.")

        elif choice == "5":
            manager.task_statistics()

        elif choice == "6":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()