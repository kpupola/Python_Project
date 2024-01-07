from handle_json import *

import random

GRID_SIZE = 60

# Funkcija, kas randomizē dic pēc vārda un attiecigi piekarto jaut tam blakus (pareizo)
def shuffle_keys(saraksts):

    keys = list(saraksts.keys()) #panem no vardnicas atslegas
    random.shuffle(keys) #samaisa taas
    
    # Create a new dictionary with shuffled keys
    shuffled_dict = {} #jauna vardnica shufflotajam
    for key in keys: 
        shuffled_dict[key] = saraksts[key]
    
    return shuffled_dict

def print_grid(rezgis):
    #Izprintē režģi konsolē
    for rinda in rezgis:
        for kolonna in rinda:
            print(kolonna, end=" ")
        print()

# Funkcijas check_word_placement() parametri ir:
    # rezgis – divdimensionāls masīvs, kurš satur vārdus un ' ' tur, kur nav vārdu
    # vards – vārds, ko vēlas ielikt režģī
    # burta_indekss – burta indekss vārdā (vards), kurš sakrīt ar burtu režģī
    # rinda – rindas indekss burtam režģī, kurš sakrīt ar vards[burta_indekss]
    # kolonna – kolonnas indekss burtam režģī, kurš sakrīt ar vards[burta_indekss]
    #
    # Atgriež True, ja vārdu ir atļaus ievietot tajā vietā
    # Jāpārbauda, ka 
    # 1) vārds nepārsniedz režģa robežas
    # 2) vārds nepārklājas ar citu vārdu neatbilstošiem burtiem
    # 3) vārds neatrodas blakus citiem vārdiem paralēli
    # 4) vārdam sākumā vai beigās nav cits vārds
def check_word_placement(rezgis, vards, burta_indekss, rinda, kolonna):

    #pārbauda, vai izvēlētais burts nav kāda krustpunktā
    if (rinda + 1) < GRID_SIZE and (kolonna + 1) < GRID_SIZE:
        if (rezgis[rinda + 1][kolonna] != ' ' and rezgis[rinda][kolonna + 1] != ' ') or (rezgis[rinda + 1][kolonna] != ' ' and rezgis[rinda][kolonna + 1] != ' '):
            return False

    vertikals = is_vertical(rezgis, rinda, kolonna) #norāda virzienu vārdam, ar kuru krustosies
    varda_garums = len(vards)
    check = True
    #vārda sākuma indeksa noteikšana
    if not vertikals: # vārdu, kuru liksim režģī, jāliek perpendikulāri tam, ar ko krustosies
        varda_sakums_rinda = rinda - burta_indekss
        varda_sakums_kolonna = kolonna
    else:
        varda_sakums_rinda = rinda
        varda_sakums_kolonna = kolonna - burta_indekss
        
    # pārbauda, vai vārda garums neiziet ārpus režģa
    for i in range(varda_garums):
        if not vertikals:
            if varda_sakums_rinda + i >= GRID_SIZE: #iziet cauri x jeb rindu indeksiem uz leju
                #print("vārds iet pāri robežai uz leju") #pagaidām testēšanas nolūkiem izprintē, kur rodas kļūda
                check = False
                break
        else:
            if varda_sakums_kolonna + i >= GRID_SIZE: #iziet cauri y jeb kolonnu indeksiem pa labi
                #print("vārds iet pāri robežai pa labi")
                check = False
                break
    
    #pārbauda, vai vārds nepārklājas nelegāli ar citiem vārdiem
    for i in range(varda_garums):
        if not vertikals:
            if (varda_sakums_rinda + i) <= GRID_SIZE:
                if rezgis[varda_sakums_rinda + i][varda_sakums_kolonna] != ' ' and rezgis[varda_sakums_rinda + i][varda_sakums_kolonna] != vards[i]:
                    #print("vārds nelegāli pārklājas vertikāli")
                    check = False
                    break
        else:
            if (varda_sakums_kolonna + i) <= GRID_SIZE:
                if rezgis[varda_sakums_rinda][varda_sakums_kolonna + i] != ' ' and rezgis[varda_sakums_rinda][varda_sakums_kolonna + i] != vards[i]:
                    #print("vārds nelegāli pārklājas horizontāli")
                    check = False
                    break
    
    #pārbauda, vai vārdam sākumā vai beigās nav cita vārda        
    if not vertikals:
            #pārbauda vārdu no augšas
            if varda_sakums_rinda > 0: #pārbauda, vai vārds nav režģa augšējā malā
                if rezgis[varda_sakums_rinda - 1][varda_sakums_kolonna] !=' ':
                    check=False

            #pārbauda vārdu no apakšas
            varda_beigu_rinda=varda_sakums_rinda + varda_garums - 1
            if varda_beigu_rinda + 1 < GRID_SIZE: #pārbauda, vai vārds nav režģa apakšējā malā
                if rezgis[varda_beigu_rinda + 1][varda_sakums_kolonna] !=' ':
                    check=False
    else:
            #pārbauda vārdu no kreisās puses
            if varda_sakums_kolonna > 0: #pārbauda, vai vārds nav režģa kreisajā malā
                if rezgis[varda_sakums_rinda][varda_sakums_kolonna - 1] != ' ':
                    check=False

            #pārbauda vārdu no labās puses
            varda_beigu_kolonna=varda_sakums_kolonna + varda_garums - 1
            if varda_beigu_kolonna + 1 < GRID_SIZE: #pārbauda, vai vārds nav režģa labajā malā
                if rezgis[varda_sakums_rinda][varda_beigu_kolonna + 1] != ' ':
                    check=False
    
    #pārbauda, vai vārds neatrodas blakus citiem vārdiem 
    for i in range(varda_garums):
        if not vertikals:
            #pārbauda vārdu no kreisās puses
            if varda_sakums_kolonna > 0: #pārbauda, vai vārds nav režģa kreisajā malā
                if rezgis[varda_sakums_rinda + i][varda_sakums_kolonna - 1] != ' ' and burta_indekss != i:
                    #print("vārdam kreisajā pusē ir cits vārds")
                    check = False
                    break
            #pārbauda vārdu no labās puses
            if varda_sakums_kolonna + 1< GRID_SIZE: #pārbauda, vai vārds nav režģa labajā malā
                if rezgis[varda_sakums_rinda + i][varda_sakums_kolonna + 1] != ' ' and burta_indekss != i:
                    #print("vārdam labajā pusē ir cits vārds")
                    check = False
                    break
        else:
            #pārbauda vārdu no augšas
            if varda_sakums_rinda > 0: #pārbauda, vai vārds nav režģa augšējā malā
                if rezgis[varda_sakums_rinda - 1][varda_sakums_kolonna + i] != ' ' and burta_indekss != i:
                    #print("vārdam augšējā pusē ir cits vārds")
                    check = False
                    break
            #pārbauda vārdu no apakšas
            if varda_sakums_rinda + 1< GRID_SIZE: #pārbauda, vai vārds nav režģa apakšējā malā
                if rezgis[varda_sakums_rinda + 1][varda_sakums_kolonna + i] != ' ' and burta_indekss != i:
                    #print("vārdam apaksējā pusē ir cits vārds")
                    check = False
                    break

    return check

