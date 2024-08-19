import os
import sys
import pandas as pd
import re
from colorama import init, Fore
from art import text2art

init(autoreset=True)

# Инициализация словаря текстов для двух языков
texts = {
    "ru": {
        "menu": "[1] Добавить базу\n[2] Удалить базу\n[3] Искать по базам\n[4] Выйти\n[5] Сменить язык",
        "add_db": "Выберите номер базы для добавления (или 16 для выхода): ",
        "db_exists": "Эта база уже занята.",
        "enter_path": "Введите директорию базы: ",
        "db_added": "База добавлена.",
        "invalid_path": "Неверный путь или формат файла.",
        "remove_db": "Выберите номер базы для удаления (или 16 для выхода): ",
        "db_empty": "Эта база уже пустая.",
        "db_removed": "База удалена.",
        "search_query": "Введите данные для поиска: ",
        "parsing": "Идет парсинг баз данных...",
        "read_success": "Чтение файла {path} успешно",
        "found_matches": "Найдены совпадения в файле {path}, столбец {column}",
        "no_matches": "Совпадений не найдено в файле {path}, столбец {column}",
        "results": "Результаты поиска:",
        "no_results": "Ничего не найдено.",
        "press_enter": "Нажмите Enter, чтобы вернуться в главное меню...",
        "exit_message": "Выход из программы.",
        "exit_press_enter": "Нажмите Enter, чтобы закрыть...",
        "invalid_choice": "Неверный выбор. Попробуйте снова.",
        "language_changed": "Язык изменен на русский."
    },
    "en": {
        "menu": "[1] Add Database\n[2] Remove Database\n[3] Search Databases\n[4] Exit\n[5] Change Language",
        "add_db": "Choose a database number to add (or 16 to exit): ",
        "db_exists": "This database is already occupied.",
        "enter_path": "Enter the database path: ",
        "db_added": "Database added.",
        "invalid_path": "Invalid path or file format.",
        "remove_db": "Choose a database number to remove (or 16 to exit): ",
        "db_empty": "This database is already empty.",
        "db_removed": "Database removed.",
        "search_query": "Enter data to search: ",
        "parsing": "Parsing databases...",
        "read_success": "Reading file {path} was successful",
        "found_matches": "Matches found in file {path}, column {column}",
        "no_matches": "No matches found in file {path}, column {column}",
        "results": "Search results:",
        "no_results": "No results found.",
        "press_enter": "Press Enter to return to the main menu...",
        "exit_message": "Exiting the program.",
        "exit_press_enter": "Press Enter to close...",
        "invalid_choice": "Invalid choice. Please try again.",
        "language_changed": "Language changed to English."
    }
}

# Переменная для хранения текущего языка
current_language = "ru"

def get_text(key):
    return texts[current_language][key]

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + text2art("SLAYSEARCH", font='block'))
    print(Fore.RED + get_text("menu"))

def print_database_menu(databases):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i, db in enumerate(databases, start=1):
        status = "Пустая" if db is None else db
        print(f"[{i}] {status}")
    print("[16] " + get_text("press_enter"))

def add_database(databases):
    while True:
        print_database_menu(databases)
        choice = input(get_text("add_db"))
        if choice == "16":
            break
        if choice.isdigit() and 1 <= int(choice) <= 15:
            index = int(choice) - 1
            if databases[index] is not None:
                print(get_text("db_exists"))
            else:
                path = input(get_text("enter_path"))
                if os.path.exists(path) and (path.endswith(".csv") or path.endswith(".xlsx")):
                    databases[index] = path
                    print(get_text("db_added"))
                else:
                    print(get_text("invalid_path"))
        else:
            print(get_text("invalid_choice"))

def remove_database(databases):
    while True:
        print_database_menu(databases)
        choice = input(get_text("remove_db"))
        if choice == "16":
            break
        if choice.isdigit() and 1 <= int(choice) <= 15:
            index = int(choice) - 1
            if databases[index] is None:
                print(get_text("db_empty"))
            else:
                databases[index] = None
                print(get_text("db_removed"))
        else:
            print(get_text("invalid_choice"))

def search_databases(databases):
    query = input(get_text("search_query"))
    escaped_query = re.escape(query)
    print(get_text("parsing"))

    results = []
    for path in databases:
        if path is None:
            continue

        try:
            if path.endswith(".csv"):
                df = pd.read_csv(path)
            elif path.endswith(".xlsx"):
                df = pd.read_excel(path)
            else:
                continue
        except Exception as e:
            print(f"Error reading file {path}: {e}")
            continue

        print(get_text("read_success").format(path=path))
        print(df.head())  # Вывод первых строк для отладки

        for column in df.columns:
            matches = df[df[column].astype(str).str.contains(escaped_query, na=False, case=False)]
            if not matches.empty:
                results.append(matches)
                print(get_text("found_matches").format(path=path, column=column))
            else:
                print(get_text("no_matches").format(path=path, column=column))

    if results:
        print(get_text("results"))
        for result in results:
            print(result.to_string(index=False))
    else:
        print(get_text("no_results"))

    input("\n" + get_text("press_enter"))

def change_language():
    global current_language
    current_language = "en" if current_language == "ru" else "ru"
    print(get_text("language_changed"))

def main():
    databases = [None] * 15

    while True:
        print_menu()
        choice = input("Выберите действие: ")
        if choice == "1":
            add_database(databases)
        elif choice == "2":
            remove_database(databases)
        elif choice == "3":
            search_databases(databases)
        elif choice == "4":
            print(get_text("exit_message"))
            input(get_text("exit_press_enter"))
            sys.exit()
        elif choice == "5":
            change_language()
        else:
            print(get_text("invalid_choice"))

if __name__ == "__main__":
    main()

        
