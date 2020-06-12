import sys
import requests

# Данные авторизации в API Trello
auth_params = {
    'key': "88ec0baa4378b3c5292a816dc58e057d",
    'token': "52bbb5f65bd95f8b53dc3c9871e4f3cef2b9e09b49b9e40c30b7e29cc44bafde",
}

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы
base_url = "https://api.trello.com/1/{}"

board_id = "5ee33bb4b3e11f67637e71e9"

def read():
    # Получим данные всех колонок на доске:
    column_data = requests.get(base_url.format('boards')+'/'+board_id+'/lists', params=auth_params).json()

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:
    for column in column_data:
        print(column['name'])

        # Получим данные всех задач в колонке и перечислим все названия
        task_data = requests.get(base_url.format('lists')+'/'+column['id']+'/cards', params=auth_params).json()
        if not task_data:
            print('\t'+'Нет задач!')
            continue
        for task in task_data:
            print('\t'+task['name'])

def create(name, column_name):
    # Получим данные всех колонок на доске
    column_date=requests.get(base_url.format('boards')+'/'+board_id+'/lists', params=auth_params).json()

    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна
    for column in column_date:
        if column['name'] == column_name:
            # Создадим задачу с именем _name_ в найденной колонке
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
            break

def move(name, column_name):
    # Получим данные всех колонок на доске
    column_data = requests.get(base_url.format('boards')+'/'+board_id+'/lists', params=auth_params).json()
    
    # Среди всех колонок нужно найти задачу по имени и получить её id
    task_id = None
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists')+'/'+column['id']+'/cards', params=auth_params).json()
        for task in column_tasks:
            if task['name'] == name:
                print("task['id']: ", task['id'])
                task_id = task['id']
                break
        if task_id:
            break

    # Теперь, когда у нас есть id задачи, которую мы хотим переместить
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу
    for column in column_data:
        if column['name'] == column_name:
            print("column['id']: ", column['id'])
            # И выполним запрос к API для перемещения задачи в нужную колонку
            requests.put(base_url.format('cards')+'/'+task_id+'/idList', data = {'value': column['id'], **auth_params})
            break

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])
