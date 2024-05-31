#!/usr/bin/python

import pytest
from ..api import PetFriends
from ..settings import valid_email, valid_passwd
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, passwd=valid_passwd):
    """Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, passwd)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert "key" in result

def test_get_all_pets_with_valid_key(filter=""):
    """Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - "my_pets" либо "" """

    _, auth_key = pf.get_api_key(valid_email, valid_passwd)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result["pets"]) > 0

def test_add_new_pet_with_valid_data(name="Marsik", animal_type="scotchfold", age="4", pet_photo="images/cat1.jpg"):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info(name="Мурзик", animal_type="Котэ", age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets["pets"]) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets["pets"][0]["id"], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result["name"] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Task 24.7.2 Test 1
def test_successfull_create_pet_simple(name="Marsik", animal_type="scotchfold", age="4"):
    """Проверяем что можно добавить питомца с корректными данными без фотографии методом create_pet_simple"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["name"] == name

# Task 24.7.2 Test 2
def test_successfull_set_photo(pet_photo="images/cat1.jpg"):
    """Проверяем что можно добавить питомцу фотографию"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key, также запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    
    # Проверяем - если список своих питомцев пустой, то добавляем нового без фотографии и опять запрашиваем список своих питомцев
    if len(my_pets["pets"]) == 0:
        pf.create_pet_simple(auth_key, "Суперкот2", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фотографии
    pet_id = my_pets["pets"][0]["id"]
    status, result = pf.set_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result["pet_photo"] != ""

# Task 24.7.2 Test 3
def test_get_api_key_for_invalid_user(email="vasja@pupkin.com", passwd="00000000"):
    """Проверяем что запрос api ключа при неверных реквизитах доступа возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, _ = pf.get_api_key(email, passwd)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

# Task 24.7.2 Test 4
def test_unsuccessfull_create_pet_simple1(name="Мурзик", animal_type=None, age=4):
    """Проверяем что при добавлении питомца с некорректными данными без фотографии методом create_pet_simple
    сервер вернёт статус-код 400"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)

    # Добавляем питомца
    status, _ = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    
# Task 24.7.2 Test 5
def test_unsuccessfull_create_pet_simple2(name="Мурзик", animal_type="Кот", age=4):
    """Проверяем что при добавлении питомца с корректными данными без фотографии методом create_pet_simple
    с некорректным auth_key сервер вернёт статус-код 403"""

    # Задаём некорректный auth_key
    auth_key = {
        "key": "12345"
    }

    # Добавляем питомца
    status, _ = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
    
# Task 24.7.2 Test 6
def test_get_all_pets_with_invalid_key(filter=""):
    """Проверяем что запрос всех питомцев с некорректным auth_key возвращает статус код 403.
    Доступное значение параметра filter - "my_pets" либо "" """

    # Задаём некорректный auth_key
    auth_key = {
        "key": "12345"
    }
    
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status == 403

# Task 24.7.2 Test 7
def test_add_new_pet_with_invalid_data(name="NoneCat", animal_type=None, age="4", pet_photo="images/cat1.jpg"):
    """Проверяем что при попытке добавить питомца с некорректными данными сервер возвращает статус-код 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)

    # Добавляем питомца
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Task 24.7.2 Test 8
def test_add_new_pet_with_invalid_key(name="SuperBig", animal_type="scotchfold", age="4", pet_photo="images/cat1.jpg"):
    """Проверяем что при поытке добавить питомца с корректными данными, но с некорректным auth_key,
    сервер возвращает статус-код 403."""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Задаём некорректный auth_key
    auth_key = {
        "key": "12345"
    }

    # Добавляем питомца
    status, _ = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403

# Task 24.7.2 Test 9
def test_unsuccessfull_set_photo_with_invalid_data(pet_photo="images/not_photo.jpg"):
    """Проверяем что при попытке добавить питомцу некорректную фотографию сервер возвращает
    статус-код 400"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key, также запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    
    # Проверяем - если список своих питомцев пустой, то добавляем нового без фотографии и опять запрашиваем список своих питомцев
    if len(my_pets["pets"]) == 0:
        pf.create_pet_simple(auth_key, "Суперкот2", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фотографии
    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.set_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

# Task 24.7.2 Test 10
def test_unsuccessfull_set_photo_with_invalid_key(pet_photo="images/cat1.jpg"):
    """Проверяем что при попытке добавить питомцу фотографию с некорректным auth_key
    сервер возвращает статус-код 403"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key, также запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_passwd)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    
    # Проверяем - если список своих питомцев пустой, то добавляем нового без фотографии и опять запрашиваем список своих питомцев
    if len(my_pets["pets"]) == 0:
        pf.create_pet_simple(auth_key, "Суперкот2", "кот", "3")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на добавление фотографии
    pet_id = my_pets["pets"][0]["id"]
    
    # Задаём некорректный auth_key
    auth_key = {
        "key": "12345"
    }
    
    status, _ = pf.set_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403
