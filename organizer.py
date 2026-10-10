import argparse
import shutil
import os
from pathlib import Path

CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".heif", ".psd"],
    "Documents": [".doc", ".docx", ".odt", ".rtf", ".pages", ".epub", ".xls", ".xlsx", ".ods", ".ppt", ".pptx"],
    "PDF": [".pdf"],
    "Text": [".txt", ".md", ".log"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".iso", ".dmg"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg", ".wma"],
    "Video": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".mpg", ".mpeg"],
    "Web": [".html", ".htm", ".css", ".js"],
    "Code": [".py", ".java", ".c", ".cpp", ".sh"],
    "Data": [".csv", ".json", ".xml"],
    "Executables": [".exe", ".msi"],
}


def get_category(file):
    extension = file.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def get_unique_path(destination, reserved):
    if not destination.exists() and destination not in reserved:
        return destination
    counter = 1
    while True:
        new_name = f"{destination.stem} ({counter}){destination.suffix}"
        new_path = destination.with_name(new_name)
        if not new_path.exists() and new_path not in reserved:
            return new_path
        counter += 1


def organize(source, target, dry_run, log=print):
    reserved = set()  
    skip_names = {"organizer.py", "gui.py"}  
    moved = 0

    for item in sorted(source.iterdir()):
        if not item.is_file():
            continue
        if item.name in skip_names:
            continue

        category = get_category(item)
        target_folder = target / category
        destination = get_unique_path(target_folder / item.name, reserved)
        reserved.add(destination)

        if dry_run:
            log(f"[DRY RUN] {item.name} -> {category}/{destination.name}")
        else:
            target_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(destination))
            log(f"{item.name} -> {category}/{destination.name}")
        moved += 1

    action = "would be moved" if dry_run else "moved"
    log(f"\nDone: {moved} file(s) {action}.")

def main():
    parser = argparse.ArgumentParser(description="Sort files into folders by file type.")
    parser.add_argument("source", nargs="?", default=".", help="folder to organize (default: current folder)")
    parser.add_argument("-t", "--target", help="base folder for the category folders (default: same as source)")
    parser.add_argument("-d", "--dry-run", action="store_true", help="show planned moves without moving anything")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_dir():
        print(f"Error: '{source}' is not a valid folder.")
        return

    target = Path(args.target) if args.target else source
    organize(source, target, args.dry_run)


if __name__ == "__main__":
    main()