# Funkcijas place_word() parametri:
    # rezgis – divdimensionāls masīvs, kurš satur vārdus un ' ' tur, kur nav vārdu
    # vards – vārds, ko vēlas ielikt režģī
    # burta_indekss – burta indekss vārdā (vards), kurš sakrīt ar burtu režģī
    # rinda – rindas indekss burtam režģī, kurš sakrīt ar vards[burta_indekss]
    # kolonna – kolonnas indekss burtam režģī, kurš sakrīt ar vards[burta_indekss]
    #
    #Ievieto vārdu režģī noteiktā vietā
def place_word(rezgis, vards, burta_indekss, rinda, kolonna):

    if is_vertical(rezgis, rinda, kolonna):
        for i in range(len(vards)):
            rezgis[rinda][kolonna - burta_indekss + i] = vards[i]
    else:
        for i in range(len(vards)):
            rezgis[rinda - burta_indekss + i][kolonna] = vards[i]
    return

# Funkcijas is_vertical() parametri:
    # rezgis – divdimensionāls masīvs, kurš satur vārdus un ' ' tur, kur nav vārdu
    # rinda – rindas indekss burtam režģī, kurš ir daļa no vārda
    # kolonna – kolonnas indekss burtam režģī, kurš ir daļa no vārda
    #
    # Atgriež True, ja vārds ir vertikāls; False, ja horizontāls
def is_vertical(rezgis, row, col):
    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
        if col != 0:
            if rezgis[row][col - 1] == " " and rezgis[row][col + 1] == " ":
                return True
    return False

#pārveido vārdnīcu vajadzīgajā formā
def alter_dict(vardnica2):
    izmainita_vardnica = []

    for word, (number, question, orientation) in vardnica2.items():
        izmainita_vardnica.append({
            "number": number,
            "orientation": orientation,
            "answer": word,
            "question": question
        })

    return izmainita_vardnica

