# Enhanced Command-Line To-Do List

This repository contains an enhanced command-line To-Do list manager written in Python. Tasks are stored in `tasks.json` in the project directory.

## Features
- Automatic detection of simple due dates (`today`, `tomorrow`, or `YYYY-MM-DD`)
- Basic AI-based categorization of tasks (work, personal, or general)
- Interactive mode for a more user-friendly experience

## Usage

1. **Add a task**
   ```bash
   python todo.py add "Buy groceries tomorrow"
   ```

2. **List tasks**
   ```bash
   python todo.py list
   ```

3. **Mark a task as complete**
   ```bash
   python todo.py complete 1
   ```

4. **Interactive mode**
   ```bash
   python todo.py interactive
   ```
