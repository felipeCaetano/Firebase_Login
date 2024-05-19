import flet as ft

from generalcontrols import Input


def _create_pressure_fields(press_num):
    row = ft.Row()
    for i in range(press_num):
        if press_num > 1:
            row.controls.append(ft.Column(
                controls=[
                    ft.Text(f"Fase {'ABC'[i]}"),
                    Input(password=None, width=45)
                ]
            ))
        else:
            row.controls.append(Input(password=None, width=45))
    return row


class DisjuntorUI(ft.Container):
    def __init__(self, name, press_num):
        super().__init__()
        self.name = name
        self.press_num = press_num
        self.press_fields = _create_pressure_fields(self.press_num)
        self.content = ft.Column(
            controls=[
                ft.Text(self.name, weight=ft.FontWeight.BOLD),
                self.press_fields]
        )


class Controller:
    def __init__(self, ui):
        self.ui = ui

    def get_press(self):
        press = []
        if self.ui.press_num > 1:
            for col in self.ui.press_fields.controls:
                press.append(col.controls[1].value)
        else:
            press.append(self.ui.press_fields.controls[0].value)
        if any([value == "" for value in press]):
            raise Exception("Os campos não podem estar vazios!")
        return press

    def clear_press(self):
        if self.ui.press_num > 1:
            for col in self.ui.press_fields.controls:
                col.controls[1].value = ""
        else:
            self.ui.press_fields.controls[0].value = ""


class Disjuntor(ft.Container):
    def __init__(self, name, press_num):
        super().__init__()
        self.ui = DisjuntorUI(name, press_num)
        self.controller = Controller(self.ui)
        self.content = self.ui.content

    def get_press(self):
        self.controller.get_press()

    def clear_press(self):
        self.controller.clear_press()

    def __repr__(self):
        press_values = self.controller.get_press()
        press_values_str = ', '.join(press_values)
        return f"Disjuntor {self.ui.name}, {press_values_str}\n"