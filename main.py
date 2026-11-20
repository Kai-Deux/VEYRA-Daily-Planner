
# ============================================================
# VEYRA DAILY PLANNER
# Developer: Rohisha
# Developed under: VEYRA Studio
# Version: 1.0
# ============================================================

import customtkinter as ctk
import json
import os
import shutil
import sys

from pathlib import Path
from PIL import Image


# ============================================================
# APPLICATION PATHS
# ============================================================

# Locate application assets in development and packaged versions
if getattr(sys, "frozen", False):
    base_path = Path(
        getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent)
    )
else:
    base_path = Path(__file__).resolve().parent

logo_path = base_path / "assets" / "veyra_planner_logo.png"


# ============================================================
# PERMANENT TASK STORAGE
# ============================================================

# Store tasks in the Windows user profile
app_data = os.getenv("LOCALAPPDATA")

if app_data:
    data_directory = Path(app_data) / "VEYRA" / "DailyPlanner"
else:
    data_directory = Path.home() / ".veyra" / "DailyPlanner"

data_directory.mkdir(parents=True, exist_ok=True)

data_file: Path = data_directory / "tasks.json"

# Preserve existing tasks from the development version
# Only migrate automatically when running the Python source.
if not getattr(sys, "frozen", False):
    old_data_file = Path(__file__).resolve().parent / "tasks.json"

    if not data_file.exists() and old_data_file.exists():
        shutil.copy2(old_data_file, data_file)


# ============================================================
# APPLICATION SETTINGS
# ============================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app: ctk.CTk = ctk.CTk()

app.title("VEYRA Daily Planner")
app.geometry("950x750")
app.minsize(750, 650)


# ============================================================
# TASK COUNTERS
# ============================================================

total_tasks: int = 0
completed_tasks: int = 0


# ============================================================
# APPLICATION LOGO
# ============================================================

with Image.open(logo_path) as image:
    logo_source = image.copy()

logo_image = ctk.CTkImage(
    light_image=logo_source,
    dark_image=logo_source,
    size=(240, 160)
)

logo_label = ctk.CTkLabel(
    app,
    image=logo_image,
    text=""
)

logo_label.pack(pady=(10, 0))


# ============================================================
# APPLICATION HEADING
# ============================================================

heading: ctk.CTkLabel = ctk.CTkLabel(
    app,
    text="VEYRA Daily Planner",
    font=("Arial", 28, "bold")
)

heading.pack(pady=(5, 5))


# VEYRA Studio branding
branding_label: ctk.CTkLabel = ctk.CTkLabel(
    app,
    text="Developed by VEYRA Studio",
    font=("Arial", 12),
    text_color="#94A3B8"
)

branding_label.pack(pady=(0, 10))


# ============================================================
# TASK COUNTER LABELS
# ============================================================

task_counter_label: ctk.CTkLabel = ctk.CTkLabel(
    app,
    text=f"Total Tasks: {total_tasks}",
    font=("Arial", 16)
)

task_counter_label.pack(pady=5)


completed_counter_label: ctk.CTkLabel = ctk.CTkLabel(
    app,
    text=f"Completed Tasks: {completed_tasks}",
    font=("Arial", 16),
    text_color="#22C55E"
)

completed_counter_label.pack(pady=5)


# ============================================================
# PRODUCTIVITY PROGRESS BAR
# ============================================================

progress_bar: ctk.CTkProgressBar = ctk.CTkProgressBar(
    app,
    width=450,
    height=15,
    corner_radius=10,
    progress_color="#22C55E"
)

progress_bar.pack(pady=15)
progress_bar.set(0)


# ============================================================
# TASK INPUT FIELD
# ============================================================

task_entry: ctk.CTkEntry = ctk.CTkEntry(
    app,
    placeholder_text="What do you want to do today?",
    width=450,
    height=45,
    corner_radius=10
)

task_entry.pack(pady=15)


# ============================================================
# LOAD SAVED TASKS
# ============================================================

def load_tasks() -> list[dict]:

    if data_file.exists():
        try:
            with data_file.open("r", encoding="utf-8") as file:
                saved_tasks = json.load(file)

            if isinstance(saved_tasks, list):
                return [
                    task for task in saved_tasks
                    if isinstance(task, dict)
                    and isinstance(task.get("name"), str)
                    and isinstance(task.get("completed"), bool)
                ]

        except (json.JSONDecodeError, OSError):
            print("Unable to load saved tasks.")

    return []


# Store tasks in memory
tasks: list[dict] = load_tasks()


# ============================================================
# SAVE TASKS
# ============================================================

def save_tasks() -> None:

    with data_file.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


# ============================================================
# UPDATE COUNTERS AND PROGRESS
# ============================================================

def update_counters() -> None:

    global total_tasks, completed_tasks

    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task["completed"]
    )

    task_counter_label.configure(
        text=f"Total Tasks: {total_tasks}"
    )

    completed_counter_label.configure(
        text=f"Completed Tasks: {completed_tasks}"
    )

    progress = (
        completed_tasks / total_tasks
        if total_tasks > 0
        else 0.0
    )

    progress_bar.set(progress)


# ============================================================
# UPDATE TASK COMPLETION STATUS
# ============================================================

