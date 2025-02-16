def menu(controller):
    while True:
        opcion = input("""
        1. Alta de socio
        2. Baja de socio
        3. Alta de libro
        4. Baja de libro
        5. Prestar libro
        6. Devolver libro
        7. Consultar libros
        8. Consultar usuarios
        9. Consultar prestamos
        0. Salir
        Seleccione una opción: 
        """)
        try:
            if opcion == '1':
                dni = input("DNI: ")
                name = input("Nombre: ")
                email = input("Email: ")
                number = input("Número: ")
                address = input("Dirección: ")
                controller.add_user(dni, name, email, number, address)
            elif opcion == '2':
                dni = input("DNI: ")
                controller.remove_user(dni)
            elif opcion == '3':
                isbn = input("ISBN: ")
                title = input("Título: ")
                author = input("Autor: ")
                genre = input("Género: ")
                cover_uri = input("URI de la portada: ")
                synopsis = input("Sinopsis: ")
                controller.add_book(isbn, title, author, genre, cover_uri, synopsis)
            elif opcion == '4':
                isbn = input("ISBN: ")
                controller.remove_book(isbn)
            elif opcion == '5':
                isbn = input("ISBN: ")
                dni = input("DNI del socio: ")
                controller.lend_book(isbn, dni)
            elif opcion == '6':
                isbn = input("ISBN: ")
                controller.return_book(isbn)
            elif opcion == '7':
                books = controller.list_books()
                for book in books:
                    print(book)
            elif opcion == '8':
                users = controller.list_users()
                for user in users:
                    print(user)
            elif opcion == '9':
                loans = controller.list_loans()
                for loan in loans:
                    print(loan)
            elif opcion == '0':
                break
            else:
                print("Opción no válida, intente de nuevo.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")