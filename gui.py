import tkinter as tk 
from main import *
from handle_json import *

def generate_puzzle_view(parent_window, atbildes_un_jautajumi):
    parent_window.destroy() # aizver iepriekšējo logu

    window = tk.Toplevel(root)
    window.minsize(500, 500)

    f = tk.Frame(window)
    f.pack()
    
    saraksts = shuffle_keys(atbildes_un_jautajumi.copy()) 
    return_values = populate_grid(saraksts)
    grid_box = tk.Text(f)
    if return_values:
        grid = return_values[1]
        grid_box.insert("1.0", return_grid_string(grid))
        print(return_grid_string(grid))
        grid_box.grid(row=0, column=0)
    else:
        grid_box.inser("1.0", "Nesanāca :(")
     
     
    #TODO: parāda izveidotu režģi un ir poga, ar kuru var uzģenerēt citus variantus
    window.mainloop()
    return

def get_input(ievade, parent_window):
    atbildes_un_jautajumi = parse_input(ievade)
    generate_puzzle_view(parent_window, atbildes_un_jautajumi)
    
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

    # TODO: funkcija, kas ievadi pārvērš sarakstā ar vārdnīcām

    izveidot_poga = tk.Button(f, text="Izveidot mīklu", command=lambda: get_input(ievade.get("1.0", tk.END), window))
    izveidot_poga.grid(row=3, column=0)

    
    window.mainloop()
    return

def parse_input(text):
    lines = text.split('\n')
    dictionary = {}
    for line in lines:
        space_index = line.find(' ')
        if space_index != -1:
            word = line[:space_index]
            question = line[space_index+1:]
            dictionary[word] = (0, question)
    return dictionary
#funkcija, kas sadala lietotaja texta inputu vardnicā ar vārdiem kā keys un to values kā - numurs (sākumā nulle), jautājums


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

def solve_puzzle_view(frame, puzzle_key):
    #    parent_window.destroy()
     #   window = tk.Toplevel(root)
      #  window.minsize(500, 500)
#  #   

    atbildes=return_answers(puzzle_key)
    jautajumi=return_questions(puzzle_key)
    vardnica=combine_dict(atbildes, jautajumi)
    grid=populate_grid(vardnica)
    
    print(vardnica)
    
    if not grid:
        return

    frame = tk.Toplevel(root)
    f = tk.Frame(frame)
    f.pack()
    
    
       
    
    
#return display_filled_windows(grid)
#    title_label = tk.Label(f, text="Atrisināt mīklu " + puzzle_key)
#       title_label.grid(row=0, column=0)
    
    #def create_window(grid, parent_window):

    def create_window(grid, parent_frame):
        entries = []

        for i, row in enumerate(grid):
            entry_row = []
            for j, value in enumerate(row):
                if value != ' ':
                    entry = tk.Entry(parent_frame, width=3, borderwidth=1, relief="solid", font=('Helvetica', 12, 'bold'), justify="center")
                    entry.insert(0, '')  # Insert the letter into the entry
                    entry.grid(row=i, column=j, padx=1, pady=1)
                    entry_row.append(entry)
                else:
                    entry_row.append('')
            entries.append(entry_row)

        return entries

    def submit_entries(entries, grid, result_label):
        # Reset background color
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != ' ':
                    entries[i][j].config(bg="white")

        entered_values = []
        for i, row in enumerate(grid):
            entered_row = []
            for j, value in enumerate(row):
                if value != ' ':
                    entered_value = entries[i][j].get()
                    entered_row.append(entered_value)
                else:
                    entered_row.append('')
            entered_values.append(entered_row)

        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != ' ' and entered_values[i][j] != value:
                    entries[i][j].config(bg="red")

        # Check for win
        if all(value == entered_values[i][j] for i, row in enumerate(grid) for j, value in enumerate(row) if value != ' '):
            result_label.config(text="Congratulations! You win!", fg="red")
        else:
            result_label.config(text="Incorrect input! Try again.", fg="red")

    

    def display_answers(entries, grid):
        for i, row in enumerate(grid):
            #entry_row = []
            for j, value in enumerate(row):
                if value != ' ':
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, value)
                    
    def try_again(entries, grid):
        for i, row in enumerate(grid):
            #entry_row = []
            for j, value in enumerate(row):
                if value != ' ':
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, '')
        
    # Crossword grid frame
    crossword_frame = tk.Frame(frame)
    crossword_frame.pack(pady=10)

    entries = create_window(grid[1], crossword_frame)

    # Submit button frame
    submit_frame = tk.Frame(frame)
    submit_frame.pack(pady=10)

    # Result label frame
    result_frame = tk.Frame(frame)
    result_frame.pack()

    # Result label
    result_label = tk.Label(result_frame, text="", font=('Helvetica', 12, 'bold'))
    result_label.pack()

    # Submit button
    submit_button = tk.Button(submit_frame, text="Check", command=lambda: submit_entries(entries, grid[1], result_label))
    submit_button.pack()

    # Display answers button frame
    answers_frame = tk.Frame(frame)
    answers_frame.pack(pady=10)

    # Display answers button
    answers_button = tk.Button(answers_frame, text="Display Answers", command=lambda: display_answers(entries, grid[1]))
    answers_button.pack()
    
    # Display answers button
    again_button = tk.Button(answers_frame, text="Try again", command=lambda: try_again(entries, grid[1]))
    again_button.pack()

                    
    
                    
    #TODO: režģis, kurā var ievadīt atbildes un tās pārbaudīt
    #window.mainloop()
    
    frame.mainloop()
    return


root = tk.Tk()
root.minsize(500, 500)

izveidot_miklu_poga = tk.Button(root, text="Izveidot jaunu krustvārdu mīklu", command=create_puzzle_view)
izveidot_miklu_poga.pack()

risinat_miklas_poga = tk.Button(root, text="Risināt mīklas", command=choose_puzzle_view)
risinat_miklas_poga.pack()

root.mainloop()