def update_task_status(
    task_checkbox: ctk.CTkCheckBox,
    task_data: dict
) -> None:

    is_completed = bool(task_checkbox.get())

    task_data["completed"] = is_completed

    if is_completed:
        task_checkbox.configure(
            text_color="#22C55E"
        )
    else:
        task_checkbox.configure(
            text_color=("gray10", "gray90")
        )

    update_counters()
    save_tasks()


# ============================================================
# DELETE TASK
# ============================================================

def delete_task(
    task_data: dict,
    task_row: ctk.CTkFrame
) -> None:

    # Remove the exact task from memory
    for index, existing_task in enumerate(tasks):
        if existing_task is task_data:
            tasks.pop(index)
            break
    else:
        return

    # Remove task from interface
    task_row.destroy()

    # Update counters and storage
    update_counters()
    save_tasks()


# ============================================================
# EDIT TASK
# ============================================================

def edit_task(
    task_data: dict,
    task_checkbox: ctk.CTkCheckBox,
    new_name: str
) -> None:

    new_name = new_name.strip()

    if not new_name:
        return

    task_data["name"] = new_name

    task_checkbox.configure(
        text=new_name
    )

    save_tasks()


# ============================================================
# OPEN EDIT WINDOW
# ============================================================

def open_edit_window(
    task_data: dict,
    task_checkbox: ctk.CTkCheckBox
) -> None:

    edit_window = ctk.CTkToplevel(app)

    edit_window.title("Edit Task")
    edit_window.geometry("400x220")
    edit_window.resizable(False, False)

    # Task name input
    edit_entry = ctk.CTkEntry(
        edit_window,
        width=300,
        height=40
    )

    edit_entry.pack(pady=(30, 15))
    edit_entry.insert(0, task_data["name"])

    # Save edited task
    def save_changes() -> None:

        new_name = edit_entry.get().strip()

        if new_name:
            edit_task(
                task_data,
                task_checkbox,
                new_name
            )

            edit_window.destroy()

    # Save Changes button
    save_button = ctk.CTkButton(
        edit_window,
        text="Save Changes",
        width=150,
        height=40,
        command=save_changes
    )

    save_button.pack(pady=10)

    # Save by pressing Enter
    edit_entry.bind(
        "<Return>",
        lambda event: save_changes()
    )

    edit_window.after(100, edit_entry.focus_set)


# ============================================================
# CREATE TASK ROW
# ============================================================

def create_task_row(task_data: dict) -> None:

    task_name = task_data["name"]

    # Task row container
    task_row = ctk.CTkFrame(
        task_frame,
        fg_color="transparent"
    )

    task_row.pack(
        fill="x",
        padx=10,
        pady=5
    )

    # Task checkbox
    task_checkbox = ctk.CTkCheckBox(
        task_row,
        text=task_name,
        font=("Arial", 16),
        width=250,
        height=30
    )

    task_checkbox.configure(
        command=lambda: update_task_status(
            task_checkbox,
            task_data
        )
    )

    # Restore completion status
    if task_data["completed"]:

        task_checkbox.select()

        task_checkbox.configure(
            text_color="#22C55E"
        )

    else:

        task_checkbox.deselect()

        task_checkbox.configure(
            text_color=("gray10", "gray90")
        )

    task_checkbox.pack(
        side="left",
        padx=5,
        pady=5
    )

    # Delete button
    delete_button = ctk.CTkButton(
        task_row,
        text="Delete",
        width=70,
        height=30,
        fg_color="#DC2626",
        hover_color="#B91C1C",
        command=lambda: delete_task(
            task_data,
            task_row
        )
    )

    delete_button.pack(
        side="right",
        padx=5
    )

    # Edit button
    edit_button = ctk.CTkButton(
        task_row,
        text="Edit",
        width=60,
        height=30,
        fg_color="#2563EB",
        hover_color="#1D4ED8",
        command=lambda: open_edit_window(
            task_data,
            task_checkbox
        )
    )

    edit_button.pack(
        side="right",
        padx=5
    )


# ============================================================
# ADD TASK
# ============================================================

def add_task() -> None:

    task = task_entry.get().strip()

    if not task:
        return

    # Create new task
    task_data = {
        "name": task,
        "completed": False
    }

    tasks.append(task_data)

    # Display new task
    create_task_row(task_data)

    # Update counters and save
    update_counters()
    save_tasks()

    # Clear input field
    task_entry.delete(0, "end")
    task_entry.focus_set()


# ============================================================
# ADD TASK BUTTON
# ============================================================

add_task_button = ctk.CTkButton(
    app,
    text="Add Task",
    width=200,
    height=45,
    corner_radius=10,
    command=add_task
)

add_task_button.pack(pady=10)


# Add tasks using Enter
task_entry.bind(
    "<Return>",
    lambda event: add_task()
)


# ============================================================
# SCROLLABLE TASK CONTAINER
# ============================================================

task_frame = ctk.CTkScrollableFrame(
    app,
    width=540,
    height=300,
    corner_radius=10
)

task_frame.pack(
    pady=15,
    padx=20,
    fill="both",
    expand=True
)


# ============================================================
# DISPLAY SAVED TASKS
# ============================================================

def display_saved_tasks() -> None:

    for task_data in tasks:
        create_task_row(task_data)

    update_counters()


# Restore saved tasks
display_saved_tasks()


# ============================================================
# APPLICATION STARTUP
# ============================================================

# Focus the task input field
app.after(100, task_entry.focus_set)

# Start the application
app.mainloop()
