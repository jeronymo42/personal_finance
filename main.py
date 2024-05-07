import json
import sys
import os
import re
from typing import Union

finance_data: dict = {'Дата': '',
                'Категория': 'Доход',
                'Сумма': 0,
                'Описание': ''
                }

main_menu: list = ['Показать баланс', 'Добавить операцию',
                   'Редактирование записи', 'Поиск записей','Выход']


def write_data(data: dict = finance_data) -> None:
    '''Функция записывает данные в файл. На входе ожидается словарь с данными.'''

    with open("data.txt", 'a', encoding='UTF-8') as file:
        file.write(str(json.dumps(data))+'\n')


def load_data() -> dict:
    '''Функция загружает данные из файла. При отсутствии данных формируется новый пустой файл.'''

    try:
        with open("data.txt", 'r', encoding='UTF-8') as data:
            data: str = data.readline()
            if data:
                result = json.loads(data)
                return result
    except:
        write_data(finance_data)
        return finance_data


def show_balance() -> None:
    '''Выводи баланс на экран'''

    income: float = 0
    expances: float = 0
    with open("data.txt", 'r', encoding='UTF-8') as data:
        current_line: str = data.readline()
        while current_line:
            transaction: str = json.loads(current_line)
            if transaction['Категория'] == 'Доход':
                income += transaction['Сумма']
            else:
                expances += transaction['Сумма']
            current_line = data.readline()
    red: str = '\033[91m'
    green: str = '\033[92m'
    balance: float = round(income - expances, 2)
    print(f"Баланс: {green if balance > 0 else red}{balance}$\033[00m")
    print(f'Доходы: {green}{income}$\033[00m;')
    print(f'Расходы: {red}{expances}$\033[00m;')


def wrong_command() -> None:
    '''Информирует пользователя об ошибке ввода'''

    print('\033[91mНеверная комманда / формат ввода данных!\033[00m')


def request_transactiona_data() -> dict:
    '''Функция опрашивает пользователя для формирования полноценной транзакции'''

    transactiona_data: dict = {}
    while True:
        date: str = input('Введите дату операции в формате Год-Месяц-День\n')
        match = re.match(r'[1,2]\d{3}-\d{2}-\d{2}', date)
        if not match:
            wrong_command()
            continue
        transactiona_data['Дата'] = date
        break

    while True:
        category: str = input('Введите категорию операции (Доход/Расход)\n')
        category = category.strip().capitalize()
        if category != 'Доход' and category != 'Расход':
            wrong_command()
            continue
        finance_data['Категория'] = category
        break

    while True:
        operation_sum: str = input('Введите сумму операции\n')
        try:
            operation_sum = round(float(operation_sum), 2)
        except:
            wrong_command()
            continue
        finance_data['Сумма'] = operation_sum
        break


    decription: str = input('Введите описание операции (может быть пустым)\n')
    finance_data['Описание'] = decription
    return finance_data


# Функция для добавления транзакцияй
def add_transaction_to_file() -> None:
    '''Функция вызывает request_transactiona_data
     для обработки ввода от пользователя и записывает транзакции в файл'''

    transactiona_data = request_transactiona_data()
    write_data(transactiona_data)


def search_data(key: str, parameter: str) -> Union[list[dict], None]:
    '''Функция поиска по параметру. Принимает 2 строки как аргументы
     и возвращает список словарей (преобразованные JSON записи транзакций)'''

    search_result = []
    try:
        with open("data.txt", 'r', encoding='UTF-8') as data:
            current_line: str = data.readline()
            while current_line:
                result: dict = json.loads(current_line)
                if result.get(key) == parameter:
                    search_result.append(result)
                    print(result)
                current_line: str = data.readline()
            return search_result
    except Exception as e:
        print(f'Произошла ошибка: {e}')

def search_transactions() -> Union[list[dict], None]:
    '''Функция запрашивает у пользователя параметры поиска
    и вызывает поиск с соответствующими параметрами'''

    key: str = ''
    parameter: str = ''
    answer: str = input('Ищем транзакцию по дате? (y/n)\n')
    if answer.lower() == 'y':
        while True:
            date: str = input('Введите дату операции в формате Год-Месяц-День\n')
            match: Union(str, None) = re.match(r'[1,2]\d{3}-\d{2}-\d{2}', date)
            if match:
                key = 'Дата'
                parameter = date
                print('OK')
                return search_data(key, parameter)
            else:
                wrong_command()

    answer: str = input('Ищем транзакцию по категории? (y/n)\n')
    if answer.lower() == 'y':
        while True:
            category: str = input('Введите категорию операции (Доход/Расход):\n')
            category = category.strip().capitalize()
            if category == 'Доход' or category == 'Расход':
                key = 'Категория'
                parameter = category
                print('OK')
                return search_data(key, parameter)
            else:
                wrong_command()

    answer: str = input('Ищем транзакцию по сумме? (y/n)\n')
    if answer.lower() == 'y':
        while True:
            transaction_sum: str = input('Введите сумму искомой транзакции:\n')
            match: Union(str, None)  = re.match(r'\d+\.?\d*', transaction_sum)
            if match:
                key = 'Сумма'
                parameter = float(transaction_sum)
                print('OK')
                return search_data(key, parameter)
            else:
                wrong_command()

def change_transaction() -> None:
    '''Функция для изменения транзакций'''

    print('Сначала найдем нужные транзакции')
    search_result: Union(list[dict], None) = search_transactions()
    changed_transactions: list[dict] = []
    if search_result:
        for transaction in search_result:
            transaction_data = request_transactiona_data()
            changed_transactions.append(transaction_data)
        with open("data.txt", 'r', encoding='UTF-8') as data:
            current_line: str = data.readline()
            while current_line:
                transaction: dict = json.loads(current_line)
                if transaction in search_result:
                    transaction = changed_transactions[search_result.index(transaction)]
                with open("data_tmp.txt", 'a', encoding='UTF-8') as data_tmp:
                    data_tmp.write(str(json.dumps(transaction))+'\n')
                current_line: str = data.readline()
        os.remove("data.txt")
        os.rename("data_tmp.txt", "data.txt")
    else:
        print('Ничего не найдено! =(')

main_menu_functions:dict = {'1': show_balance,
                            '2': add_transaction_to_file,
                            '3': change_transaction,
                            '4':search_transactions,
                            '5': sys.exit
                            }

# Главный цикл
while True:
    for i, option in enumerate(main_menu, 1):
        print(i, option)
    command: str = input('Введите номер команды...\n')
    if command in main_menu_functions:
        main_menu_functions[command]()
    else:
        wrong_command()
