from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
from plyer import notification
from kivy.core.window import Window


class NotificationApp(App):
    def build(self):
        # Устанавливаем белый фон окна
        Window.clearcolor = (1, 1, 1, 1)

        # Главный layout - вертикальный контейнер
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint=(1, 1)
        )

        # Заголовок приложения
        title_label = Label(
            text='Напоминания',
            font_size='24sp',
            color=(0, 0, 0, 1),  # Черный цвет
            size_hint=(1, 0.2),
            bold=True
        )
        main_layout.add_widget(title_label)

        # Контейнер для поля ввода времени
        time_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, 0.2)
        )

        time_label = Label(
            text='Время до напоминания (минуты):',
            font_size='16sp',
            color=(0, 0, 0, 1),
            size_hint=(1, 0.5),
            halign='left'
        )
        time_layout.add_widget(time_label)

        self.time_input = TextInput(
            hint_text='Например: 5, 10, 30',
            multiline=False,
            size_hint=(1, 0.5),
            font_size='18sp',
            foreground_color=(0, 0, 0, 1),
            background_color=(0.95, 0.95, 0.95, 1),
            padding=[10, 10],
            input_filter='int'  # Только цифры
        )
        time_layout.add_widget(self.time_input)

        main_layout.add_widget(time_layout)

        # Контейнер для поля ввода сообщения
        message_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(1, 0.2)
        )

        message_label = Label(
            text='Текст напоминания:',
            font_size='16sp',
            color=(0, 0, 0, 1),
            size_hint=(1, 0.5),
            halign='left'
        )
        message_layout.add_widget(message_label)

        self.message_input = TextInput(
            hint_text='Что вам нужно не забыть?',
            multiline=False,
            size_hint=(1, 0.5),
            font_size='18sp',
            foreground_color=(0, 0, 0, 1),
            background_color=(0.95, 0.95, 0.95, 1),
            padding=[10, 10]
        )
        message_layout.add_widget(self.message_input)

        main_layout.add_widget(message_layout)

        # Кнопка установки напоминания
        self.set_button = Button(
            text='Установить напоминание',
            size_hint=(1, 0.15),
            font_size='18sp',
            background_color=(0.2, 0.6, 1, 1),  # Синий цвет
            color=(1, 1, 1, 1),  # Белый текст
            bold=True
        )
        self.set_button.bind(on_press=self.set_notification)
        main_layout.add_widget(self.set_button)

        # Метка статуса
        self.status_label = Label(
            text='Готов к работе',
            font_size='16sp',
            color=(0.3, 0.3, 0.3, 1),  # Серый цвет
            size_hint=(1, 0.1)
        )
        main_layout.add_widget(self.status_label)

        return main_layout

    def set_notification(self, instance):
        """
        Метод вызывается при нажатии на кнопку установки напоминания
        instance - ссылка на кнопку, которая была нажата
        """
        try:
            # Получаем текст из поля ввода времени
            time_text = self.time_input.text.strip()

            # Проверяем, что время не пустое
            if not time_text:
                self.show_error("Введите время в минутах")
                return

            # Преобразуем текст в число (минуты)
            minutes = int(time_text)

            # Проверяем, что время положительное
            if minutes <= 0:
                self.show_error("Время должно быть больше 0 минут")
                return

            # Получаем текст сообщения
            message = self.message_input.text.strip()

            # Проверяем, что сообщение не пустое
            if not message:
                self.show_error("Введите текст напоминания")
                return

            # Переводим минуты в секунды
            seconds = minutes * 60

            # Устанавливаем таймер для отправки уведомления
            # Clock.schedule_once выполняет функцию один раз через указанное время
            Clock.schedule_once(lambda dt: self.send_notification(message), seconds)

            # Обновляем статус
            self.status_label.text = f'Напоминание установлено на {minutes} минут'
            self.status_label.color = (0, 0.5, 0, 1)  # Зеленый цвет

            # Очищаем поля ввода
            self.time_input.text = ''
            self.message_input.text = ''

        except ValueError:
            # Ошибка возникает если введено не число
            self.show_error("Введите корректное число минут")
        except Exception as e:
            # Обработка любых других ошибок
            self.show_error(f"Произошла ошибка: {str(e)}")

    def send_notification(self, message):
        """
        Метод для отправки системного уведомления
        message - текст напоминания
        """
        try:
            # Используем plyer для отправки уведомления
            notification.notify(
                title='Напоминание',  # Заголовок уведомления
                message=message,  # Текст уведомления
                timeout=10,  # Время показа уведомления в секундах
                app_name='Notification App'  # Название приложения
            )

            # Обновляем статус в основном потоке Kivy
            # Используем Clock.schedule_once чтобы избежать проблем с потоками
            Clock.schedule_once(lambda dt: self.update_status('Напоминание отправлено!'), 0)

        except Exception as e:
            # Если возникла ошибка при отправке уведомления
            error_message = f"Ошибка отправки: {str(e)}"
            Clock.schedule_once(lambda dt: self.show_error(error_message), 0)

    def update_status(self, text):
        """
        Метод для обновления текста статуса
        text - новый текст статуса
        """
        self.status_label.text = text
        self.status_label.color = (0, 0.5, 0, 1)  # Зеленый цвет

    def show_error(self, message):
        """
        Метод для показа всплывающего окна с ошибкой
        message - текст ошибки
        """
        # Создаем контент для popup окна
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Текст ошибки
        error_label = Label(
            text=message,
            font_size='16sp',
            color=(0, 0, 0, 1),
            size_hint=(1, 0.7)
        )
        content.add_widget(error_label)

        # Кнопка OK
        ok_button = Button(
            text='OK',
            size_hint=(1, 0.3),
            background_color=(0.8, 0.2, 0.2, 1),  # Красный цвет
            color=(1, 1, 1, 1)  # Белый текст
        )
        content.add_widget(ok_button)

        # Создаем popup окно
        popup = Popup(
            title='Ошибка',
            content=content,
            size_hint=(0.8, 0.4),
            auto_dismiss=False
        )

        # Привязываем кнопку OK к закрытию popup
        ok_button.bind(on_press=popup.dismiss)

        # Открываем popup окно
        popup.open()

        # Также обновляем статусную метку
        self.status_label.text = 'Ошибка: ' + message
        self.status_label.color = (0.8, 0.2, 0.2, 1)  # Красный цвет


# Запуск приложения
if __name__ == '__main__':
    NotificationApp().run()