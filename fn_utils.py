import os
import psutil

def get_disk_usage():
    usage = psutil.disk_usage("/")
    total = usage.total / (1024 ** 3)
    used = usage.used / (1024 ** 3)
    free = usage.free / (1024 ** 3)
    return total, used, free

def scan_directory(path, progress_callback):
    folder_sizes = {}
    total_files = 0
    total_size = 0
    files_processed = 0

    for dirpath, dirnames, filenames in os.walk(path):
        total_files += len(filenames)

    for dirpath, dirnames, filenames in os.walk(path):
        folder_size = 0
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            try:
                folder_size += os.path.getsize(filepath)
            except (PermissionError, FileNotFoundError):
                continue
        folder_sizes[dirpath] = folder_size
        total_size += folder_size
        files_processed += len(filenames)

        progress_callback(files_processed, total_files)

    return sorted(folder_sizes.items(), key=lambda x: x[1], reverse=True)

def update_progress(files_processed, total_files, progress_bar, root):
    if total_files > 0:
        progress = (files_processed / total_files) * 100
        root.after(0, lambda: progress_bar.config(value=progress))
