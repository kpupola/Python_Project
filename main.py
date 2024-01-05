
GRID_SIZE = 40

def print_grid(rezgis):
    #Izprintē režģi konsolē
    for rinda in rezgis:
        rinda_str = ''
        for burts in rinda:
            rinda_str = rinda_str + ' ' + str(burts)
        print(rinda_str)

def check_word_placement(vards, burta_indekss, rezga_indekss):
    #Atgriež True, ja vārdu ir atļaus ievietot tajā vietā
    #Jāpārbauda, ka 
    # 1) vārds nepārsniedz režģa robežas
    # 2) vārds nepārklājas ar citu vārdu neatbilstošiem burtiem
    # 3) vārds neatrodas blakus citiem vārdiem paralēli

    vertikals = is_vertical(rezga_indekss)
    varda_garums = len(vards)
    check = True
    #vārda sākuma indeksa noteikšana
    if vertikals: 
        varda_sakums = [rezga_indekss[0] - burta_indekss, rezga_indekss[1]]
    else:
        varda_sakums = [rezga_indekss[0], rezga_indekss[1] - burta_indekss]
    
    # pārbauda, vai vārda garums neiziet ārpus režģa
    for i in range(varda_garums):
        if vertikals:
            if varda_sakums[0 + i] >= GRID_SIZE or varda_sakums[1 + i] >= GRID_SIZE:
                check = False
                break
    


    return check

def place_word(vards, burta_indekss, rezga_indekss):
    #Ievieto vārdu režģī noteiktā vietā
    return

def is_vertical(rezga_indekss):
    #Atgriež True, ja vārds režģī ir vertikāls
    #(Nav atrunāta situācija, ja iedotais indekss ir vārdu krustpunktam)
    return

def populate_grid(saraksts):
    #Ievieto dotā saraksta vārdus režģī, atgriež režģi
    rezgis = [[' '] * GRID_SIZE] * GRID_SIZE #sākumā tiek izveidots tukšs režģis
    return

def get_user_input():
    #Atgriež sarakstu ar lietotāja ievadītiem vārdiem
    return

def main():
    lietotaja_saraksts = get_user_input()
    print(populate_grid(lietotaja_saraksts))

if __name__ == "__main__":
    main()
