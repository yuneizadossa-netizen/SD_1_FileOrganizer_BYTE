import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

from organizer import organize

# Color palette (dark theme with blue and purple)
BG = "#12122a"           # window background (dark navy)
PANEL = "#1c1c3c"        # panel background
PURPLE = "#8b5cf6"       # main accent
PURPLE_HOVER = "#a78bfa"
BLUE = "#3b82f6"         # secondary accent
BLUE_HOVER = "#60a5fa"
TEXT = "#e5e7eb"
MUTED = "#9ca3af"
LOG_BG = "#0b0b1c"
LOG_TEXT = "#93c5fd"

FONT = ("Segoe UI", 10)
FONT_BOLD = ("Segoe UI", 10, "bold")


class FancyButton(tk.Button):
    """Button with a hover effect."""

    def __init__(self, master, color, hover, **kwargs):
        super().__init__(
            master,
            bg=color,
            fg="white",
            activebackground=hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=14,
            pady=6,
            font=FONT_BOLD,
            cursor="hand2",
            **kwargs,
        )
        self.color = color
        self.hover = hover
        self.bind("<Enter>", lambda e: self.configure(bg=self.hover))
        self.bind("<Leave>", lambda e: self.configure(bg=self.color))


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("720x540")
        self.configure(bg=BG)

        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.dry_run_var = tk.BooleanVar(value=True)

        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=PURPLE)
        header.pack(fill="x")
        tk.Label(header, text="File Organizer", bg=PURPLE, fg="white",
                 font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=20, pady=(12, 0))
        tk.Label(header, text="Sort your files into folders by type",
                 bg=PURPLE, fg="#ede9fe", font=FONT).pack(anchor="w", padx=20, pady=(0, 12))

        # Settings panel
        panel = tk.Frame(self, bg=PANEL, padx=15, pady=15)
        panel.pack(fill="x", padx=15, pady=15)

        tk.Label(panel, text="Source folder", bg=PANEL, fg=TEXT,
                 font=FONT_BOLD).grid(row=0, column=0, sticky="w")
        self.make_entry(panel, self.source_var).grid(row=0, column=1, padx=10, pady=4)
        FancyButton(panel, BLUE, BLUE_HOVER, text="Browse",
                    command=self.choose_source).grid(row=0, column=2)

        tk.Label(panel, text="Target folder", bg=PANEL, fg=TEXT,
                 font=FONT_BOLD).grid(row=1, column=0, sticky="w")
        self.make_entry(panel, self.target_var).grid(row=1, column=1, padx=10, pady=4)
        FancyButton(panel, BLUE, BLUE_HOVER, text="Browse",
                    command=self.choose_target).grid(row=1, column=2)

        tk.Label(panel, text="Target is optional. If empty, the source folder is used.",
                 bg=PANEL, fg=MUTED, font=("Segoe UI", 9)).grid(row=2, column=1, sticky="w")

        tk.Checkbutton(
            panel, text="Dry run (only show what would happen)",
            variable=self.dry_run_var, bg=PANEL, fg=TEXT, font=FONT,
            selectcolor=BG, activebackground=PANEL, activeforeground=TEXT,
        ).grid(row=3, column=1, sticky="w", pady=(8, 0))

        # Action buttons
        buttons = tk.Frame(self, bg=BG)
        buttons.pack(fill="x", padx=15)
        FancyButton(buttons, PURPLE, PURPLE_HOVER, text="Organize",
                    command=self.run).pack(side="left")
        FancyButton(buttons, BLUE, BLUE_HOVER, text="Save log",
                    command=self.save_log).pack(side="left", padx=8)
        FancyButton(buttons, "#4b5563", "#6b7280", text="Clear",
                    command=self.clear_log).pack(side="left")
        FancyButton(buttons, "#4b5563", "#6b7280", text="Create test files",
                    command=self.create_test_files).pack(side="left", padx=8)

        # Log box
        self.log_box = scrolledtext.ScrolledText(
            self, state="disabled", height=14, bg=LOG_BG, fg=LOG_TEXT,
            insertbackground="white", font=("Consolas", 10), relief="flat",
            padx=10, pady=10,
        )
        self.log_box.pack(fill="both", expand=True, padx=15, pady=15)

    def make_entry(self, parent, variable):
        return tk.Entry(parent, textvariable=variable, width=50, bg=LOG_BG, fg=TEXT,
                        insertbackground="white", relief="flat", font=FONT,
                        highlightthickness=1, highlightbackground="#3f3f6b",
                        highlightcolor=PURPLE)

    def choose_source(self):
        folder = filedialog.askdirectory(title="Choose the folder to organize")
        if folder:
            self.source_var.set(folder)

    def choose_target(self):
        folder = filedialog.askdirectory(title="Choose the target folder")
        if folder:
            self.target_var.set(folder)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")
        self.update_idletasks()

    def clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")

    def create_test_files(self):
        folder = filedialog.askdirectory(title="Choose where to create the test folder")
        if not folder:
            return

        test_folder = Path(folder) / "TestFolder"
        test_folder.mkdir(exist_ok=True)

        sample_files = ["photo.jpg", "song.mp3", "notes.txt", "report.pdf",
                        "video.mp4", "archive.zip", "unknown.xyz"]
        for name in sample_files:
            (test_folder / name).touch()

        self.source_var.set(str(test_folder))
        self.log(f"Test folder created: {test_folder}")
        self.log(f"{len(sample_files)} sample files added. Click Organize to try it.\n")

    def save_log(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            initialfile="sample_run_log.txt")
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.log_box.get("1.0", "end"))

    def run(self):
        source = Path(self.source_var.get())
        if not source.is_dir():
            messagebox.showerror("Error", "Please choose a valid source folder.")
            return

        target = Path(self.target_var.get()) if self.target_var.get() else source
        dry_run = self.dry_run_var.get()

        if not dry_run:
            if not messagebox.askyesno("Confirm", f"Files in '{source}' will be moved. Continue?"):
                return

        organize(source, target, dry_run, log=self.log)


if __name__ == "__main__":
    App().mainloop()