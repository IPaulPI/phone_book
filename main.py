def work_with_phonebook():
    while True:
        choice = show_menu()  # Показать меню и получить выбор пользователя
        phone_book = read_txt('phon.txt')  # Прочитать данные из файла

        if choice == 1:
            print_result(phone_book)  # Показать весь справочник
        elif choice == 2:
            last_name = input('Введите фамилию: ')
            found_contacts = find_by_lastname(phone_book, last_name)  # Найти абонента по фамилии
            for contact in found_contacts:
                print(contact)  # Показать найденные контакты
        elif choice == 3:
            number = input('Введите номер телефона: ')
            print(find_by_number(phone_book, number))  # Найти абонента по номеру телефона
        elif choice == 4:
            user_data = input('Введите новые данные (Фамилия, Имя, Телефон, Описание): ')
            add_user(phone_book, user_data)  # Добавить нового абонента
            write_txt('phon.txt', phone_book)  # Сохранить изменения в файл
        elif choice == 5:
            last_name = input('Введите фамилию: ')
            contact_index = select_contact_by_lastname(phone_book, last_name)
            if contact_index is not None:
                new_number = input('Введите новый номер: ')
                print(change_number(phone_book, contact_index, new_number))  # Изменить номер абонента
                write_txt('phon.txt', phone_book)  # Сохранить изменения в файл
        elif choice == 6:
            last_name = input('Введите фамилию: ')
            contact_index = select_contact_by_lastname(phone_book, last_name)
            if contact_index is not None:
                print(delete_by_lastname(phone_book, contact_index))  # Удалить абонента по фамилии
                write_txt('phon.txt', phone_book)  # Сохранить изменения в файл
        elif choice == 7:
            source_file = input('Введите имя исходного файла: ')
            target_file = input('Введите имя целевого файла: ')
            last_name = input('Введите фамилию для копирования: ')
            copy_contact(source_file, target_file, last_name)  # Копировать контакт
        elif choice == 8:
            print("Работа завершена.")
            break  # Завершить работу

def show_menu():
    # Показать меню
    print("\nВыберите необходимое действие:\n"
          "1. Отобразить весь справочник\n"
          "2. Найти абонента по фамилии\n"
          "3. Найти абонента по номеру телефона\n"
          "4. Добавить абонента в справочник\n"
          "5. Изменить номер абонента по фамилии\n"
          "6. Удалить абонента по фамилии\n"
          "7. Копировать контакт из одного файла в другой\n"
          "8. Закончить работу")
    while True:
        try:
            choice = int(input('Введите номер действия: '))  # Получить выбор пользователя
            if 1 <= choice <= 8:
                return choice
            else:
                print("Введите число от 1 до 8.")
        except ValueError:
            print("Введите допустимое число.")

def read_txt(filename):
    phone_book = []
    fields = ['Фамилия', 'Имя', 'Телефон', 'Описание']  # Поля записи

    # Открыть файл и прочитать строки
    with open(filename, 'r', encoding='utf-8') as phb:
        for line in phb:
            stripped_line = line.strip()
            if stripped_line:  # Игнорировать пустые строки
                record = dict(zip(fields, stripped_line.split(',')))  # Преобразовать строку в запись (словарь)
                phone_book.append(record)  # Добавить запись в телефонную книгу

    return phone_book

def write_txt(filename, phone_book):
    # Открыть файл и записать данные
    with open(filename, 'w', encoding='utf-8') as phout:
        for record in phone_book:
            if all(value.strip() for value in record.values()):  # Проверка на пустые значения
                s = ','.join(value.strip() for value in record.values())  # Преобразовать запись (словарь) в строку
                phout.write(f'{s}\n')  # Записать строку в файл

def print_result(phone_book):
    # Показать все записи в телефонной книге
    for record in phone_book:
        print(' '.join(value for value in record.values()))

def find_by_lastname(phone_book, last_name):
    # Найти записи по фамилии и вернуть их в виде строки с пробелами между значениями
    for record in phone_book:
        return (' '.join(record.values()) for record in phone_book if record['Фамилия'] == last_name)


def find_by_number(phone_book, number):
    # Найти записи по номеру телефона
    found_contacts = [ ' '.join(record.values()) for record in phone_book if record['Телефон'] == number ]
    if found_contacts:
        return found_contacts[0]  # Вернуть первый найденный контакт в виде строки
    else:
        return f'Контакт с номером телефона {number} не найден.'


def change_number(phone_book, index, new_number):
    # Изменить номер телефона абонента по индексу
    phone_book[index]['Телефон'] = new_number
    return f'Number changed to {new_number}'

def delete_by_lastname(phone_book, index):
    # Удалить запись по индексу
    deleted_record = phone_book.pop(index)
    return f'Entry for {deleted_record["Фамилия"]} deleted'

def add_user(phone_book, user_data):
    # Добавить новую запись
    fields = ['Фамилия', 'Имя', 'Телефон', 'Описание']
    cleaned_data = [data.strip() for data in user_data.split(',')]  # Удалить лишние пробелы для каждого элемента
    record = dict(zip(fields, cleaned_data))  # Преобразовать данные в запись (словарь)
    if all(value for value in record.values()):  # Проверка на пустые значения
        phone_book.append(record)  # Добавить запись в телефонную книгу

def copy_contact(source_file, target_file, last_name):
    source_phone_book = read_txt(source_file)  # Прочитать исходный файл
    target_phone_book = read_txt(target_file)  # Прочитать целевой файл

    # Найти контакт по фамилии
    contact = find_by_lastname(source_phone_book, last_name)
    if contact:
        target_phone_book.extend(contact)  # Добавить контакт в целевой файл
        write_txt(target_file, target_phone_book)  # Сохранить изменения
        print(f'Контакт {last_name} успешно скопирован из {source_file} в {target_file}.')
    else:
        print(f'Контакт с фамилией {last_name} не найден в файле {source_file}.')

def select_contact_by_lastname(phone_book, last_name):
    # Найти записи по фамилии и предложить пользователю выбрать нужный контакт
    contacts = find_by_lastname(phone_book, last_name)
    if not contacts:
        print(f'Контакты с фамилией {last_name} не найдены.')
        return None
    if len(contacts) == 1:
        return phone_book.index(contacts[0])  # Вернуть индекс единственного контакта
    print(f'Найдено несколько контактов с фамилией {last_name}:')
    for index, contact in enumerate(contacts):
        print(f"{index + 1}: {' '.join(contact.values())}")
    while True:
        try:
            selection = int(input('Выберите номер контакта: '))  # Предложить пользователю выбрать контакт
            if 1 <= selection <= len(contacts):
                return phone_book.index(contacts[selection - 1])  # Вернуть индекс выбранного контакта
            else:
                print(f"Введите число от 1 до {len(contacts)}.")
        except ValueError:
            print("Введите допустимое число.")

work_with_phonebook()
