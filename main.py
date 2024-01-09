import tkinter as tk 
from grid_logic import *
from handle_json import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

# aizver Toplevel veida logu
def close_top(top):
    top.destroy()
    top.update()

#Funckija, kas pievieno mīklai nosaukumu un saglabā to
def get_title_and_save(parent_window, entries_array, miklas_nosaukums=''):

    check = True
    if not miklas_nosaukums:
    
        miklas_no_faila = return_keys()

        # pārbauda, vai lietotāja ievadītais nosaukums ir unikāls
        check = False
        while not check:
            miklas_nosaukums = simpledialog.askstring("Nosaukums", "Ievadiet mīklas nosaukumu:")
            if miklas_nosaukums == None:
                break
            if not miklas_nosaukums:
                messagebox.showerror("Tukša ievade", "Lūdzu ievadiet mīklas nosaukumu!")
            elif miklas_nosaukums in miklas_no_faila:
                messagebox.showerror("Slikts nosaukums", "Mīkla ar tādu nosaukumu jau eksistē!")
            else:
                messagebox.showinfo("Malacis!", "Mīkla veiksmīgi saglabāta!")
                check = True
    
    if miklas_nosaukums and check:
        save(miklas_nosaukums, entries_array)
        close_top(parent_window)
        return True
    else:
        return False

#Funkcija, kas lietotāja ievadītos vārdus saliek režģī
def generate_puzzle_view(parent_window, atbildes_un_jautajumi, miklas_nosaukums=''):
    close_top(parent_window) # aizver iepriekšējo logu

    window = tk.Toplevel(root)
    window.minsize(500, 500)

    f = tk.Frame(window, bg="#f3f4f6")  
    f.pack(padx=20, pady=20)  

    # f = tk.Frame(window)
    # f.pack()
    grid_box = tk.Text(f, width=60, height=40)

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
                grid_box.config(width=40, height=5, wrap="word", state="disabled", bg="#e0777e")
                break
    
    if return_values: # ja ir saņemts izdevies režģis
        grid = return_values[1]
        grid_box.insert("1.0", return_grid_string(grid)) 
        grid_box.config(state="disabled")

    grid_box.grid(row=0, column=0) # izvieto teksta lauku

    # Funkcija, kas ievieto teksta laukā dažādus variantus režģim
    def print_rezgis():
        grid_box.config(state="normal")
        grid_box.delete("1.0", tk.END)
        
        #izprintē variantu režģim no lietotāja ievadītajiem vārdiem
        saraksts = shuffle_keys(atbildes_un_jautajumi.copy()) 
        return_values = populate_grid(saraksts)

        while not return_values: # nodrošina, ka tiek izprintēti tikai režģi, kas ir izdevušies
            saraksts = shuffle_keys(atbildes_un_jautajumi.copy())
            return_values = populate_grid(saraksts)
        
        if return_values: # ja ir saņemts izdevies režģis
            grid = return_values[1]
            grid_box.insert("1.0", return_grid_string(grid))
            grid_box.config(state="disabled")
            grid_box.focus_set()
            grid_box.grid(row=0, column=0)
        else:
            grid_box.insert("1.0", "Nesanāca :(")
            grid_box.config(state="disabled")

    if return_values: # ja ir saņemts izdevies režģis
        # poga, ar kuru izsauc print_rezgis(), kas uzģenerēs citu izkārtojumu
        shuffle_poga = tk.Button(f, text="Izveidot citu izkārtojumu", command=print_rezgis)
        shuffle_poga.grid(row=1, column=0)

        # poga, ar kuru tiks saglabāts esošais variants režģim
        save_poga = tk.Button(f, text="Saglabāt", command=lambda: get_title_and_save(window, return_values[0], miklas_nosaukums))
        save_poga.grid(row=1, column=1) 
    else:
        # ja nav izdevies izveidot veiksmīgu režģi
        atpakal_poga = tk.Button(f, text="Atgriezties uz vārdu ievadi", command= lambda: create_puzzle_view(window))
        atpakal_poga.grid(row=1, column=0)

    close_poga = tk.Button(f, text="Aizvērt logu", command=lambda: close_top(window))
    close_poga.grid(row=2, column=0)
    window.mainloop()
    return

# Funkcija, kas apstrādā lietotāja ievadi
def get_input(ievade, parent_window, miklas_nosaukums=''):
    rezultats = parse_input(ievade)
    if rezultats[0] == True:
        close_top(parent_window)
        atbildes_un_jautajumi = rezultats[1]
        generate_puzzle_view(parent_window, atbildes_un_jautajumi, miklas_nosaukums)