def populate_grid(saraksts):

    vards_jautajums2 = {}
    varda_nr = 1

    #Ievieto dotā saraksta vārdus režģī, atgriež režģi
    rezgis = [[' ' for i in range(GRID_SIZE)] for j in range(GRID_SIZE)] #sākumā tiek izveidots tukšs režģis
    #Nosaka pirmo vārdu no vardnicas kā key 
    pirmais_vards = next(iter(saraksts.keys()))
    #Ievieto pirmo vārdu režģī
    place_word(rezgis, pirmais_vards, 0, 10, 10)
    #Nomaina pirmā vārda numuru uz 1
    saraksts[pirmais_vards] = (varda_nr, saraksts[pirmais_vards][1], 0)
    #Pievieno pirmo ierakstu jaunas otrajam dictionarijam
    vards_jautajums2 = {pirmais_vards: saraksts[pirmais_vards]}
    # Izdzēš pirmo saraksta vārdnīcas ierakstu
    saraksts.pop(next(iter(saraksts.keys()), None), None)
    
    vards_index = 0
    varda_nr = 2
    vardu_saraksts = list(saraksts.keys()) #vārdus, kas glabati kā keys, pārveido par vārdu sarakstu
    while vards_index < len(vardu_saraksts): # ejam cauri sarakstam 
          vards_ielikts = False
          vards = vardu_saraksts[vards_index]
          for burta_indekss, burts in enumerate(vards): # ejam cauri vārdam
              for rinda in range(GRID_SIZE):
                  for kolonna in range(GRID_SIZE):
                      if rezgis[rinda][kolonna] == burts:
                          if check_word_placement(rezgis, vards, burta_indekss, rinda, kolonna):
                              if is_vertical(rezgis, rinda, kolonna):
                                  orientation = 0
                              else:
                                  orientation = 1
                              place_word(rezgis, vards, burta_indekss, rinda, kolonna)
                              vards_jautajums2[vards] = saraksts[vards] #pievieno otrajai vardnicai ierakstu, kas bāzēta uz konkrēto vārdu
                              vards_jautajums2[vards] = (varda_nr, vards_jautajums2[vards][1], orientation) #nomaina ieraksta numuru uz vārda numuru
                              varda_nr += 1
                              del saraksts[vards] #izdzēšs no pirmās vārdnīcas ierakstu, kas satur vārdu
                              vardu_saraksts.pop(vards_index) #izdzēš vārdu no vardu_saraksts
                              vards_index = vards_index - 1
                              vards_ielikts = True
                              break
                      if vards_ielikts:
                          break
                  if vards_ielikts:
                      break
              if vards_ielikts:
                  break
          vards_index += 1

    if not saraksts: #ja izdodas izveidot režģi
         vardnica = alter_dict(vards_jautajums2)
         print('Vardi izvietoti veiksmigi')
         return (vardnica, rezgis)
    else:
        print('Nesanāca izveidot režģi')
        return False 
    

def varda_parbaude(vards):
    if len(vards)<= 2 or len(vards) > GRID_SIZE:
        return False
    else:
        return True

def get_user_input():

    vards_jautajums = {}
    while True:
        word = input("Ievadiet vārdu (vai 'viss', lai pabeigtu): ").strip().lower()
        if word == 'viss':
            break
        question = input ("Ievadiet vārdam atbilstošo jautājumu: ").strip().lower()
        # Check if the key already exists in the dictionary
        if vards_jautajums and word in vards_jautajums:
                print("Vārds {} jau ir bijis ievietots mīklā. Lūdzu ievadiet citu vārdu!".format(word))
        else:
            if varda_parbaude(word) == False:
                print("Vārds {} nav atbilstošā izmērā. Lūdzu ievadiet citu vārdu!".format(word))
            else:
                vards_jautajums[word] = (0, question, 0) # (nr pec kartas, jautajums, orientacija (0-horizontals, 1-vertikals))
    return vards_jautajums

def main():
    lietotaja_saraksts = get_user_input()
    if not lietotaja_saraksts:
           print('Saraksts ir tukss, ievadiet kadu vardu!')
    else:
        for i in range(len(lietotaja_saraksts) + int(len(lietotaja_saraksts)/2)):
             saraksts = shuffle_keys(lietotaja_saraksts.copy()) 
             return_values = populate_grid(saraksts)
             if return_values:
                print(return_values[0])
                print_grid(return_values[1])
             
    
if __name__ == "__main__":
    main()