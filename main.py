import sqlite3 as sq
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView


base = sq.connect('pizza.db')
cur = base.cursor()

base.execute('CREATE TABLE IF NOT EXISTS data(name PRIMARY KEY, point)')
base.commit()


def add_in_db(name, point):
    cur.execute('INSERT INTO data VALUES(?, ?)', (name, point))
    base.commit()


def del_in_db(name):
    cur.execute('DELETE FROM data WHERE name == ?', (name, ))
    base.commit()


def check_db():
    s = cur.execute('SELECT * FROM data').fetchall()
    d = {}
    for value, key in s:
        d[int(key)] = value
    arr = sorted([i for i in d.keys()], reverse=True)
    result = []
    for i, value in enumerate(arr):
        result.append(f'{i+1}. {d[value]} - {value}\n')
    return result


class MyApp(App):
    def build(self):
        # глваное окно
        container = BoxLayout(orientation='vertical')
        button_container = BoxLayout(size_hint=[1, 0.3])
        # объявление виджетов
        del_screen_btn = Button(text='удалить', on_release=self.run_del_screen)
        add_screen_btn = Button(text='добавить', on_release=self.run_add_screen)
        spisok = ScrollView()
        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.update_spisok()
        spisok.add_widget(self.layout)

        # добавление виджетов
        button_container.add_widget(add_screen_btn)
        button_container.add_widget(del_screen_btn)
        container.add_widget(spisok)
        container.add_widget(button_container)

        return container

    def update_spisok(self):
        self.layout.clear_widgets()
        for i in check_db():
            self.layout.add_widget(Button(text=i, size_hint_y=None))


    def run_add_screen(self, value):
        # функции
        def back(event):
            screen.dismiss()

        def save(value):
            if len(name.text) != 0 and len(point.text) != 0:
                for i in point.text:
                    if i not in '1234567890':
                        point.text = ''
                        label.text = 'в строке с баллами должны быть только числа'
                        break
                else:
                    text = name.text
                    add_in_db(name.text, point.text)
                    name.text = ''
                    point.text = ''
                    self.update_spisok()
                    label.text = f'{text} сохранено'
            else:
                label.text = 'необходимо заполнить все поля'
        # окно добавления знчений
        screen = ModalView(size_hint=[1, 0.5], auto_dismiss=False)
        container = BoxLayout(orientation='vertical')
        button_container = BoxLayout(size_hint=[1, 0.4])

        label = Label(text='Здесь можно добавить позицию')
        name = TextInput(multiline=False, size_hint=[1, 0.5], font_size='30sp', hint_text='название позиции')
        point = TextInput(multiline=False, size_hint=[1, 0.5], font_size='30sp', hint_text='кол-во баллов')
        save_btn = Button(text='сохранить', on_release=save)
        back_btn = Button(text='назад', on_release=back)

        button_container.add_widget(save_btn)
        button_container.add_widget(back_btn)

        container.add_widget(label)
        container.add_widget(name)
        container.add_widget(point)
        container.add_widget(button_container)

        screen.add_widget(container)
        screen.open()

    def run_del_screen(self, value):
        # функции
        def back(value):
            screen.dismiss()

        def delete(value):
            if len(name.text) != 0:
                del_in_db(name.text)
                self.update_spisok()
                label.text = f'позиция {name.text} удалена'
                name.text = ''
            else:
                label.text = 'строка не может быть пустой'
        # окно удаления знчений
        screen = ModalView(size_hint=[1, 0.5], auto_dismiss=False)
        container = BoxLayout(orientation='vertical')
        button_container = BoxLayout(size_hint=[1, 0.3])

        label = Label(text='Здесь можно удалить позицию')
        name = TextInput(multiline=False, size_hint=[1, 0.4], font_size='30sp', hint_text='название позиции')
        save_btn = Button(text='удалить', on_release=delete)
        back_btn = Button(text='назад', on_release=back)

        button_container.add_widget(save_btn)
        button_container.add_widget(back_btn)

        container.add_widget(label)
        container.add_widget(name)
        container.add_widget(button_container)

        screen.add_widget(container)
        screen.open()


if __name__ == '__main__':
    MyApp().run()
