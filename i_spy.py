# модуль для работы с JSON-форматом
import json
# модуль для HTTP-запросов
import urllib.request
# модуль рисования, часть графической библиотеки tkinter
import turtle
# модуль для использования возможностей операционной системы
import os
import time
# модуль для открытия URL-адресов по умолчанию
import webbrowser
from typing import Dict, List, Any
from http.client import HTTPResponse


os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    # задаём адрес для запроса списка космонавтов
    url: str = 'http://api.open-notify.org/astros.json'
    res: HTTPResponse = urllib.request.urlopen(url)
    # загружаем и читаем json-файл
    result: Dict[str, Any] = json.loads(res.read())
    # создаём текстовый файл с именами членов экипажа
    # открываем файл для записи
    with open('iss.txt', 'w') as file:
        # добавляем запись и дублируем текст в консоль
        file.write(f'В настоящий момент на МКС {str(result["number"])} космонавтов:\n\n')
        print('В настоящий момент на МКС ' + str(result["number"]) + ' космонавтов:\n')
        # получаем список имён космонавтов
        people: List[Dict[str, str]] = result['people']
        for person in people:
            file.write(person['name'] + '\n')
            # дублируем текст в консоль
            print(person['name'])

    file_path: str = os.path.abspath('iss.txt')

    # главное окно для графической работы
    screen: turtle.Screen = turtle.Screen()
    screen.setup(1280, 720)
   
    # устанавливаем систему координат для экрана, аналогичную координатам Земли
    screen.setworldcoordinates(-180, -90, 180, 90)
    # загружаем изображение карты мира из файла
    screen.bgpic('map.gif')
    # загружаем изображение станции из файла
    screen.register_shape('iss.gif')
    # присваиваем переменной iss значение объекта Turtle
    iss = turtle.Turtle()
    # придаём переменной вид изображения станции из файла
    iss.shape('iss.gif')
    # выключаем функцию рисования следа от объекта Turtle()
    iss.penup()

    while True:
        # адрес для запроса о текущем положении МКС
        url: str = 'http://api.open-notify.org/iss-now.json'
        res: HTTPResponse = urllib.request.urlopen(url)
        # переводим ответ в JSON и читаем
        result: Dict[str, Dict[str, str]] = json.loads(res.read())
        # локация станции
        location: Dict[str, str] = result['iss_position']
        # широта
        lat: float = float(location['latitude'])
        # долгота
        lon: float = float(location['longitude'])

        current_time: str = time.strftime("%Y-%m-%d %H:%M:%S")
        print("\nДата и время:", current_time)
        print(f'Широта: {lat}')
        print(f'Долгота: {lon}')

        iss.goto(lon, lat)

        time.sleep(5)


main()
