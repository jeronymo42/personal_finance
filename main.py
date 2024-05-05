import json
from datetime import datetime

finance_data = {'balance':0,
                'transactions':{}}

main_menu = ['Показать баланс', 'Добавить операцию']

def write_data():
    with open("data.txt", 'r') as data:
        data.write(json.dumps(finance_data))

def load_data():
    with open("data.txt", 'r') as data:
        result = json.loads(data.readline())
    return result

def show_balance():
    finance_data = load_data()
    print(f"Баланс: \033[92m{finance_data['balance']}$\033[00m")

def wrong_command():
    print('\033[91mНеверная комманда / формат ввода данных!\033[00m')

main_menu_functions = {'1':show_balance}

while True:
    for i, option in enumerate(main_menu, 1):
        print(i, option)
    command = input()
    if command in main_menu_functions:
        main_menu_functions[command]()
    else:
        wrong_command()

