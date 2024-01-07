import tkinter as tk 
from main import *
from handle_json import *

def generate_puzzle_view(parent_window, ievade):
    parent_window.destroy() # aizver iepriekšējo logu

    window = tk.Toplevel(root)
    window.minsize(500, 500)

    f = tk.Frame(window)
    f.pack()

    teksts = ievade.get("1.0", tk.END)
    vardnica = parse_input(teksts)

    #TODO: parāda izveidotu režģi un ir poga, ar kuru var uzģenerēt citus variantus
    window.mainloop()
    return

def create_puzzle_view():
    window = tk.Toplevel(root)
    window.minsize(500, 500)

    f = tk.Frame(window)
    f.pack()

    # user text input ar atbildēm un jautājumiem
    ievadi_vardus_label = tk.Label(f, text="Ievadi atbildes un jautājumus zemāk!\nIevadi atsevišķu atbildi un jautājumu jaunā rindiņā.\nFormāts: atbilde[atstarpe]jautājums")
    ievadi_vardus_label.grid(row=0, column=0)
    xscrollbar = tk.Scrollbar(f, orient="horizontal")
    xscrollbar.grid(row=2, column=0, sticky='NSEW')
    ievade = tk.Text(f, height=12, width=45, wrap="none", xscrollcommand=xscrollbar.set)
    ievade.grid(row=1, column=0)

    izveidot_poga = tk.Button(f, text="Izveidot mīklu", command=lambda: generate_puzzle_view(window))
    izveidot_poga.grid(row=3, column=0)

    window.mainloop()
    return

#funkcija, kas sadala lietotaja texta inputu vardnicā ar vārdiem kā keys un to values kā - numurs (sākumā nulle), jautājums
def parse_input(text):
    lines = text.split('\n')
    dictionary = {}
    for line in lines:
        space_index = line.find(' ')
        if space_index != -1:
            word = line[:space_index]
            question = line[space_index+1:]
            dictionary[word] = (0, 0, question)
    return dictionary

def choose_puzzle_view():
    window = tk.Toplevel(root)
    window.minsize(500, 500)

    f = tk.Frame(window)
    f.pack()

    # saraksts ar izveidotajām puzlēm, no kura vienu var izvēlēties
    izvelies_miklu = tk.Label(f, text="Izvēlies kādu no esošajām mīklām, ko risināt!")
    izvelies_miklu.grid(row=0, column=0)
    miklu_nosakumi = return_keys()
    for i in range(len(miklu_nosakumi)):
        b = tk.Button(f, text=miklu_nosakumi[i], command=lambda puzzle_key = miklu_nosakumi[i]: solve_puzzle_view(window, puzzle_key))
        b.grid(row=i + 1, column=0)
    window.mainloop()

def solve_puzzle_view(parent_window, puzzle_key):
    parent_window.destroy()
    window = tk.Toplevel(root)
    window.minsize(500, 500)

    f = tk.Frame(window)
    f.pack()

    title_label = tk.Label(f, text="Atrisināt mīklu " + puzzle_key)
    title_label.grid(row=0, column=0)

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