import tkinter as tk 
from main import *
from handle_json import *

def generate_puzzle_view():
    window = tk.Tk()
    window.minsize(500, 500)

    #TODO: parāda izveidotu režģi un ir poga, ar kuru var uzģenerēt citus variantus
    window.mainloop()
    return

def create_puzzle_view():
    window = tk.Tk()
    window.minsize(500, 500)

    #TODO: user text input ar atbildēm un jautājumiem
    window.mainloop()
    return

def choose_puzzle_view():
    window = tk.Tk()
    window.minsize(500, 500)

    #TODO: saraksts ar izveidotajām puzlēm, no kura vienu var izvēlēties
    window.mainloop()
    return

def solve_puzzle_view(puzzle_title):
    window = tk.Tk()
    window.minsize(500, 500)

    #TODO: režģis, kurā var ievadīt atbildes un tās pārbaudīt
    window.mainloop()
    return

def start_screen():
    window = tk.Tk()
    window.minsize(500, 500)

    izveidot_miklu_poga = tk.Button(window, text="Izveidot jaunu krustvārdu mīklu", command = create_puzzle_view)
    izveidot_miklu_poga.pack()

    risinat_miklas_poga = tk.Button(window, text="Risināt mīklas", command=choose_puzzle_view)
    risinat_miklas_poga.pack()

    window.mainloop()

start_screen()