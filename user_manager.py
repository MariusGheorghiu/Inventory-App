import json
import os

#Gestionarea utilizatorilor: autentificare și administrare.
class UserManager:
    def __init__(self, filename="data/users.json"):
        self.filename = filename
        self.users = self.load_users()

    #Incarca utilizatorii sau returneaza o lista goala
    def load_users(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    #Salveaza lista de utilizatori în fisier
    def save_users(self):
        with open(self.filename, "w") as file:
            json.dump(self.users, file)

    #Adauga un utilizator nou
    def add_user(self, username, password, is_admin=False):
        self.users.append({"username": username, "password": password, "is_admin": is_admin})
        self.save_users()

    #Verifica daca utilizatorul este valid
    def authenticate(self, username, password):
        for user in self.users:
            if user["username"] == username and user["password"] == password:
                return user
        return None