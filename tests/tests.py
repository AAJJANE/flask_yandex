import requests
from pprint import pprint


def print_response(description, response):
    print("\n" + description)
    try:
        pprint(response.json())
    except Exception as e:
        print("Ошибка при разборе JSON:", e)
        print("Сырые данные:", response.text)


print("\n--- USERS API ---")

# 1. Получить пользователя с ID 2
response = requests.get("http://127.0.0.1:8080/api/v2/users/2")
print_response("Получение пользователя с ID 2:", response)

# 2. Получить пользователя с некорректным ID (0)
response = requests.get("http://127.0.0.1:8080/api/v2/users/0")
print_response("Получение пользователя с некорректным ID (0):", response)

# 3. Удалить пользователя с некорректным ID (0)
response = requests.delete("http://127.0.0.1:8080/api/v2/users/0")
print_response("Удаление пользователя с некорректным ID (0):", response)

# 4. Удалить пользователя с ID 6
response = requests.delete("http://127.0.0.1:8080/api/v2/users/6")
print_response("Удаление пользователя с ID 6:", response)

# 5. Создание пользователя (BAD no-json — запрос без тела)
response = requests.post("http://127.0.0.1:8080/api/v2/users")
print_response("Создание пользователя (без JSON-тела):", response)

# 6. Создание пользователя (BAD empty — пустой JSON)
response = requests.post(
    "http://127.0.0.1:8080/api/v2/users",
    headers={"Content-Type": "application/json"},
    json={}
)
print_response("Создание пользователя (пустой JSON):", response)

# 7. Создание пользователя (валидные данные)
new_user = {
    "surname": "{% faker 'randomLastName' %}",
    "name": "{% faker 'randomFirstName' %}",
    "age": 18,
    "position": "{% faker 'randomJobTitle' %}",
    "speciality": "{% faker 'randomNoun' %}",
    "address": "{% faker 'randomStreetAddress' %}",
    "email": "{% faker 'randomEmail' %}",
    "password": "{% faker 'randomPassword' %}"
}
response = requests.post(
    "http://127.0.0.1:8080/api/v2/users",
    headers={"Content-Type": "application/json"},
    json=new_user
)
print_response("Создание пользователя (валидные данные):", response)

# 8. Обновление пользователя PUT с некорректным ID (без данных)
response = requests.put("http://127.0.0.1:8080/api/v2/users/0")
print_response("Обновление пользователя с некорректным ID (0) без данных:", response)

# 9. Обновление пользователя PUT с пустым JSON (ID 2)
response = requests.put(
    "http://127.0.0.1:8080/api/v2/users/2",
    headers={"Content-Type": "application/json"},
    json={}
)
print_response("Обновление пользователя с ID 2 (пустой JSON):", response)

# 10. Обновление адреса пользователя PUT (ID 2)
update_address = {
    "address": "{% faker 'randomCity' %}"
}
response = requests.put(
    "http://127.0.0.1:8080/api/v2/users/2",
    headers={"Content-Type": "application/json"},
    json=update_address
)
print_response("Обновление адреса пользователя с ID 2:", response)

# 11. Получить список всех пользователей
response = requests.get("http://127.0.0.1:8080/api/v2/users")
print_response("Список всех пользователей:", response)
