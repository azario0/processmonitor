# Process Monitor

Process Monitor is a Python-based application that allows users to visualize, filter, and manage running processes on their system. It provides a user-friendly graphical interface built with Tkinter and uses the psutil library to interact with system processes.

## Features

- Display all running processes categorized by importance (high, medium, low).
- Search for processes by name.
- Refresh the list of running processes.
- Terminate (kill) specific processes.
- User-friendly interface with scrollable process list.

## Installation

### Prerequisites

- Python 3.x
- `pip` (Python package installer)

### Install Required Packages

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/process-monitor.git
    cd process-monitor
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Create a `requirements.txt` file with the following content:

    ```txt
    tkinter
    psutil
    ```

## Usage

To run the application, execute the following command in your terminal:

```sh
python process_monitor.py
```
Creating an Executable

To create a standalone executable, you can use PyInstaller:

    Install PyInstaller:

    sh

pip install pyinstaller

Navigate to the directory containing process_monitor.py and run:

sh

    pyinstaller --onefile process_monitor.py

    The executable will be created in the dist directory.

File Structure

    process_monitor.py: Main script for the Process Monitor application.
    README.md: This file.
    requirements.txt: List of required Python packages.

Functions
get_current_user

python

def get_current_user():
    return pwd.getpwuid(os.geteuid()).pw_name

Returns the username of the current user.
get_process_importance

python

def get_process_importance(proc_info, current_user):
    try:
        if proc_info['username'] == 'root':
            return 'high'
        elif proc_info['username'] == current_user:
            return 'medium'
        else:
            return 'low'
    except KeyError:
        return 'low'

Determines the importance of a process based on its owner.
Class: ProcessMonitor
init

Initializes the main application window and sets up the UI components.
on_frame_configure

Adjusts the scrollable region of the canvas.
frame_width

Adjusts the width of the inner frame to match the canvas width.
refresh_processes

Refreshes the list of processes and categorizes them.
create_category

Creates a category section for processes with a specific importance level.
toggle_category

Shows or hides the processes in a category.
add_process

Adds a process entry to the specified parent frame.
kill_process

Terminates a process by its PID.
search_processes

Filters processes based on the search term.
Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.