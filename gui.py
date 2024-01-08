import tkinter as tk 
from main import *
from handle_json import *
from tkinter import messagebox

def close_top(top):
    top.destroy()
    top.update()

def generate_puzzle_view(parent_window, atbildes_un_jautajumi):
    #parent_window.destroy() # aizver iepriekšējo logu

    window = tk.Toplevel(root)
    window.minsize(500, 500)

    f = tk.Frame(window)
    f.pack()
    grid_box = tk.Text(f, width=60, height=30)

    #izprintē pirmo variantu režģim no lietotāja ievadītajiem vārdiem
    saraksts = shuffle_keys(atbildes_un_jautajumi.copy()) 
    return_values = populate_grid(saraksts)
    #cikls, kas nodrošina, ka tik attēloti tikai režģi, kas ir izdevušies
    fail_count = 0
    while not return_values:
            saraksts = shuffle_keys(atbildes_un_jautajumi.copy())
            return_values = populate_grid(saraksts)
            fail_count += 1
            if fail_count == 30:
                grid_box.insert("1.0", "Ar šo vārdu sarakstu nav izdevies izveidot režģi, mēģini ievadīt citus vārdus.")
                break
    
    if return_values:
        grid = return_values[1]
        grid_box.insert("1.0", return_grid_string(grid))
        grid_box.config(state="disabled")

    grid_box.grid(row=0, column=0)
    def print_rezgis():

        grid_box.config(state="normal")
        grid_box.delete("1.0", tk.END)
        
        #izprintē variantu režģim no lietotāja ievadītajiem vārdiem
        saraksts = shuffle_keys(atbildes_un_jautajumi.copy()) 
        return_values = populate_grid(saraksts)

        while not return_values:
            saraksts = shuffle_keys(atbildes_un_jautajumi.copy())
            return_values = populate_grid(saraksts)
        
        if return_values:
            grid = return_values[1]
            grid_box.insert("1.0", return_grid_string(grid))
            grid_box.config(state="disabled")
            grid_box.grid(row=0, column=0)
        else:
            grid_box.insert("1.0", "Nesanāca :(")
            grid_box.config(state="disabled")

    if return_values: 
        shuffle_poga = tk.Button(f, text="Izveidot citu izkārtojumu", command=print_rezgis)
        shuffle_poga.grid(row=1, column=0)
        
        save_poga = tk.Button(f, text="Saglabāt", command=lambda: save(return_values[0]))
        save_poga.grid(row=1, column=1) 
    else:
        atpakal_poga = tk.Button(f, text="Atgriezties uz vārdu ievadi", command=lambda: close_top(window))
        atpakal_poga.grid(row=1, column=0)

    window.mainloop()
    return

def get_input(ievade, parent_window):
    rezultats = parse_input(ievade)
    if rezultats[0] == True:
        atbildes_un_jautajumi = rezultats[1]
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

#funkcija, kas sadala lietotaja texta inputu vardnicā ar vārdiem kā keys un to values kā - numurs (sākumā nulle), jautājums
def parse_input(text):
    lines = text.split('\n')
    dictionary = {}
    for line in lines:
        space_index = line.find(' ')
        if space_index != -1:
            word = line[:space_index].strip()
            question = line[space_index+1:].strip()
            if word.isalpha() and question.isalpha():
                if word and question:
                    if dictionary and word in dictionary:
                        messagebox.showerror("Ievades kļūda",  "Vārds '{}' jau ir bijis ievietots mīklā divreiz.".format(word))
                        return False, ""
                    else:
                        dictionary[word] = (0, question)
                else:
                    messagebox.showerror("Ievades kļūda", "Tukšs vārds vai jautājums.")
                    return False, ""
            else:
                messagebox.showerror("Kļūda", "Ievades kļūda: vārdā vai jautājumā ir simboli, kas nav burti.")
                return False, ""
        elif line.strip():  #pārbauda, vai starp vārdu un jautājumu ir atstarpe
            messagebox.showerror("Kļūda", "Ievades kļūda: nav atstarpju starp vārdu un jautājumu.")
            return False, ""

    return True, dictionary

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
 
