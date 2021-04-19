import sys
from io import BytesIO
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt
from pprint import pprint

import requests
from PIL import Image


DELTA = 0.005
LETTER_LONGITUDE = 0
LETTER_LATTITUDE = 0
LETTER = '{},{},org'
LETTER_LONGITUDE = 0
LETTER_LATTITUDE = 0


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
MAP_TYPE = 'map'


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
    global LONGITUDE
    LONGITUDE = float(toponym_longitude)
    global LATTITUDE
    global MAP_TYPE
    global DELTA
    LATTITUDE = float(toponym_lattitude)
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    im = Image.open(BytesIO(response.content))
    im.save('images/map.png')


def make_bigger():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    global LONGITUDE, LATTITUDE
    toponym_longitude, toponym_lattitude = str(LONGITUDE), str(LATTITUDE)
    global DELTA
    global MAP_TYPE
    DELTA -= 0.001
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
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
    global DELTA
    global LONGITUDE, LATTITUDE
    global MAP_TYPE
    toponym_longitude, toponym_lattitude = str(LONGITUDE), str(LATTITUDE)
    DELTA += 0.001
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    try:
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
    except Exception:
        pass


def need_function(json_response):
    json_envelope = \
        json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['boundedBy']['Envelope']
    object_x1, object_y1 = [float(elem)
                            for elem in json_envelope['lowerCorner'].split()]
    object_x2, object_y2 = [float(elem)
                            for elem in json_envelope['upperCorner'].split()]
    object_width = object_x2 - object_x1
    object_height = object_y2 - object_y1
    return (object_width, object_height)


def move_up():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    global LONGITUDE, LATTITUDE
    width, height = need_function(JSON_RESPONSE)
    LATTITUDE += height
    toponym_longitude, toponym_lattitude = str(LONGITUDE), str(LATTITUDE)
    global DELTA
    global MAP_TYPE
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    try:
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
    except Exception:
        pass


def move_down():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    global LONGITUDE, LATTITUDE
    width, height = need_function(JSON_RESPONSE)
    LATTITUDE -= height
    toponym_longitude, toponym_lattitude = str(LONGITUDE), str(LATTITUDE)
    global DELTA
    global MAP_TYPE
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    try:
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
    except Exception:
        pass


def move_right():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    global LONGITUDE, LATTITUDE
    width, height = need_function(JSON_RESPONSE)
    LONGITUDE += width
    toponym_longitude, toponym_lattitude = str(LONGITUDE), str(LATTITUDE)
    global DELTA
    global MAP_TYPE
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    try:
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
    except Exception:
        pass


def change_map_type():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    global LONGITUDE, LATTITUDE
    toponym_longitude, toponym_lattitude = str(LONGITUDE), str(LATTITUDE)
    global DELTA
    global MAP_TYPE
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    try:
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
    except Exception:
        pass


def search_object(address, widget):
    toponym_to_find = address
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        widget.plainTextEdit.setPlainText('Объект не найден!')
        return
    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        global LONGITUDE
        LONGITUDE = float(toponym_longitude)
        global LATTITUDE
        global MAP_TYPE
        global DELTA
        global LETTER_LONGITUDE, LETTER_LATTITUDE
        LATTITUDE = float(toponym_lattitude)
        delta = str(DELTA)
        LETTER_LONGITUDE = LONGITUDE
        LETTER_LATTITUDE = LATTITUDE
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": MAP_TYPE,
            'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        im = Image.open(BytesIO(response.content))
        im.save('images/map.png')
        widget.plainTextEdit_2.setPlainText(toponym_address)
    except Exception:
        widget.plainTextEdit.setPlainText('Объект не найден!')


def move_left():
    global JSON_RESPONSE
    json_response = JSON_RESPONSE
    global LONGITUDE, LATTITUDE
    width, height = need_function(JSON_RESPONSE)
    LONGITUDE -= width
    toponym_longitude, toponym_lattitude = str(LONGITUDE), str(LATTITUDE)
    global DELTA
    global MAP_TYPE
    delta = str(DELTA)
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": MAP_TYPE,
        'pt': LETTER.format(LETTER_LONGITUDE, LETTER_LATTITUDE)
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
        self.MyButton.clicked.connect(self.run)
        self.MyButton_2.clicked.connect(self.run)
        self.MyButton_3.clicked.connect(self.run)
        self.MyButton_3.clicked.connect(self.run)
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.run)

    def run(self):
        global MAP_TYPE
        if self.sender() == self.pushButton:
            search_object(self.plainTextEdit.toPlainText(), self)
        elif self.sender() == self.pushButton_2:
            self.plainTextEdit.setPlainText('')
            self.plainTextEdit_2.setPlainText('')
            global LETTER_LONGITUDE, LETTER_LATTITUDE
            LETTER_LONGITUDE = 0
            LETTER_LATTITUDE = 0
            change_map_type()
        else:
            if self.sender() == self.MyButton:
                MAP_TYPE = 'map'
            if self.sender() == self.MyButton_2:
                MAP_TYPE = 'sat'
            if self.sender() == self.MyButton_3:
                MAP_TYPE = 'sat,skl'
            change_map_type()
        self.pixmap = QPixmap('images/map.png')
        self.pixmap = self.pixmap.scaled(
            self.label.width(), self.label.height())
        self.label.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            make_bigger()
        if event.key() == Qt.Key_PageDown:
            make_smaller()
        if event.key() == Qt.Key_Up:
            move_up()
        if event.key() == Qt.Key_Right:
            move_right()
        if event.key() == Qt.Key_Down:
            move_down()
        if event.key() == Qt.Key_Left:
            move_left()
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
