from biblioteca.views.view import menu
from biblioteca.controllers.controller import Controller

if __name__ == "__main__":
    db_name = "biblioteca.db"
    controller = Controller(db_name)
    menu(controller)