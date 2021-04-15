import sys
from io import BytesIO
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtCore import Qt

import requests
from PIL import Image


DELTA = 0.005


def get_request():
    toponym_to_find = 'Вашингтон, Мемориал Линкольна'
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('response error:')
        print(response)
        sys.exit()
    json_response = response.json()
    return json_response


JSON_RESPONSE = get_request()


def save_image():
    toponym_to_find = 'Вашингтон, Мемориал Линкольна'
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        print('response error:')
        print(response)
        sys.exit()
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    delta = "0.005"
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    im = Image.open(BytesIO(response.content))
    im.save('images/map.png')


def make_bigger():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    global DELTA
    DELTA -= 0.001
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    try:
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
    except Exception:
        pass


def make_smaller():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    global DELTA
    DELTA += 0.001
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    try:
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
    except Exception:
        pass


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_form.ui', self)
        save_image()
        self.pixmap = QPixmap('images/map.png')
        self.pixmap = self.pixmap.scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(self.pixmap)

    def run(self):
        self.label.setText("OK")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            make_bigger()
        if event.key() == Qt.Key_PageDown:
            make_smaller()
        self.pixmap = QPixmap('images/map.png')
        self.pixmap = self.pixmap.scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(self.pixmap)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
