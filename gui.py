import tkinter as tk 
from main import *
from handle_json import *

def generate_puzzle_view():
    window = tk.Toplevel(root)
    window.minsize(500, 500)

    #TODO: parāda izveidotu režģi un ir poga, ar kuru var uzģenerēt citus variantus
    window.mainloop()
    return

def create_puzzle_view():
    window = tk.Toplevel(root)
    window.minsize(500, 500)

    #TODO: user text input ar atbildēm un jautājumiem
    ievadi_vardus_label = tk.Label(window, text="Ievadi atbildes un jautājumus zemāk!\nIevadi atsevišķu atbildi un jautājumu jaunā rindiņā.")
    ievade = tk.Entry(window)

    ievadi_vardus_label.pack()
    ievade.pack()
    #window.mainloop()
    return

def choose_puzzle_view():
    window = tk.Toplevel(root)
    window.minsize(500, 500)

    #TODO: saraksts ar izveidotajām puzlēm, no kura vienu var izvēlēties
    #window.mainloop()
    return

def solve_puzzle_view(puzzle_title):
    window = tk.Toplevel(root)
    window.minsize(500, 500)

    #TODO: režģis, kurā var ievadīt atbildes un tās pārbaudīt
    window.mainloop()
    return


root = tk.Tk()
root.minsize(500, 500)

izveidot_miklu_poga = tk.Button(root, text="Izveidot jaunu krustvārdu mīklu", command=create_puzzle_view)
izveidot_miklu_poga.pack()

risinat_miklas_poga = tk.Button(root, text="Risināt mīklas", command=choose_puzzle_view)
risinat_miklas_poga.pack()

root.mainloop()