#Funkcija, kas izveido skatu, kurā lietotājs ievada atbidles un jautājumus
def create_puzzle_view(parent_window=None):
    if parent_window:
        close_top(parent_window)
    window = tk.Toplevel(root)
    window.title('Krustvārdu mīklas izveide')
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
    ievade.focus_set()

    izveidot_poga = tk.Button(f, text="Izveidot mīklu", command=lambda: get_input(ievade.get("1.0", tk.END), window))
    izveidot_poga.grid(row=3, column=0)

    window.mainloop()

#Funkcija, kas pārbauda lietotāja ievadi un saliek to vārdnīcā
def parse_input(text):
    lines = text.split('\n')
    dictionary = {}
    for line in lines:
        space_index = line.find(' ')
        if space_index != -1:
            word = line[:space_index].strip()
            question = line[space_index+1:].strip()
            if len(word) < 2 or len(word) > GRID_SIZE:
                messagebox.showerror("Ievades kļūda", "Vārds '{}' nav atsbilstošā izmērā.".format(word))
                return False, ""
            if not word or not question:
                messagebox.showerror("Ievades kļūda", "Tukšs vārds vai jautājums.")
                return False, ""
            if word.isalpha():
                if dictionary and word in dictionary:
                    messagebox.showerror("Ievades kļūda",  "Vārds '{}' jau ir bijis ievietots mīklā divreiz.".format(word))
                    return False, ""
                else:
                    dictionary[word] = question
            else:
                messagebox.showerror("Kļūda", "Ievades kļūda: vārdā ir simboli, kas nav burti.")
                return False, ""
        elif line.strip():  
            messagebox.showerror("Kļūda", "Ievades kļūda: nav atstarpju starp vārdu un jautājumu.")
            return False, ""
    if not dictionary:
        messagebox.showerror("Kļūda", "Ievades kļūda: Nav ievadīts neviens vārds un jautājums.")
        return False, ""
    else:
        return True, dictionary
    
#Funkcija, kas attēlo konkrētās mīklas saturu ar opciju to atjaunot
def update_puzzle_view(parent_window, puzzle_key):
    close_top(parent_window)

    window = tk.Toplevel(root)
    window.minsize(500, 500)
    window.title('Krustvārdu mīklas rediģēšana')

    f = tk.Frame(window)
    f.pack()

    # user text input ar atbildēm un jautājumiem
    ievadi_vardus_label = tk.Label(f, text="Ievadi atbildes un jautājumus zemāk!\nIevadi atsevišķu atbildi un jautājumu jaunā rindiņā.\nFormāts: atbilde[atstarpe]jautājums")
    ievadi_vardus_label.grid(row=0, column=0)
    xscrollbar = tk.Scrollbar(f, orient="horizontal")
    xscrollbar.grid(row=2, column=0, sticky='NSEW')
    ievade = tk.Text(f, height=12, width=45, wrap="none", xscrollcommand=xscrollbar.set)

    # teksta lauciņā ievada esošo informāciju par mīklu
    atbildes_un_jautajumi = combine_dict(return_answers(puzzle_key), return_questions(puzzle_key))
    veca_mikla_str = ''
    for key, value in atbildes_un_jautajumi.items():
        veca_mikla_str += key + ' ' + value + '\n'
    ievade.insert("1.0", veca_mikla_str)
    ievade.grid(row=1, column=0)

    izveidot_poga = tk.Button(f, text="Saglabāt mīklu", command=lambda: get_input(ievade.get("1.0", tk.END), window, puzzle_key))
    izveidot_poga.grid(row=3, column=0)

    window.mainloop()
  

def choose_puzzle_view():
    window = tk.Toplevel(root)
    window.minsize(600, 500)
    window.title('Krustvārdu mīklu izvēle')
    window.configure(background='#E75480')

    f = ttk.Frame(window)
    f.pack(pady=50, padx=100, fill='both', expand=True)

    def refresh_frame():
        # atjauno skatu ar jaunāko info no faila
        for item in f.winfo_children():
            item.destroy()
        display_frame()

    def delete_puzzle_refresh(puzzle_key):
        # izdzēš konkrētu mīklu un atjauno skatu
        delete_puzzle(puzzle_key)
        refresh_frame()

    def clear_list():
        # izdzēš visu sarakstu un atjauno skatu
        clear_file()
        refresh_frame()


