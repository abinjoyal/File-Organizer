from setuptools import setup, find_packages

setup(
    name="file_organizer",
    version="2.0.0",
    description="Automated Python file organizer tool with GUI, Undo, Duplicate Detection, and Live Watcher.",
    author="File Organizer Team",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "file-organizer=file_organizer.main:main",
            "file-organizer-gui=file_organizer.gui:launch_gui",
        ],
    },
    python_requires=">=3.7",
)
