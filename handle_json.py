from main import *
import json
import os

file_name = "answer_keys.json"

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

def return_puzzle(puzzle_key):
    # atgriež sarakstu ar visām puzles atbildēm un jautājumiem
    puzzle = []
    with open(file_name, "r", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            puzzle = data[puzzle_key]
    return puzzle

def clear_file(): #nestrādā
    # TODO: izdzēš visus faila datus, izņemot pirmo ierakstu
    with open(file_name, "r+", encoding="utf8") as f:
        if os.stat(file_name).st_size != 0:
            data = json.load(f)
            pirmais_ieraksts = {"Izmēģinājuma mīkla" : data["Izmēģinājuma mīkla"]}
            print(pirmais_ieraksts)
            f.seek(0)
            json.dump(pirmais_ieraksts, f, indent=4)
    return


write_to_file(sample_dict, "pirmā mīkla")
write_to_file(sample_dict, "otrā mīkla")
print(return_keys())
print(return_answers("Izmēģinājuma mīkla"))
print(return_puzzle("Izmēģinājuma mīkla"))
#clear_file()