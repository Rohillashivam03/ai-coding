import json
import argparse
from pathlib import Path

DATA_FILE = Path("tasks.json")


def load_tasks():
    if DATA_FILE.exists():
        with DATA_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)


def add_task(text):
    tasks = load_tasks()
    tasks.append({"task": text, "done": False})
    save_tasks(tasks)
    print(f"Added task: {text}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, t in enumerate(tasks, start=1):
        status = "\u2713" if t.get("done") else " "
        print(f"[{status}] {i}. {t['task']}")


def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        print(f"Marked task {index + 1} as complete.")
    else:
        print("Invalid task number.")


def parse_args():
    parser = argparse.ArgumentParser(description="Simple command-line To-Do list")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", help="Task description")

    subparsers.add_parser("list", help="List tasks")

    complete_parser = subparsers.add_parser("complete", help="Mark a task as done")
    complete_parser.add_argument("number", type=int, help="Task number to mark complete")

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "add":
        add_task(args.text)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.number - 1)
    else:
        print("No command provided. Use -h for help.")


if __name__ == "__main__":
    main()
