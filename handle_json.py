from main import *
import json
import os
from tkinter import simpledialog

file_name = "answer_keys.json" # faila nosaukums
sample_puzzle = "Izmēģinājuma mīkla" # key vērtība izmēģinājuma mīklai

sample_dict = [
    {
        "number" : 1,
        "answer" : "dators",
        "question" : "Kur dzīvo vīrusi"
    },
    {
        "number" : 2,
        "answer" : "bulcina",
        "question" : "Labakas brokastis" 
    }
    ]

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
def save(dictionary):
    mīklas_nosaukums = simpledialog.askstring("Nosaukums", "Ievadiet mīklas nosaukumu:")
    if not mīklas_nosaukums:
        print("Lūdzu, ievadiet mīklas nosaukumu!")
        return False

    file_name = "answer_keys.json"  # Aizpildiet ar vēlamo faila nosaukumu
    with open(file_name, "r+", encoding="utf8") as file:
        if os.stat(file_name).st_size != 0:
            file_data = json.load(file)
            if mīklas_nosaukums not in file_data:
                # Mainīt nosaukumu no 'word' uz 'answer'
                updated_dictionary = [
                    {
                        'number': item['number'],
                        'orientation': item['orientation'],
                        'answer': item['word'],
                        'question': item['question'][1]
                    } for item in dictionary
                ]
                file_data[mīklas_nosaukums] = updated_dictionary
                file.seek(0)
                json.dump(file_data, file, indent=4, ensure_ascii=False)
            else:
                print("Šāda mīkla jau eksistē! Izvēlies citu nosaukumu.")
                return False
        else:
            # Mainīt nosaukumu no 'word' uz 'answer'
            dict_to_save = {mīklas_nosaukums: [
                {
                    'number': item['number'],
                    'orientation': item['orientation'],
                    'answer': item['word'],
                    'question': item['question'][1]
                } for item in dictionary
            ]}
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
    return


# write_to_file(sample_dict, "pirmā mīkla")
# write_to_file(sample_dict, "otrā mīkla")
# print(return_keys())
# print(return_answers("Izmēģinājuma mīkla"))
# print(return_puzzle("Izmēģinājuma mīkla"))
# clear_file()
# # print(combine_dict(return_answers("Izmēģinājuma mīkla"), return_questions("Izmēģinājuma mīkla")))