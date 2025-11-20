import tkinter as tk
from tkinter import messagebox, filedialog
import math
import os
import csv
import json
import webbrowser

last_result = None

def add_symbol(symbol):
    entry.insert(tk.END, symbol)

def clear():
    entry.delete(0, tk.END)

def calculate():
    global last_result
    try:
        expression = entry.get().replace("√", "math.sqrt").replace("%", "/100").replace("Ans", str(last_result) if last_result is not None else "0")
        result = eval(expression)
        last_result = result
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
        history.insert(tk.END, f"{expression} = {result}")
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

def export_txt():
    file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file:
        with open(file, "w", encoding="utf-8") as f:
            for line in history.get(0, tk.END):
                f.write(line + "\n")
        messagebox.showinfo("TXT Export", f"Saved to file:\n{file}")

def export_csv():
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file:
        with open(file, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Expression", "Result"])
            for line in history.get(0, tk.END):
                if "=" in line:
                    expression, result = line.split("=", 1)
                    writer.writerow([expression.strip(), result.strip()])
        messagebox.showinfo("CSV Export", f"Saved to file:\n{file}")

def export_json():
    file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if file:
        data = []
        for line in history.get(0, tk.END):
            if "=" in line:
                expression, result = line.split("=", 1)
                data.append({"expression": expression.strip(), "result": result.strip()})
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("JSON Export", f"Saved to file:\n{file}")

def load_history():
    file = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file:
        history.delete(0, tk.END)
        with open(file, "r", encoding="utf-8") as f:
            for line in f:
                history.insert(tk.END, line.strip())
        messagebox.showinfo("History Loaded", f"Loaded from file:\n{file}")

def show_about():
    messagebox.showinfo("About", "                polsoft.ITS London\n\n                    Calculator v1.0\n\n   with history, export and Ans variable\n\n        2025© Sebastian Januchowski")

def open_github():
    webbrowser.open("https://github.com/seb07uk")

def open_chomik():
    webbrowser.open("https://chomikuj.pl/polsoft-its")

def handle_key(event):
    key = event.char
    if key in "0123456789.+-*/()%":
        add_symbol(key)
    elif key == "\r":
        calculate()
    elif key == "\x08":
        entry.delete(len(entry.get())-1, tk.END)

window = tk.Tk()
window.title("Calculator with History and Ans")
window.geometry("325x610")
window.configure(bg="#d6eaf8")

if os.path.exists("ikona.ico"):
    window.iconbitmap("ikona.ico")

menu = tk.Menu(window)
window.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Load History from TXT", command=load_history)
file_menu.add_command(label="Export to TXT", command=export_txt)
file_menu.add_command(label="Export to CSV", command=export_csv)
file_menu.add_command(label="Export to JSON", command=export_json)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)

polsoft_menu = tk.Menu(menu, tearoff=0)
polsoft_menu.add_command(label="GitHub", command=open_github)
polsoft_menu.add_command(label="Chomik", command=open_chomik)

help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(label="About", command=show_about)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="polsoft.ITS", menu=polsoft_menu)
menu.add_cascade(label="Help", menu=help_menu)

entry = tk.Entry(window, font=("Arial", 20), justify="right", bg="#ebf5fb", fg="#000000")
entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")

history = tk.Listbox(window, height=6, font=("Arial", 12), bg="#aed6f1")
history.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="we")

buttons = [
    ('(', 2, 0), (')', 2, 1), ('√', 2, 2), ('%', 2, 3),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
    ('0', 6, 0), ('.', 6, 1), ('+', 6, 2), ('=', 6, 3),
    ('Ans', 7, 0), ('C', 7, 1)
]

btn_color = "#85c1e9"
btn_calc = "#5dade2"
btn_clear = "#aed6f1"

for (text, row, col) in buttons:
    if text == '=':
        tk.Button(window, text=text, width=5, height=2, font=("Arial", 14), bg=btn_calc,
                  command=calculate).grid(row=row, column=col, padx=5, pady=5)
    elif text == 'C':
        tk.Button(window, text=text, width=11, height=2, font=("Arial", 14), bg=btn_clear,
                  command=clear).grid(row=row, column=col, columnspan=2, padx=5, pady=5)
    else:
        tk.Button(window, text=text, width=5, height=2, font=("Arial", 14), bg=btn_color,
                  command=lambda t=text: add_symbol(t)).grid(row=row, column=col, padx=5, pady=5)

window.bind("<Key>", handle_key)
window.mainloop()