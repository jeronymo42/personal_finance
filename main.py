import json
import sys
import re
from datetime import datetime

finance_data = {'Дата': '',
                'Категория': 'Доход',
                'Сумма': 0,
                'Описание': ''
                }

main_menu = ['Показать баланс', 'Добавить операцию', 'Редактирование записи', 'Поиск записей','Выход']


def write_data(data: dict = finance_data) -> None:
    '''Функция записывает данные в файл. На входе ожидается словарь с данными.'''
    with open("data.txt", 'a') as file:
        file.write(str(json.dumps(data))+'\n')


def load_data() -> dict:
    '''Функция загружает данные из файла'''
    try:
        with open("data.txt", 'r') as data:
            data = data.readline()
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
    with open("data.txt", 'r') as data:
        current_line: str = data.readline()
        while current_line:
            transaction = json.loads(current_line)
            if transaction['Категория'] == 'Доход':
                income += transaction['Сумма']
            else:
                expances += transaction['Сумма']
            current_line = data.readline()
    red = '\033[91m'
    green = '\033[92m'
    balance = income - expances
    print(f"Баланс: {green if balance > 0 else red}{balance}$\033[00m")
    print(f'Доходы: {green}{income}$\033[00m;')
    print(f'Расходы: {red}{expances}$\033[00m;')


def wrong_command() -> None:
    '''Информирует пользователя об ошибке ввода'''
    print('\033[91mНеверная комманда / формат ввода данных!\033[00m')


# Функция для добавления транзакцияй
def add_transaction() -> None:
    '''Данная функция ничего не принимает, но ожидает ввода от пользователя, записывает произведенные транзакции'''
    finance_data = {}
    while True:
        date: str = input('Введите дату операции в формате Год-Месяц-День\n')
        match = re.match(r'[1,2]\d{3}-\d{2}-\d{2}', date)
        if not match:
            wrong_command()
            continue
        finance_data['Дата'] = date
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
    

    decription: str = input('Введите описание операции\n')
    finance_data['Описание'] = decription
    write_data(finance_data)

def search_data(key: str, parameter: str) -> None:
    try:
        with open("data.txt", 'r') as data:
            current_line = data.readline()
            while current_line:
                result = json.loads(current_line)
                if result.get(key) == parameter:
                    print(result)
                    current_line
                return result
    except Exception as e:
        print(f'Произошла ошибка: {e}')

def search_transactions() -> None:
    key: str = ''
    parameter: str = ''
    answer: str = input('Ищем транзакцию по дате? (y/n)\n')
    if answer.lower() == 'y':
        while True:
            date = input('Введите дату операции в формате Год-Месяц-День\n')
            match = re.match(r'[1,2]\d{3}-\d{2}-\d{2}', date)
            if match:
                key = date
                parameter = 'Дата'
                print('OK')
                return
            else:
                wrong_command()
                
    answer: str = input('Ищем транзакцию по категории? (y/n)\n')
    if answer.lower() == 'y':
        while True:
            category = input('Введите категорию операции (Доход/Расход):\n')
            category = category.strip().capitalize()
            if category == 'Доход' or category == 'Расход':
                key = category
                parameter = 'Категория'
                print('OK')
                return
            else:
                wrong_command()


    answer: str = input('Ищем транзакцию по сумме? (y/n)\n')
    if answer.lower() == 'y':
        while True:
            transaction_sum = input('Введите сумму искомой транзакции:\n')
            match = re.match(r'\d+\.?\d*', transaction_sum)
            if match:
                key = transaction_sum
                parameter = 'Сумма'
                print('OK')
                return
            else:
                wrong_command()


main_menu_functions:dict = {'1': show_balance, '2': add_transaction, '3':'', '4':search_transactions ,'5': sys.exit}

# Главный цикл
while True:
    for i, option in enumerate(main_menu, 1):
        print(i, option)
    command = input('Введите номер команды...\n')
    if command in main_menu_functions:
        main_menu_functions[command]()
    else:
        wrong_command()
