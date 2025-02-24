import sys

from PyQt5 import QtWidgets, QtGui, uic

from inventory_manager import InventoryManager
from user_manager import UserManager


class LoginWindow(QtWidgets.QWidget):
    def __init__(self, user_manager, inventory_app):
        super().__init__()
        self.user_manager = user_manager
        self.inventory_app = inventory_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Autentificare")
        self.setGeometry(400, 300, 300, 150)



        layout = QtWidgets.QVBoxLayout()

        self.username_input = QtWidgets.QLineEdit(self)
        self.username_input.setPlaceholderText("Nume de utilizator")
        layout.addWidget(self.username_input)

        self.password_input = QtWidgets.QLineEdit(self)
        self.password_input.setPlaceholderText("Parolă")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QtWidgets.QPushButton("Autentificare", self)
        self.login_button.clicked.connect(self.authenticate)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = self.user_manager.authenticate(username, password)
        if user:
            self.inventory_app.set_user(user)
            self.inventory_app.show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Eroare", "Nume de utilizator sau parola incorecta.")

#Aceasta clasa reprezinta interfața principala a aplicatiei.
class InventoryApp(QtWidgets.QMainWindow):
    def __init__(self, user_manager, inventory_manager):
        super().__init__()
        self.user_manager = user_manager
        self.inventory_manager = inventory_manager
        self.current_user = None

        # Seteaza iconita aplicatiei
        self.setWindowIcon(QtGui.QIcon('dist/data/icon.ico'))
        self.setStyleSheet("""
            QWidget {
                background-color: #cfd8dc; 
                font-family: 'Arial',; 
                font-size: 12pt; 
            }

            QPushButton {
                background-color: #263238; 
                color: white;
                padding: 8px 16px; 
                border: none;
                border-radius: 15px; 
                font-size: 15pt; 
            }

            QPushButton:hover {
                background-color: #37474f; 
            }

            QPushButton:pressed {
                background-color: #336600; 
            }

            QLabel {
                color: #333; 
                font-weight: 500; 
                margin-bottom: 5px; 
            }

            QLineEdit, QTextEdit, QTableWidget { 
                padding: 6px; 
                border: 1px solid #ccc;
                border-radius: 4px; 
                font-size: 10pt; 
                background-color: white;
            }

            QTableWidget::item { 
                padding: 4px;
            }

            QTableWidget::horizontalHeader { 
                background-color: #eee;
                color: #333;
                font-weight: bold;
            }

            QInputDialog {
                font-size: 10pt;
            }

            QMessageBox {
                background-color: #ffffff; 
                font-size: 10pt;
            }
        """)

        self.init_ui()


    def set_user(self, user):
        self.current_user = user

    def init_ui(self):
        self.setWindowTitle("Gestionare Inventar")
        self.setGeometry(100, 100, 500, 300)


        # Layout principal
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout()

        # Butoane pentru funcționalități
        self.add_button = QtWidgets.QPushButton(" ➕Adauga Obiect")
        self.add_button.clicked.connect(self.add_item_dialog)
        layout.addWidget(self.add_button)

        self.delete_button = QtWidgets.QPushButton("❌Sterge Obiect")
        self.delete_button.clicked.connect(self.delete_item_dialog)
        layout.addWidget(self.delete_button)

        self.list_button = QtWidgets.QPushButton("📋Afiseaza Obiecte")
        self.list_button.clicked.connect(self.list_items_dialog)
        layout.addWidget(self.list_button)

        self.search_button = QtWidgets.QPushButton("🔍Cauta Obiect")
        self.search_button.clicked.connect(self.search_item)
        layout.addWidget(self.search_button)

        self.allocate_button = QtWidgets.QPushButton("📌Aloca Obiect")
        self.allocate_button.clicked.connect(self.allocate_item)
        layout.addWidget(self.allocate_button)

        central_widget.setLayout(layout)

    def add_item_dialog(self):
        if self.current_user and self.current_user["is_admin"]:
            company, company_entered = QtWidgets.QInputDialog.getText(self, "Adauga Obiect", "Introduceti firma:")
            model, model_entered = QtWidgets.QInputDialog.getText(self, "Adauga Obiect", "Introduceti modelul:")
            year, year_entered = QtWidgets.QInputDialog.getText(self, "Adauga Obiect", "Introduceti anul achizitiei:")
            price, price_entered = QtWidgets.QInputDialog.getText(self, "Adauga Obiect", "Introduceti pretul:")
            department, department_entered = QtWidgets.QInputDialog.getText(self, "Adauga Obiect",
                                                                            "Introduceti departamentul:")

            if company_entered and model_entered and year_entered and price_entered and department_entered:
                try:
                    year = int(year)
                    price = float(price)
                    item = {
                        "id": len(self.inventory_manager.items) + 1,  # ID unic
                        "company": company,
                        "model": model,
                        "year": year,
                        "price": price,
                        "department": department,
                        "allocated_to": ""  # Initial, obiectul nu este alocat
                    }
                    self.inventory_manager.add_item(item)
                    QtWidgets.QMessageBox.information(self, "Succes", "Obiect adaugat cu succes!")
                except ValueError:
                    QtWidgets.QMessageBox.warning(self, "Eroare", "Anul și pretul trebuie să fie numere valide.")
            else:
                QtWidgets.QMessageBox.warning(self, "Eroare", "Toate campurile sunt obligatorii.")
        else:
            QtWidgets.QMessageBox.warning(self, "Eroare", "Doar administratorii pot adauga obiecte.")

    def delete_item_dialog(self):
        if self.current_user and self.current_user["is_admin"]:
            # Dialog pentru stergerea unui obiect
            item_id, ok = QtWidgets.QInputDialog.getInt(self, "Sterge Obiect", "Introduceti ID-ul obiectului de sters:")

            if ok:
                if self.inventory_manager.delete_item(item_id):
                    QtWidgets.QMessageBox.information(self, "Succes", "Obiect sters cu succes!")
                else:
                    QtWidgets.QMessageBox.warning(self, "Eroare", "Obiectul nu a fost gasit.")
        else:
            QtWidgets.QMessageBox.warning(self, "Eroare", "Doar administratorii pot sterge obiecte.")

    def list_items_dialog(self):
        items = self.inventory_manager.list_items()
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Lista Obiectelor")
        dialog.setGeometry(100, 100, 800, 400)  # Mărim fereastra pentru a încăpea tabelul

        layout = QtWidgets.QVBoxLayout()

        # Cream un tabel
        table = QtWidgets.QTableWidget(dialog)
        table.setColumnCount(7)  # 7 coloane pentru fiecare câmp al obiectului
        table.setHorizontalHeaderLabels(["ID", "Firma", "Model", "An", "Pret $", "Departament", "Alocat catre"])

        # Setam dimensiunile coloanelor
        table.setColumnWidth(0, 50)  # ID
        table.setColumnWidth(1, 120)  # Firma
        table.setColumnWidth(2, 150)  # Model
        table.setColumnWidth(3, 65)  # An
        table.setColumnWidth(4, 80)  # Pret
        table.setColumnWidth(5, 140)  # Departament
        table.setColumnWidth(6, 120)  # Alocat catre

        # Setam numarul de randuri
        table.setRowCount(len(items))

        # Definirea unui font personalizat
        custom_font = QtGui.QFont("Britannic Bold", 10)

        # Adaugam date in tabel
        for row, item in enumerate(items):
            for column, key in enumerate(["id", "company", "model", "year", "price", "department", "allocated_to"]):
                table_item = QtWidgets.QTableWidgetItem(str(item[key]))
                table_item.setFont(custom_font)  # Aplicăm fontul personalizat
                table.setItem(row, column, table_item)

                # Adauga culori diferite pentru fiecare coloana in parte
                if column == 0:  # ID
                    table_item.setBackground(QtGui.QColor("#d3d3d3"))
                elif column == 1:  # Firma
                    table_item.setBackground(QtGui.QColor("#b9f6ca"))
                elif column == 2:  # Model
                    table_item.setBackground(QtGui.QColor("#90caf9"))
                elif column == 3:  # An
                    table_item.setBackground(QtGui.QColor("#ffb74d"))
                elif column == 4:  # Pret
                    table_item.setBackground(QtGui.QColor("#afbfa0"))
                elif column == 5:  # Departament
                    table_item.setBackground(QtGui.QColor("#c8e6c9"))
                elif column == 6:  # Alocat catre
                    table_item.setBackground(QtGui.QColor("#ce93d8"))

        layout.addWidget(table)
        dialog.setLayout(layout)

        dialog.exec_()

    def search_item(self):
        search_key, search_key_ok = QtWidgets.QInputDialog.getItem(self, "Cauta Obiecte", "Selectati criteriul de cautare:", ["company", "model", "year", "department", "allocated_to"])
        search_value, search_value_ok = QtWidgets.QInputDialog.getText(self, "Cauta Obiect", f"Introduceti valoarea pentru {search_key}:")

        if search_key_ok and search_value_ok:
            results = self.inventory_manager.search_item(**{search_key: search_value})
            if not results:
                QtWidgets.QMessageBox.information(self, "Rezultat", "Nu au fost gasite obiecte.")
            else:
                result_texts = [f"ID: {item['id']}, Firma: {item['company']}, Model: {item['model']}, An: {item['year']}, Preț: {item['price']}, Departament: {item['department']}, Alocat către: {item['allocated_to']}" for item in results]
                QtWidgets.QMessageBox.information(self, "Rezultat", "\n".join(result_texts))

    def allocate_item(self):
        item_id, item_id_ok = QtWidgets.QInputDialog.getInt(self, "Aloca Obiect", "Introduceti ID-ul obiectului:")
        user, user_ok = QtWidgets.QInputDialog.getText(self, "Aloca Obiect", "Introduceti numele utilizatorului:")

        if item_id_ok and user_ok:
            if self.inventory_manager.allocate_item(item_id, user):
                QtWidgets.QMessageBox.information(self, "Succes", f"Obiectul cu ID-ul {item_id} a fost alocat utilizatorului {user}.")
            else:
                QtWidgets.QMessageBox.warning(self, "Eroare", "Obiectul nu a fost gasit sau este deja alocat altui utilizator.")




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    user_manager = UserManager("data/users.json")
    inventory_manager = InventoryManager("data/inventory.json")
    inventory_app = InventoryApp(user_manager, inventory_manager)
    login_window = LoginWindow(user_manager, inventory_app)
    login_window.show()
    sys.exit(app.exec_())