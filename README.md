# VEYRA Daily Planner

**Version:** 1.0  
**Developer:** Rohisha Ramauthar  
**Studio:** VEYRA Studio  
**Platform:** Windows Desktop

## Overview

VEYRA Daily Planner is a desktop productivity application developed in Python. It provides a simple interface for managing daily tasks, monitoring completion progress, and maintaining a persistent task list between sessions.

## Features

- Add, edit, delete, and complete tasks
- Automatic task saving and restoration
- Real-time task completion counters
- Visual productivity progress bar
- Scrollable task management interface
- Dark-themed graphical user interface
- Custom VEYRA Studio branding
- Packaged Windows executable

## Technologies Used

- Python 3.14
- CustomTkinter
- Pillow
- JSON
- PyInstaller

## Installation

1. Download the Windows release folder.
2. Keep `VEYRA Daily Planner.exe` and the `_internal` folder together.
3. Double-click `VEYRA Daily Planner.exe` to launch the application.

No separate Python installation is required when using the packaged executable.

## Data Storage

Tasks are saved locally in the user's application data directory using JSON.

On Windows, the application stores tasks at:

`%LOCALAPPDATA%\VEYRA\DailyPlanner\tasks.json`

## Development Skills Demonstrated

- Python application development
- Desktop GUI design
- Event-driven programming
- File handling and JSON persistence
- Application state management
- Input validation
- Windows executable packaging
- Software testing and debugging

## Future Improvements

- Task priorities and categories
- Due dates and reminders
- Task search and filtering
- Productivity analytics
- Export and backup functionality

## Developer

Developed by Rohisha Ramauthar under VEYRA Studio.

**Version 1.0 — Initial Windows Desktop Release**