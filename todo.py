import json
import argparse
import re
from datetime import datetime, timedelta
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


def parse_due_date(text: str):
    text = text.lower()
    today = datetime.now().date()
    if "tomorrow" in text:
        return str(today + timedelta(days=1))
    if "today" in text:
        return str(today)
    match = re.search(r"(\d{4}-\d{2}-\d{2})", text)
    if match:
        return match.group(1)
    return ""


def categorize_task(text: str):
    text = text.lower()
    if any(word in text for word in ["buy", "pay", "call"]):
        return "personal"
    if any(word in text for word in ["email", "meet", "review"]):
        return "work"
    return "general"


def add_task(text):
    tasks = load_tasks()
    due = parse_due_date(text)
    category = categorize_task(text)
    tasks.append({"task": text, "done": False, "due": due, "category": category})
    save_tasks(tasks)
    print(f"Added task: {text}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    for i, t in enumerate(tasks, start=1):
        status = "\u2713" if t.get("done") else " "
        due = f" (due {t['due']})" if t.get("due") else ""
        cat = f" [{t['category']}]" if t.get("category") else ""
        print(f"[{status}] {i}. {t['task']}{due}{cat}")


def complete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["done"] = True
        save_tasks(tasks)
        print(f"Marked task {index + 1} as complete.")
    else:
        print("Invalid task number.")


def interactive_mode():
    print("Entering interactive mode. Type 'help' for commands.")
    while True:
        try:
            command = input(" > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not command:
            continue
        if command == "exit" or command == "quit":
            break
        if command == "help":
            print("Commands: add <task>, list, complete <num>, quit")
            continue
        if command.startswith("add "):
            add_task(command[4:].strip())
            continue
        if command == "list":
            list_tasks()
            continue
        if command.startswith("complete "):
            try:
                num = int(command.split()[1])
                complete_task(num - 1)
            except (IndexError, ValueError):
                print("Invalid command. Usage: complete <num>")
            continue
        print("Unknown command. Type 'help' for options.")


def parse_args():
    parser = argparse.ArgumentParser(description="Enhanced command-line To-Do list")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("text", help="Task description")

    subparsers.add_parser("list", help="List tasks")

    complete_parser = subparsers.add_parser("complete", help="Mark a task as done")
    complete_parser.add_argument("number", type=int, help="Task number to mark complete")

    subparsers.add_parser("interactive", help="Interactive mode")

    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "add":
        add_task(args.text)
    elif args.command == "list":
        list_tasks()
    elif args.command == "complete":
        complete_task(args.number - 1)
    elif args.command == "interactive":
        interactive_mode()
    else:
        print("No command provided. Use -h for help.")


if __name__ == "__main__":
    main()
