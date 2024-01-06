from main import *
import json
import os

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
    with open("answer_keys.json", "r+") as file:
        if os.stat("answer_keys.json").st_size != 0:
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

write_to_file(sample_dict, "cita mikla")
write_to_file(sample_dict, "vel kkas")