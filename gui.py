import tkinter as tk 
from main import *
from handle_json import *


def start_screen():
    window = tk.Tk()
    window.minsize(500, 500)

    izveidot_miklu_poga = tk.Button(window, text="Izveidot jaunu krustvārdu mīklu")
    izveidot_miklu_poga.pack()

    risinat_miklas_poga = tk.Button(window, text="Risināt mīklas")
    risinat_miklas_poga.pack()
    
    window.mainloop()

start_screen()