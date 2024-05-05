import json, sys
from datetime import datetime

finance_data = {'balance':0,
                'transactions':{}}

main_menu = ['Показать баланс', 'Добавить операцию', 'Выход']


def write_data(data:dict=finance_data) -> None:
    '''Функция записывает данные в файл. На входе ожидается словарь с данными.'''
    with open("data.txt", 'w') as file:
        file.write(str(json.dumps(data)))


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
    finance_data = load_data()
    color = '\033[92m' if finance_data['balance'] > 0 else '\033[91m'
    print(f"Баланс: {color}{finance_data['balance']}$\033[00m")


def wrong_command() -> None:
    '''Информирует пользователя об ошибке ввода'''
    print('\033[91mНеверная комманда / формат ввода данных!\033[00m')


# Функция для добавления транзакцияй
def add_transaction() -> None:
    '''Данная функция ничего не принимает, но ожидает ввода от пользователя, записывает произведенные транзакции'''

    while True:
        input_data = input('Введите сумму перации (c - для расходов) и описание операции через ";"\n')
        if ';' not in input_data:
            wrong_command()
        else:
            transaction_sum, transaction_desctiption = input_data.split(';')
            transaction_sum = round(float(transaction_sum), 2)
            finance_data = load_data()
            finance_data['balance'] += transaction_sum
            finance_data['transactions'][str(datetime.now())] = [transaction_sum, transaction_desctiption.strip()]
            write_data(finance_data)
            print(f'Внесена следующая операция: "{transaction_desctiption}"')
            show_balance()
            return


main_menu_functions = {'1': show_balance, '2': add_transaction, '3': sys.exit}

# Главный цикл
while True:
    for i, option in enumerate(main_menu, 1):
        print(i, option)
    command = input('Введите номер команды...\n')
    if command in main_menu_functions:
        main_menu_functions[command]()
    else:
        wrong_command()

