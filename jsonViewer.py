import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json

def open_file():
    """Open a JSON file and display its contents."""
    file_path = filedialog.askopenfilename(
        title="Open JSON File",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
    )

    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            display_json(data)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open file: {e}")

def display_json(data, parent=""):
    """Display JSON data in the tree view."""
    tree.delete(*tree.get_children())
    
    def insert_item(parent, key, value):
        if isinstance(value, dict):
            node = tree.insert(parent, "end", text=key, values=("object", ""))
            for k, v in value.items():
                insert_item(node, k, v)
        elif isinstance(value, list):
            node = tree.insert(parent, "end", text=key, values=("array", ""))
            for i, item in enumerate(value):
                insert_item(node, f"[{i}]", item)
        else:
            tree.insert(parent, "end", text=key, values=(type(value).__name__, value))

    for k, v in data.items():
        insert_item(parent, k, v)

def clear_view():
    """Clear the tree view."""
    tree.delete(*tree.get_children())

# Initialize the main window
root = tk.Tk()
root.title("JSON Viewer")
root.geometry("900x700")
root.minsize(800, 600)
root.configure(bg="#2e3b4e")

# Set custom styles
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                font=("Calibri", 12),
                rowheight=28,
                background="#1e1e2e",
                fieldbackground="#1e1e2e",
                foreground="#dcdcdc",
                borderwidth=0)
style.configure("Treeview.Heading",
                font=("Calibri", 14, "bold"),
                background="#4a90e2",
                foreground="white")
style.map("Treeview",
          background=[("selected", "#4a90e2")],
          foreground=[("selected", "white")])
style.configure("TButton",
                font=("Calibri", 12),
                padding=6,
                background="#4a90e2",
                foreground="white",
                borderwidth=0)
style.map("TButton",
          background=[("active", "#357ab8")])

# Create a frame for the tree view and scrollbar
frame = ttk.Frame(root, padding=10, style="TFrame")
frame.pack(fill=tk.BOTH, expand=True)

# Add a tree view
columns = ("Type", "Value")
tree = ttk.Treeview(frame, columns=columns, show="tree", style="Treeview")

# Configure column headers
tree.heading("#0", text="Key", anchor="w")
tree.heading("Type", text="Type", anchor="w")
tree.heading("Value", text="Value", anchor="w")
tree.column("#0", stretch=tk.YES, anchor="w")
tree.column("Type", width=150, anchor="w")
tree.column("Value", width=500, anchor="w")

# Add a vertical scrollbar
vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)

# Pack the tree view and scrollbar
vsb.pack(side=tk.RIGHT, fill=tk.Y)
tree.pack(fill=tk.BOTH, expand=True)

# Add buttons
button_frame = ttk.Frame(root, padding=10, style="TFrame")
button_frame.pack(fill=tk.X)

open_button = ttk.Button(button_frame, text="Open JSON", command=open_file)
open_button.pack(side=tk.LEFT, padx=10)

clear_button = ttk.Button(button_frame, text="Clear", command=clear_view)
clear_button.pack(side=tk.LEFT, padx=10)

exit_button = ttk.Button(button_frame, text="Exit", command=root.quit)
exit_button.pack(side=tk.RIGHT, padx=10)

# Start the main loop
root.mainloop()
