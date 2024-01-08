from main import *
import json
import os

file_name = "answer_keys.json" # faila nosaukums
sample_puzzle = "Izmēģinājuma mīkla" # key vērtība izmēģinājuma mīklai, ko nevar izdzēst

def write_to_file(answer_key, title):
    # pievieno dict mīklu ar atbildēm un jautājumiem
    with open(file_name, "r+", encoding="utf8") as file:
        if os.stat(file_name).st_size != 0:
            file_data = json.load(file)
            if title not in file_data:
                file_data[title] = answer_key
                file.seek(0)
                json.dump(file_data, file, indent=4)
            else:
                print("Šāda mīkla jau eksistē! Izvēlies citu nosaukumu.")
                return False
        else:
            dict = {title:answer_key}
            json.dump(dict, file, indent=4)
    return True

def save(miklas_nosaukums, entry_array):
    # pievieno jauno mīklu failam

    file_data = {}
    file_size = os.stat(file_name).st_size
    with open(file_name, "r", encoding="utf8") as file:
            if file_size != 0:
                file_data = json.load(file)

    with open(file_name, "w") as file:
        if file_size != 0:
            file_data[miklas_nosaukums] = entry_array
            file.seek(0)
            json.dump(file_data, file, indent=4, ensure_ascii=False)
        else:
            dict_to_save = {miklas_nosaukums: entry_array}
            json.dump(dict_to_save, file, indent=4, ensure_ascii=False)
    return True



def return_keys():
    # atgriež sarakstu ar krustvārdu mīklu nosaukumiem, kas saglabāti failā
    keys = []
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            keys = list(data.keys())
    return keys

def return_answers(puzzle_key):
    # atgriež sarakstu ar konkrētas puzles atbildēm
    answers = []
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            for entry in data[puzzle_key]:
                answers.append(entry["answer"])
    return answers

def return_questions(puzzle_key):
    # atgriež sarakstu ar konkrētās puzles jautājumiem
    questions = []
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            for entry in data[puzzle_key]:
                questions.append(entry["question"])
    return questions

def combine_dict(answers, questions):
    # apvieno atbilžu un jautājumu sarakstu vārdnīcā
    # tādā formātā, kas atbilst populate_grid() funkcijai
    dict = {}
    for i in range(len(answers)):
        dict[answers[i]] = questions[i]
    return dict

def return_puzzle(puzzle_key):
    # atgriež sarakstu ar visām puzles atbildēm un jautājumiem
    puzzle = []
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            puzzle = data[puzzle_key]
    return puzzle

def clear_file(): 
    # izdzēš visus faila datus, izņemot pirmo ierakstu (izmēģinājuma mīklu)
    data = {}
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            keys = data.copy().keys()
            for key in keys:
                if key != sample_puzzle:
                    del data[key]
    
    with open(file_name, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)

def delete_puzzle(puzzle_key):
    # izdzēš konkrētu mīklu no faila
    data = {}
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            keys = data.copy().keys()
            for key in keys:
                if key == puzzle_key:
                    del data[key]
    
    with open(file_name, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)

def update_puzzle(puzzle_key, new_entries):
    # new_entries ir saraksts formātā [{"number": .., "orientation": .., "answer": .., "question": ..}, {...}, ...]
    # pieliek konkrētajai puzlei klāt jaunus ierakstus
    data = {}
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            keys = data.copy().keys()
            for key in keys:
                if key == puzzle_key:
                    data[key] = new_entries
    
    with open(file_name, "w", encoding="utf8") as f:
        json.dump(data, f, indent=4)
