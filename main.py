import random

GRID_SIZE = 40

def shuffle_words(saraksts):
    random.shuffle(saraksts)
    return saraksts

def shuffle_words(saraksts):
    random.shuffle(saraksts)
    return saraksts

def fill_grid(rezgis):
    #Atgriež aizpildītu režģi
    for rinda in rezgis:
        for kolonna in rezgis:
            indekss_str = ''
            for burts in [rinda][kolonna]:
                indekss_str = indekss_str + ' ' + str(burts)
    return rezgis

def print_grid(rezgis):
    #Izprintē režģi konsolē
    for rinda in rezgis:
        rinda_str = ''
        for burts in rinda:
            rinda_str = rinda_str + ' ' + str(burts)
        print(rinda_str)

def check_word_placement(vards_rezgi_vertikals, vards, burta_indekss, rezga_indekss):
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

def is_vertical(rezgis, row, col):
    if 0 <= row < len(rezgis) and 0 <= col < len(rezgis[0]):
        if row > 0 and rezgis[row - 1][col] != " ":
            return True
        if row < len(rezgis) - 1 and rezgis[row + 1][col] != " ":
            return True
    return False

def populate_grid(saraksts):
    #Ievieto dotā saraksta vārdus režģī, atgriež režģi
    rezgis = [[' '] * GRID_SIZE] * GRID_SIZE #sākumā tiek izveidots tukšs režģis
    for vards_index in range(len(saraksts)):
        vards=saraksts[vards_index]
        for burta_indekss, burts in enumerate(vards):
            for rinda in range(len(fill_grid(empty_grid))):
                for kolonna in range(len(empty_grid[0])):
                    if empty_grid[rinda][kolonna] == burts:
                        if is_vertical(empty_grid, rinda, kolonna):
                            vards_rezgi_vertikals=True
                        else:
                            vards_rezgi_vertikals=False
                            if check_word_placement(vards_rezgi_vertikals, vards, burta_indekss, empty_grid[rinda][kolonna]):
                                place_word(vards, burta_indekss, empty_grid[rinda][kolonna])
                                saraksts.pop(vards_index)
                                vards_index=0
    if not saraksts:
        print('Vardi izvietoti veiksmigi')
        return True
    else:
        return False 
    

def get_user_input():
    word_list = []
    while True:
        word = input("Ievadiet vārdu (vai 'viss', lai pabeigtu): ").strip().lower()
        if word == 'viss':
            break
    word_list.append(word)
    return word_list

def main():
    saraksts = get_user_input()
    lietotaja_saraksts = shuffle_words(saraksts)
    populate_grid(lietotaja_saraksts)
    #print_grid(empty_grid)
    
if __name__ == "__main__":
    main()
