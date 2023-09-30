from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.vector import Vector

# Импорт необходимых модулей для обработки акселерометра на мобильном устройстве
from plyer import accelerometer
import serial

class ControlApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Управление: Подключение...")
        self.layout.add_widget(self.label)

        # Запуск слушателя акселерометра
        accelerometer.enable()
        Clock.schedule_interval(self.update, 1.0/10.0)

        # Подключение к ПК через USB
        try:
            self.ser = serial.Serial('COM3', 9600)  # Укажите правильный COM-порт и скорость передачи
            self.label.text = "Управление: Подключено к ПК"
        except serial.SerialException:
            self.label.text = "Управление: Ошибка подключения"

        return self.layout

    def update(self, dt):
        # Получение данных акселерометра
        acceleration = accelerometer.acceleration[:3]

        # Обработка данных акселерометра
        x, y, z = acceleration
        vector = Vector(x, y)
        angle = vector.angle((1, 0))  # Угол между текущим вектором и (1, 0)

        # Управление влево и вправо на основе угла
        if angle < 45 or angle > 315:
            self.label.text = "Управление: Влево"
            self.send_data("LEFT_ON")
        elif 135 < angle < 225:
            self.label.text = "Управление: Вправо"
            self.send_data("RIGHT_ON")
        else:
            self.label.text = "Управление: Нейтральное положение"
            self.send_data("NEUTRAL")

    def send_data(self, data):
        if hasattr(self, 'ser'):
            self.ser.write(data.encode('utf-8') + b'\n')

    def on_stop(self):
        if hasattr(self, 'ser'):
            self.ser.close()

if __name__ == '__main__':
    ControlApp().run()
