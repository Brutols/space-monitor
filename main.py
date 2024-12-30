import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import fn_utils

def start_scan():
    path = filedialog.askdirectory(title="Seleziona una directory")
    if not path:
        return

    btn_scan.config(state="disabled")
    progress_bar.pack(padx=10, pady=10, fill="x")

    try:
        max_dirs = int(entry_max_dirs.get())
        if max_dirs <= 0:
            raise ValueError("Il numero deve essere maggiore di zero.")
    except ValueError as e:
        messagebox.showerror("Errore", f"Errore nel numero di directory: {e}")
        return

    threading.Thread(target=scan_thread, args=(path, max_dirs)).start()

def scan_thread(path, max_dirs):
    try:
        results = fn_utils.scan_directory(path, update_progress)
        tree.delete(*tree.get_children())

        for folder, size in results[:max_dirs]:
            tree.insert("", "end", values=(folder, f"{size / (1024 ** 3):.2f} GB"))
    except Exception as e:
        messagebox.showerror("Errore", f"Si è verificato un errore: {e}")
    finally:
        btn_scan.config(state="normal")
        progress_bar.pack_forget()

def show_disk_usage():
    total, used, free = fn_utils.get_disk_usage()
    lbl_total.config(text=f"Totale: {total:.2f} GB")
    lbl_used.config(text=f"Usato: {used:.2f} GB")
    lbl_free.config(text=f"Libero: {free:.2f} GB")

def update_progress(files_processed, total_files):
    fn_utils.update_progress(files_processed, total_files, progress_bar, root)

root = tk.Tk()
root.title("Monitor Spazio Disco")
root.geometry("600x600")

frame_info = ttk.LabelFrame(root, text="Utilizzo del Disco")
frame_info.pack(fill="x", padx=10, pady=10)

lbl_total = ttk.Label(frame_info, text="Totale: -- GB")
lbl_total.pack(anchor="w", padx=10, pady=2)

lbl_used = ttk.Label(frame_info, text="Usato: -- GB")
lbl_used.pack(anchor="w", padx=10, pady=2)

lbl_free = ttk.Label(frame_info, text="Libero: -- GB")
lbl_free.pack(anchor="w", padx=10, pady=2)

btn_refresh = ttk.Button(frame_info, text="Aggiorna", command=show_disk_usage)
btn_refresh.pack(padx=10, pady=5)

frame_max_dirs = ttk.LabelFrame(root, text="Numero di directory da mostrare")
frame_max_dirs.pack(fill="x", padx=10, pady=10)

lbl_max_dirs = ttk.Label(frame_max_dirs, text="Inserisci il numero di directory:")
lbl_max_dirs.pack(side="left", padx=10)

entry_max_dirs = ttk.Spinbox(frame_max_dirs, from_=1, to=100, width=5)
entry_max_dirs.set(10)
entry_max_dirs.pack(side="left", padx=10)

frame_results = ttk.LabelFrame(root, text="Directory più Grandi")
frame_results.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("Folder", "Size")
tree = ttk.Treeview(frame_results, columns=columns, show="headings")
tree.heading("Folder", text="Cartella")
tree.heading("Size", text="Dimensione")
tree.column("Folder", anchor="w", width=400)
tree.column("Size", anchor="e", width=100)
tree.pack(fill="both", expand=True, padx=10, pady=10)

btn_scan = ttk.Button(root, text="Scansiona Directory", command=start_scan)
btn_scan.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=400, mode="determinate")

show_disk_usage()

root.mainloop()