#Funkcija, kas atgriež sarakstu ar izveidotajām puzlēm, no kura vienu var izvēlēties
    def display_frame():
        style = ttk.Style(window)
        style.configure('TButton', font=('Arial', 14), padding=10, foreground='black', background='#C21807')
        style.configure('TLabel', font=('Arial', 18, 'bold'), padding=5, foreground='white', background='#E75480')
        style.configure('Pink.TButton', font=('Arial', 14,'bold'), padding=10, foreground='black', background='#E75480')
        style.configure('Red.TButton', font=('Arial', 14), padding=10, foreground='#8B0000', background='#E75480')

        izvelies_miklu = ttk.Label(f, text="Izvēlies kādu no esošajām mīklām, ko risināt!", style='TLabel')
        izvelies_miklu.grid(row=0, column=0, columnspan=5, pady=10)

        miklu_nosakumi = return_keys()
        for i in range(len(miklu_nosakumi)):
            def on_enter(event):
                event.widget.config(bg="white", fg="#E75480") 

            def on_leave(event):
                event.widget.config(bg="#E75480", fg="white")
            # poga, kas aizved uz mīklas risināšanas logu
            solve_but = ttk.Button(f, text=miklu_nosakumi[i].upper(), command=lambda puzzle_key = miklu_nosakumi[i]: solve_puzzle_view(window, puzzle_key), style='TButton')
            solve_but.grid(row=i + 2, column=1, pady=5, padx=10)

            if miklu_nosakumi[i] != "Izmēģinājuma mīkla":
                
                # poga, kas aizved uz mīklas rediģēšanas logu
                update_but = ttk.Button(f, text="Rediģēt mīklu", command=lambda puzzle_key = miklu_nosakumi[i]: update_puzzle_view(window, puzzle_key), style='TButton')
                update_but.grid(row=i + 2, column=4, pady=5, padx=10)
                update_but.configure(style='Red.TButton')

                # poga, kas izdzēš mīklu no saraksta
                delete_but = ttk.Button(f, text="Izdzēst mīklu", command=lambda puzzle_key = miklu_nosakumi[i]: delete_puzzle_refresh(puzzle_key), style='TButton')
                delete_but.grid(row=i + 2, column=2, pady=5, padx=10)
                delete_but.configure(style='Red.TButton')

        delete_all_but = ttk.Button(f, text="Izdzēst visas mīklas", command=clear_list, style='TButton')
        if len(miklu_nosakumi) == 1:
            delete_all_but.config(state="disabled")
        delete_all_but.grid(row=2, column=2, pady=10, columnspan=3)
        delete_all_but.configure(style='Pink.TButton')
    
    display_frame()

    window.mainloop()
    
    
#Funkcija, kas atver krustvārdu mīklas risināšanas skatu
def solve_puzzle_view(frame, puzzle_key):
    
    #Izsauc funkcijas, kas atgriež atbildes, jautājumus un funkcija, kas saliek kopā tos vārdnīcas formātā
    atbildes=return_answers(puzzle_key)
    jautajumi=return_questions(puzzle_key)
    vardnica=combine_dict(atbildes, jautajumi)
    grid=populate_grid(vardnica) 
    
    
    vardnica1 = grid[0]
    
    
    print(vardnica)
    if not grid:
        return

    frame = tk.Toplevel(root)
    frame.minsize(600, 500)
    f = tk.Frame(frame)
    frame.configure(background='#FFB5C5')
    frame.title('Krustvārdu mīklas risināšana')
    f.pack()
    
 #izveido krustvārdu mīklas režģi
    def create_window(grid, parent_frame):
        parent_frame.configure(background='#FFB5C5')
        entries = []
        for i, row in enumerate(grid):
            entry_row = []
            for j, value in enumerate(row):
                if value != ' ': #izveido ievades lauciņus, tur kur nav tukšums
                    if str(value).isnumeric():
                        index = tk.Text(parent_frame, width=3, height=1, borderwidth=1, relief="solid", font=('Arial', 10, 'bold'), cursor="arrow")
                        index.insert("1.1", value)
                        index.config(state="disabled", bg="#E75480")
                        index.tag_configure("center", justify="center")
                        index.tag_add("center", "1.0", "end")
                        index.grid(row=i, column=j)
                        entry_row.append('')
                    else:
                        entry = tk.Entry(parent_frame, width=3, borderwidth=1, relief="solid", font=('Arial', 12, 'bold'), justify="center")
                        entry.insert(0, '')  
                        entry.grid(row=i, column=j, padx=1, pady=1)
                        entry_row.append(entry)
                else:
                    entry_row.append('')
            entries.append(entry_row)
        return entries # Atgriež ievades lauciņu sarakstu

    #funkcija saglabās ievades vērtības un pārbauda vai tās sakrīt ar atbildēm
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
            result_label.config(text="Apsveicam! Tu atrisināji!", fg="white",font=('Arial', 15, 'bold'))           
        else:
            result_label.config(text="Nepareizi! Izlabo kļūdas!", fg="red",font=('Arial', 13))
            

#parāda atbildes
    def display_answers(entries, grid):
        for i, row in enumerate(grid):
            for j, value in enumerate(row):
                if value != ' ' and entries[i][j] != '':
                    entries[i][j].delete(0, tk.END)
                    entries[i][j].insert(0, value)
