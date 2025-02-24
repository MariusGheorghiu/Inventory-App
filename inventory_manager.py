import json
import os


class InventoryManager:

    # Initializeaza managerul si încarca datele din fisier.
    def __init__(self, filename="data/inventory.json"):
        self.filename = filename
        self.items = self.load_data()

    # Incarca datele din fiaierul JSON sau returneaza o listă goala.
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return []
        return []

    # Salvează datele în fișierul JSON.
    def save_data(self):

        with open(self.filename, "w") as file:
            json.dump(self.items, file, indent=4)
    # Adauga un obiect nou in inventar
    def add_item(self, item):
        self.items.append(item)
        self.save_data()

    #Sterge un obiect pe baza ID-ului.
    def delete_item(self, item_id):

        self.items = [item for item in self.items if item["id"] != item_id]
        self.save_data()

    #Cauta obiecte dupa criterii specifice.
    def search_item(self, **kwargs):
        results = self.items
        for key, value in kwargs.items():
            results = [item for item in results if str(item.get(key, "")).lower() == str(value).lower()]
        return results

    #Returnează lista tuturor obiectelor din inventar.
    def list_items(self):
        return self.items

    #Aloca un obiect unui utilizator daca nu este deja alocat.
    def allocate_item(self, item_id, user):
        for item in self.items:
            if item["id"] == item_id and not item.get("allocated_to"):
                item["allocated_to"] = user
                self.save_data()
                return True
        return False