#izsauc funkcijas, kas atgriež atbildes, jautājumus un funkcija, kas saliek kopā tos vārdnīcas formātā
    atbildes=return_answers(puzzle_key)
    jautajumi=return_questions(puzzle_key)
    vardnica=combine_dict(atbildes, jautajumi)
    grid=populate_grid(vardnica) 
    
    vardnica1 = grid[0]
    
    print(vardnica1)
    print(vardnica)
    if not grid:
        return

    frame = tk.Toplevel(root)
    f = tk.Frame(frame)
    f.pack()
    
 #izveido krustvārdu mīklas režģi
    def create_window(grid, parent_frame):
        entries = []

        for i, row in enumerate(grid):
            entry_row = []
            for j, value in enumerate(row):
                if value != ' ': #izveido ievades lauciņus, tur kur nav tukšums
                    if str(value).isnumeric():
                        index = tk.Text(parent_frame, width=3, height=1, borderwidth=1, relief="solid", font=('Helvetica', 10, 'bold'), cursor="arrow")
                        index.insert("1.1", value)
                        index.config(state="disabled", bg="#ffff99")
                        index.grid(row=i, column=j)
                        entry_row.append('')
                    else:
                        entry = tk.Entry(parent_frame, width=3, borderwidth=1, relief="solid", font=('Helvetica', 12, 'bold'), justify="center")
                        entry.insert(0, '')  
                        entry.grid(row=i, column=j, padx=1, pady=1)
                        entry_row.append(entry)
                else:
                    entry_row.append('')
            entries.append(entry_row)

        return entries # Atgriež ievades lauciņu sarakstu

    def submit_entries(entries, grid, result_label):
        # Atiestata ievadē esošo fona krāsu
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != ' ' and entries[i][j] != '':
                    entries[i][j].config(bg="white")
        # saglabā ievades vērtības
        entered_values = []
        for i, row in enumerate(grid):
            entered_row = []
            for j, value in enumerate(row):
                if value != ' ' and entries[i][j] != '':
                    entered_value = entries[i][j].get()
                    entered_row.append(entered_value)
                else:
                    entered_row.append('')
            entered_values.append(entered_row)
        #ja ir nepareizi, iekrāso sarkanu
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != ' ' and entered_values[i][j] != value and entries[i][j] != '':
                    entries[i][j].config(bg="red")

        # pārbauda vai ir pareizi un uzvarēšanas paziņojums
        if all(value == entered_values[i][j] for i, row in enumerate(grid) for j, value in enumerate(row) if value != ' ' and entries[i][j] != ''):
            result_label.config(text="Congratulations! You win!", fg="red")
        else:
            result_label.config(text="Incorrect input! Try again.", fg="red")

    
#parāda atbildes
    def display_answers(entries, grid):
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != ' ' and entries[i][j] != '':
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, value)
#notīra krustvārdu mīklas ievades vērtības, lai sāktu no jauna                 
    def try_again(entries, grid):
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != ' ' and entries[i][j] != '':
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, '')


   
    # Krustvārdu mīklas režģa logs
    crossword_frame = tk.Frame(frame)
    crossword_frame.pack(pady=10)
    

    entries = create_window(grid[1], crossword_frame)
        
    # Iesniegt pogas logs
    submit_frame = tk.Frame(frame)
    submit_frame.pack(pady=10)

    # Rezultāta etiķetes logs
    result_frame = tk.Frame(frame)
    result_frame.pack()

    # Rezultāta etiķete
    result_label = tk.Label(result_frame, text="", font=('Helvetica', 12, 'bold'))
    result_label.pack()

    # Iesniegt poga
    submit_button = tk.Button(submit_frame, text="Check", command=lambda: submit_entries(entries, grid[1], result_label))
    submit_button.pack()

    # Parādīt atbildes poga logs
    answers_frame = tk.Frame(frame)
    answers_frame.pack(pady=10)

    # Parādīt atbildes poga
    answers_button = tk.Button(answers_frame, text="Display Answers", command=lambda: display_answers(entries, grid[1]))
    answers_button.pack()
    
    # Mēģināt vēlreiz poga
    again_button = tk.Button(answers_frame, text="Try again", command=lambda: try_again(entries, grid[1]))
    again_button.pack()     
    
    new_frame = tk.Frame(frame)
    new_frame.pack(pady=10)

    # Jautājumu parādīšanas virsraksts
    new_label = tk.Label(new_frame, text="Jautājumi")
    new_label.pack()  
    
    # divi rāmji priekš jautājumu grupām
    bottom_labels_frame = tk.Frame(frame)
    bottom_labels_frame.pack(side=tk.TOP, padx=10, pady=10)

    
    top_labels_frame = tk.Frame(frame)
    top_labels_frame.pack(side=tk.TOP, padx=10, pady=10)
    
    #virsraksti
    nos_text1_label = tk.Label(bottom_labels_frame, text="Horizontāli", font=('Helvetica', 11, 'bold'))
    nos_text1_label.pack()

    nos_text2_label = tk.Label(top_labels_frame, text="Vertikāli", font=('Helvetica', 11, 'bold'))
    nos_text2_label.pack()
    #iedalījums horizontālajos un vertikālajos
    for item in vardnica1:
        
        label_text = f"{item['number']}{'.'} {item['question']}"
        if item['orientation'] == 0:
            
            left_label = tk.Label(bottom_labels_frame, text=label_text, font=('Helvetica', 10))
            left_label.pack()
        if item['orientation'] == 1:
            
            right_label = tk.Label(top_labels_frame, text=label_text, font=('Helvetica', 10))
            right_label.pack()

            
      

    frame.mainloop()
    return


root = tk.Tk()
root.minsize(500, 500)

izveidot_miklu_poga = tk.Button(root, text="Izveidot jaunu krustvārdu mīklu", command=create_puzzle_view)
izveidot_miklu_poga.pack()

risinat_miklas_poga = tk.Button(root, text="Risināt mīklas", command=choose_puzzle_view)
risinat_miklas_poga.pack()

root.mainloop()