#notīra krustvārdu mīklas ievades vērtības, lai sāktu no jauna                 
    def try_again(entries, grid, result_label):
        result_label.config(text="") 
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
    submit_frame = tk.Frame(frame,bg="#FFB5C5")
    submit_frame.pack(pady=10)
    
    
    

    # Rezultāta etiķetes logs
    result_frame = tk.Frame(frame)
    result_frame.pack()

    # Rezultāta etiķete
    result_label = tk.Label(result_frame, text="", font=('Arial', 9, 'bold'),bg="#FFB5C5")
    result_label.pack()

    # Iesniegt poga
    submit_button = tk.Button(submit_frame, text="Pārbaudīt", bg="white", font=('Arial', 9, 'bold'), fg="#E75480", width=17,pady=3, command=lambda: submit_entries(entries, grid[1], result_label))
    submit_button.pack()

    # Parādīt atbildes poga logs
    answers_frame = tk.Frame(frame,bg="#FFB5C5")
    answers_frame.pack(pady=10)

    # Parādīt atbildes poga
    answers_button = tk.Button(answers_frame, text="Pareizās atbildes",bg="white",font=('Arial', 9, 'bold'), fg="#E75480",width=17,pady=3, command=lambda: display_answers(entries, grid[1]))
    answers_button.pack(pady=1)
    
    # Mēģināt vēlreiz poga
    again_button = tk.Button(answers_frame, text="Sākt no sākuma",bg="white",font=('Arial', 9, 'bold'), fg="#E75480",width=17,pady=3, command=lambda: try_again(entries, grid[1],result_label))
    again_button.pack(pady=1)     
    
    new_frame = tk.Frame(frame)
    new_frame.pack(pady=10)
    new_frame.configure(background='#E75480')

    # Jautājumu parādīšanas virsraksts
    new_label = tk.Label(new_frame, text="Jautājumi:", font=('Arial', 12, 'bold'),  fg="black", bg="#FFB5C5")
    new_label.pack()  
    
    
    # divi rāmji priekš jautājumu grupām
    bottom_labels_frame = tk.Frame(frame,bg="#FFB5C5")
    bottom_labels_frame.pack(side=tk.TOP, padx=10, pady=10)

    
    top_labels_frame = tk.Frame(frame,bg="#FFB5C5")
    top_labels_frame.pack(side=tk.TOP, padx=10, pady=10)
    
    #virsraksti
    nos_text1_label = tk.Label(bottom_labels_frame, text="Horizontāli", font=('Arial', 13, 'bold'),fg="black",  bg="#FFB5C5")
    nos_text1_label.pack()

    nos_text2_label = tk.Label(top_labels_frame, text="Vertikāli", font=('Arial', 13, 'bold'),fg="black",  bg="#FFB5C5")
    nos_text2_label.pack()
    #iedalījums horizontālajos un vertikālajos
    for item in vardnica1:
        
        label_text = f"{item['number']}{'.'} {item['question']}"
        if item['orientation'] == 0:
            
            left_label = tk.Label(bottom_labels_frame, text=label_text, font=('Arial', 10),fg="black",  bg="#FFB5C5")
            left_label.pack()
        if item['orientation'] == 1:
            
            right_label = tk.Label(top_labels_frame, text=label_text, font=('Arial', 10),fg="black",  bg="#FFB5C5")
            right_label.pack()

    frame.mainloop()
    return

root = tk.Tk()
def main():

    root.minsize(500, 500)
    root.title('Krustvārdu mīklas')
    root.configure(background='#E75480')

    style = ttk.Style(root)
    style.configure('TButton', font=('Arial', 14), padding=10, foreground='#A94064', corner_radius=10)
    style.configure('TLabel', font=('Arial', 20, 'bold'), padding=5, foreground='white', background='#E75480')
    style.configure('TFrame', background='#E75480')

    main_frame = ttk.Frame(root)
    main_frame.pack(pady=50, padx=100, fill='both', expand=True)

    title_label = ttk.Label(main_frame, text="Krustvārdu mīklas".upper(), style='TLabel')
    title_label.pack(pady=20)

    izveidot_miklu_poga = ttk.Button(main_frame, text="Izveidot jaunu krustvārdu mīklu", command=create_puzzle_view)
    izveidot_miklu_poga.pack(pady=10, padx=50, fill='x')

    risinat_miklas_poga = ttk.Button(main_frame, text="Mīklu saraksts", command=choose_puzzle_view)
    risinat_miklas_poga.pack(pady=10, padx=50, fill='x')

    root.mainloop()

if __name__ == "__main__":
    main()