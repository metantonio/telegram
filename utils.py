import json

def find_user(username):
    try:
        with open("contact.json", "r") as f:
            contacts = json.load(f)
            
            if username in contacts:
                #print(contacts[username]["email"])
                return contacts[username]["email"]
            else:
                #print("user do not exist")
                return None
    except NameError as error:
        print(str(error))
        return None

def find_files(username):
    try:
        with open("contact.json", "r") as f:
            contacts = json.load(f)
            
            if username in contacts:
                #print(contacts[username]["email"])
                files= contacts[username]["files"]
                text = ""
                with open("files.json", "r") as fjson:
                    files_doc = json.load(fjson)
                    for file in files:
                        text += "\n"+files_doc[file]["description"] + " en la url: " + files_doc[file]["url"]
                    return text
            else:
                #print("user do not exist")
                return None
    except NameError as error:
        print(str(error))
        return None