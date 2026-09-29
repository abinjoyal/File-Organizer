import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path

from .organizer import FileOrganizer
from .undo import UndoManager
from .duplicates import DuplicateScanner


class OrganizerGUI:
    """Tkinter Desktop Graphical User Interface for File Organizer."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("📁 Python File Organizer v2.0")
        self.root.geometry("680x600")
        self.root.minsize(600, 500)

        self.organizer = FileOrganizer()
        self.undo_manager = UndoManager()
        self.dup_scanner = DuplicateScanner()

        self._build_ui()

    def _build_ui(self):
        # Configure styles
        style = ttk.Style()
        style.theme_use("clam")

        # Top Frame - Folder Selection
        folder_frame = ttk.LabelFrame(self.root, text=" Target Directory ", padding=10)
        folder_frame.pack(fill="x", padx=15, pady=10)

        self.path_var = tk.StringVar(value=str(Path.home() / "Downloads"))
        entry = ttk.Entry(folder_frame, textvariable=self.path_var, font=("Segoe UI", 10))
        entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_browse = ttk.Button(folder_frame, text="📁 Browse", command=self._browse_folder)
        btn_browse.pack(side="right")

        # Options Frame - Feature Toggles
        opts_frame = ttk.LabelFrame(self.root, text=" Organize Options ", padding=10)
        opts_frame.pack(fill="x", padx=15, pady=5)

        self.date_sort_var = tk.BooleanVar(value=False)
        self.unzip_var = tk.BooleanVar(value=False)
        self.clean_names_var = tk.BooleanVar(value=False)
        self.dry_run_var = tk.BooleanVar(value=False)
        self.find_dup_var = tk.BooleanVar(value=False)

        cb1 = ttk.Checkbutton(opts_frame, text="📅 Date-Based Folders (Category/YYYY/MM)", variable=self.date_sort_var)
        cb1.grid(row=0, column=0, sticky="w", pady=3, padx=5)

        cb2 = ttk.Checkbutton(opts_frame, text="📦 Auto-Extract Zip Archives", variable=self.unzip_var)
        cb2.grid(row=0, column=1, sticky="w", pady=3, padx=5)

        cb3 = ttk.Checkbutton(opts_frame, text="🏷️ Smart Clean Filenames (Rename UUIDs)", variable=self.clean_names_var)
        cb3.grid(row=1, column=0, sticky="w", pady=3, padx=5)

        cb4 = ttk.Checkbutton(opts_frame, text="🔍 Move Duplicates to 'Duplicates/'", variable=self.find_dup_var)
        cb4.grid(row=1, column=1, sticky="w", pady=3, padx=5)

        cb5 = ttk.Checkbutton(opts_frame, text="🧪 Dry-Run (Preview only)", variable=self.dry_run_var)
        cb5.grid(row=2, column=0, sticky="w", pady=3, padx=5)

        # Action Buttons Frame
        btn_frame = ttk.Frame(self.root, padding=10)
        btn_frame.pack(fill="x", padx=15, pady=5)

        btn_run = ttk.Button(btn_frame, text="🚀 Organize Now", command=self._run_organize)
        btn_run.pack(side="left", padx=5)

        btn_undo = ttk.Button(btn_frame, text="↩️ Undo Last Session", command=self._run_undo)
        btn_undo.pack(side="left", padx=5)

        btn_dup = ttk.Button(btn_frame, text="🔍 Scan Duplicates", command=self._run_scan_duplicates)
        btn_dup.pack(side="left", padx=5)

        # Log Window
        log_frame = ttk.LabelFrame(self.root, text=" Activity Log ", padding=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, state="disabled", font=("Consolas", 9))
        self.log_text.pack(fill="both", expand=True)

    def _log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.path_var.get())
        if folder:
            self.path_var.set(folder)

    def _run_organize(self):
        target = Path(self.path_var.get())
        if not target.exists():
            messagebox.showerror("Error", f"Directory '{target}' does not exist.")
            return

        self._log(f"=== Starting Organization: {target} ===")
        moved, _ = self.organizer.organize(
            target_directory=target,
            dry_run=self.dry_run_var.get(),
            date_sort=self.date_sort_var.get(),
            unzip=self.unzip_var.get(),
            clean_names=self.clean_names_var.get()
        )

        if self.find_dup_var.get():
            self._log("Scanning for duplicate files...")
            self.dup_scanner.move_duplicates(target, dry_run=self.dry_run_var.get())

        messagebox.showinfo("Completed", f"Processed {moved} file(s)!")

    def _run_undo(self):
        if messagebox.askyesno("Confirm Undo", "Are you sure you want to rollback the last organization session?"):
            self._log("=== Running Rollback / Undo ===")
            restored, failed = self.undo_manager.undo_last_session()
            messagebox.showinfo("Undo Result", f"Restored {restored} file(s). Failed: {failed}")

    def _run_scan_duplicates(self):
        target = Path(self.path_var.get())
        if not target.exists():
            messagebox.showerror("Error", f"Directory '{target}' does not exist.")
            return

        self._log(f"=== Scanning Duplicates in: {target} ===")
        total_dup, moved = self.dup_scanner.move_duplicates(target, dry_run=self.dry_run_var.get())
        messagebox.showinfo("Duplicates Result", f"Found {total_dup} duplicate file(s). Moved: {moved}")


def launch_gui():
    root = tk.Tk()
    app = OrganizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
