import tkinter as tk
from tkinter import messagebox, filedialog
import math
import os
import csv
import json
import webbrowser

ostatni_wynik = None

def dodaj_znak(znak):
    pole.insert(tk.END, znak)

def wyczysc():
    pole.delete(0, tk.END)

def oblicz():
    global ostatni_wynik
    try:
        wyrazenie = pole.get().replace("√", "math.sqrt").replace("%", "/100").replace("Ans", str(ostatni_wynik) if ostatni_wynik is not None else "0")
        wynik = eval(wyrazenie)
        ostatni_wynik = wynik
        pole.delete(0, tk.END)
        pole.insert(0, str(wynik))
        historia.insert(tk.END, f"{wyrazenie} = {wynik}")
    except:
        pole.delete(0, tk.END)
        pole.insert(0, "Błąd")

def eksportuj_txt():
    plik = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")])
    if plik:
        with open(plik, "w", encoding="utf-8") as f:
            for linia in historia.get(0, tk.END):
                f.write(linia + "\n")
        messagebox.showinfo("Eksport TXT", f"Zapisano do pliku:\n{plik}")

def eksportuj_csv():
    plik = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Pliki CSV", "*.csv")])
    if plik:
        with open(plik, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Wyrażenie", "Wynik"])
            for linia in historia.get(0, tk.END):
                if "=" in linia:
                    wyrazenie, wynik = linia.split("=", 1)
                    writer.writerow([wyrazenie.strip(), wynik.strip()])
        messagebox.showinfo("Eksport CSV", f"Zapisano do pliku:\n{plik}")

def eksportuj_json():
    plik = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Pliki JSON", "*.json")])
    if plik:
        dane = []
        for linia in historia.get(0, tk.END):
            if "=" in linia:
                wyrazenie, wynik = linia.split("=", 1)
                dane.append({"wyrazenie": wyrazenie.strip(), "wynik": wynik.strip()})
        with open(plik, "w", encoding="utf-8") as f:
            json.dump(dane, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Eksport JSON", f"Zapisano do pliku:\n{plik}")

def wczytaj_historie():
    plik = filedialog.askopenfilename(filetypes=[("Pliki tekstowe", "*.txt")])
    if plik:
        historia.delete(0, tk.END)
        with open(plik, "r", encoding="utf-8") as f:
            for linia in f:
                historia.insert(tk.END, linia.strip())
        messagebox.showinfo("Wczytano historię", f"Załadowano z pliku:\n{plik}")

def pokaz_o_programie():
    messagebox.showinfo("O programie", "                    polsoft.ITS London\n\n                       Kalkulator  v1.0\n\n   z historią, eksportem i zmienną odpowiedzi\n\n             2025© Sebastian Januchowski")

def otworz_github():
    webbrowser.open("https://github.com/seb07uk")

def otworz_chomik():
    webbrowser.open("https://chomikuj.pl/polsoft-its")

def obsluz_klawisz(event):
    klawisz = event.char
    if klawisz in "0123456789.+-*/()%":
        dodaj_znak(klawisz)
    elif klawisz == "\r":
        oblicz()
    elif klawisz == "\x08":
        pole.delete(len(pole.get())-1, tk.END)

okno = tk.Tk()
okno.title("Kalkulator z historią i Ans")
okno.geometry("325x610")
okno.configure(bg="#d6eaf8")

if os.path.exists("ikona.ico"):
    okno.iconbitmap("ikona.ico")

menu = tk.Menu(okno)
okno.config(menu=menu)

menu_plik = tk.Menu(menu, tearoff=0)
menu_plik.add_command(label="Wczytaj historię z TXT", command=wczytaj_historie)
menu_plik.add_command(label="Eksportuj do TXT", command=eksportuj_txt)
menu_plik.add_command(label="Eksportuj do CSV", command=eksportuj_csv)
menu_plik.add_command(label="Eksportuj do JSON", command=eksportuj_json)
menu_plik.add_separator()
menu_plik.add_command(label="Zamknij", command=okno.quit)

menu_polsoft = tk.Menu(menu, tearoff=0)
menu_polsoft.add_command(label="GitHub", command=otworz_github)
menu_polsoft.add_command(label="Chomik", command=otworz_chomik)

menu_pomoc = tk.Menu(menu, tearoff=0)
menu_pomoc.add_command(label="O programie", command=pokaz_o_programie)

menu.add_cascade(label="Plik", menu=menu_plik)
menu.add_cascade(label="polsoft.ITS", menu=menu_polsoft)
menu.add_cascade(label="Pomoc", menu=menu_pomoc)

pole = tk.Entry(okno, font=("Arial", 20), justify="right", bg="#ebf5fb", fg="#000000")
pole.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")

historia = tk.Listbox(okno, height=6, font=("Arial", 12), bg="#aed6f1")
historia.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="we")

przyciski = [
    ('(', 2, 0), (')', 2, 1), ('√', 2, 2), ('%', 2, 3),
    ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
    ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
    ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
    ('0', 6, 0), ('.', 6, 1), ('+', 6, 2), ('=', 6, 3),
    ('Ans', 7, 0), ('C', 7, 1)
]

kolor_przycisku = "#85c1e9"
kolor_oblicz = "#5dade2"
kolor_wyczysc = "#aed6f1"

for (tekst, wiersz, kolumna) in przyciski:
    if tekst == '=':
        tk.Button(okno, text=tekst, width=5, height=2, font=("Arial", 14), bg=kolor_oblicz,
                  command=oblicz).grid(row=wiersz, column=kolumna, padx=5, pady=5)
    elif tekst == 'C':
        tk.Button(okno, text=tekst, width=11, height=2, font=("Arial", 14), bg=kolor_wyczysc,
                  command=wyczysc).grid(row=wiersz, column=kolumna, columnspan=2, padx=5, pady=5)
    else:
        tk.Button(okno, text=tekst, width=5, height=2, font=("Arial", 14), bg=kolor_przycisku,
                  command=lambda t=tekst: dodaj_znak(t)).grid(row=wiersz, column=kolumna, padx=5, pady=5)

okno.bind("<Key>", obsluz_klawisz)
okno.mainloop()