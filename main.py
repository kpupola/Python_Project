
GRID_SIZE = 40
empty_grid = [[0]*GRID_SIZE]*GRID_SIZE

def print_grid(rezgis):
    #Izprintē režģi konsolē
    for rinda in rezgis:
        rinda_str = ''
        for burts in rinda:
            rinda_str = rinda_str + ' ' + str(burts)
        print(rinda_str)

def check_word_placement(vards, burta_indekss, rezga_indekss):
    #Atgriež True, ja vārdu ir atļaus ievietot tajā vietā
    return

def place_word(vards, burta_indekss, rezga_indekss):
    #Ievieto vārdu režģī noteiktā vietā
    return

def is_vertical(GRID_SIZE, row, col):
    if 0 <= row < len(GRID_SIZE) and 0 <= col < len(GRID_SIZE[0]):
        if row > 0 and GRID_SIZE[row - 1][col] != " ":
            return True
        if row < len(GRID_SIZE) - 1 and GRID_SIZE[row + 1][col] != " ":
            return True
    return False

def populate_grid(saraksts):
    #Ievieto dotā saraksta vārdus režģī
    return

def get_user_input():
    word_list = []
    while True:
        word = input("Ievadiet vārdu (vai 'viss', lai pabeigtu): ").strip().lower()
        if word == 'viss':
            break
    word_list.append(word)
    return word_list

def main():
    lietotaja_saraksts = get_user_input()
    populate_grid(lietotaja_saraksts)
    print_grid(empty_grid)

if __name__ == "__main__":
    main()
