# File Organizer 

A modular, feature-packed Python application for sorting files, undoing actions, detecting duplicates, monitoring folders in real-time, and launching a Graphical Desktop Interface.

---

## Key Features 

- **Extension Categorization**: Sorts files into `Images`, `Documents`, `Audio`, `Videos`, `Archives`, `Code`, and `Others`.
- **Undo Support (`--undo`)**: Roll back the last organization session and restore files to their original paths.
- **Date-Based Folders (`--date-sort`)**: Sort files into `Category/YYYY/Month/` based on creation timestamp.
- **Duplicate Scanner (`--find-duplicates`)**: Uses SHA-256 chunk hashing to move duplicate files into `Duplicates/`.
- **Auto-Unzipper (`--unzip`)**: Automatically extracts `.zip` archive files into dedicated folders.
- **Smart Renamer (`--clean-names`)**: Renames messy UUID or hash filenames (e.g. `00ab967...jpg`) into clean indexed names.
- **Live Watcher (`--watch`)**: Monitors target folder in real-time and auto-sorts new downloads instantly.
- **Desktop GUI (`--gui` or `file-organizer-gui`)**: Launch a modern Graphical Desktop window with feature toggles and progress logs.

---

## Project Architecture

```text
File-Organizer/
│
├── file_organizer/                # Main Python Package
│   ├── __init__.py                # Version 2.0.0
│   ├── main.py                    # CLI launcher & flag handler
│   ├── organizer.py               # Core FileOrganizer engine
│   ├── rules.py                   # Extension & category rules
│   ├── utils.py                   # Date extractor, smart renamer, path collision handlers
│   ├── undo.py                    # Transaction recorder & rollback manager
│   ├── duplicates.py              # SHA-256 duplicate file detector
│   ├── watcher.py                 # Live background directory monitor
│   └── gui.py                     # Tkinter Desktop GUI
│
├── config/
│   └── categories.json            # Category mapping configuration
│
├── tests/                         # Unit tests
│   ├── test_organizer.py
│   ├── test_rules.py
│   ├── test_undo.py
│   └── test_duplicates.py
│
├── logs/                          # Log & history
│   ├── organizer.log
│   └── history.json
│
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

---

## Manual Commands Guide

### 1. Launch Desktop GUI Window
```bash
python -m file_organizer.main --gui
```
*(Or after `pip install -e .`, simply type `file-organizer-gui` in terminal!)*

### 2. Rollback / Undo Last Session
```bash
python -m file_organizer.main --undo
```

### 3. Organize with Date-Based Subfolders (`Category/YYYY/Month`)
```bash
python -m file_organizer.main -p "C:\Users\YourName\Downloads" --date-sort
```

### 4. Scan & Move Duplicate Files
```bash
python -m file_organizer.main -p "C:\Users\YourName\Downloads" --find-duplicates
```

### 5. Dry-Run (Preview without changing disk)
```bash
python -m file_organizer.main -p "C:\Users\YourName\Downloads" --dry-run
```

### 6. Start Live Background Auto-Sort Watcher
```bash
python -m file_organizer.main -p "C:\Users\YourName\Downloads" --watch
```

### 7. Run Unit Test Suite
```bash
python -m unittest discover tests
```

### 8. Install Editable CLI Commands (`file-organizer` & `file-organizer-gui`)
```bash
pip install -e .
```
