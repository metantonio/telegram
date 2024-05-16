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
