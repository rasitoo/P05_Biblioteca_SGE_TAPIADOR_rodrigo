from biblioteca.repositories.repository import Repositories
from biblioteca.views.view import menu
from biblioteca.controllers.controller import Controller

if __name__ == "__main__":
    repo = Repositories("ejem.db")
    controller = Controller(repo)
    menu(controller)