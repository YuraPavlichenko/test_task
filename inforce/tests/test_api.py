import requests
import json


url = 'http://localhost:8000/create-menu/'


def test_create_menu_with_invalid_price():
    data = {
        'dish_name': 'Test Dish',
        'restaurant': 1,
        'price': 'Invalid Price',
        'day_of_week': 'Monday',
        'date': '2023-09-25',
    }

    response = requests.post(url, data=data)
    assert response.status_code == 400 or response.status_code == 404


def test_invalid_page_returns_404():
    url = 'http://127.0.0.1:8000/restaurant/dsadanjk/menu/'

    response = requests.get(url)
    assert response.status_code == 404


def test_get_menu_by_day():
    url = 'http://127.0.0.1:8000/menu-by-day/monday/'  # Замініть цей URL на актуальний
    response = requests.get(url)

    assert response.status_code == 200
    assert response.headers['content-type'] == 'application/json'


def test_get_jwt_tokens():
    url = 'http://127.0.0.1:8000/api/token/'
    data = {
        'username': 'admin',
        'password': 'admin',  # Замініть на свій пароль
    }

    response = requests.post(url, data=data)

    assert response.status_code == 200
    response_data = response.json()

    assert 'refresh' in response_data
    assert 'access' in response_data


def test_restaurant_creation():
    url = 'http://127.0.0.1:8000/create-restaurant/'
    data = {
        'name': 'test_restaurant',
    }

    response = requests.post(url, data=data)

    assert response.status_code == 201