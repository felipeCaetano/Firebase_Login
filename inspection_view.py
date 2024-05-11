import datetime

import flet as ft

from disjuntor_view import Disjuntor
from generalcontrols import body_style, Input, InputWithSuffix, Button


class PressureForm(ft.Container):
    def __init__(self, page, sename="SE BGI"):
        super().__init__(**body_style)
        self.alignment = ft.alignment.top_center
        self.page = page
        self.appbar = self.page.appbar
        self.appbar.leading = ft.IconButton("menu")
        self.appbar.title = ft.Text(f"{sename} Cadastrar Leituras")
        self.appbar.bgcolor = ft.colors.GREEN_ACCENT_100
        controls_list = self.create_controls(sename)
        self.content = ft.Column(
            # alignment=ft.alignment.center,
            controls=controls_list
        )

    def create_controls(self, sename):
        def change_date(e):
            print(f"Date picker changed, value is {date_picker.value}")
            date_input_update()

        def date_input_update():
            date_input = contols_list.controls[0].controls[0].controls[1]
            date_input.value = str(
                date_picker.value.strftime("%d/%m/%Y")
            )[0:10]
            date_input.update()

        def date_picker_dismissed(e):
            print(f"Date picker dismissed, value is {date_picker.value}")

        def change_time(e):
            print(
                f"Time picker changed, value (minute) is {time_picker.value.minute}")
            time_input_update()

        def time_input_update():
            time_input = contols_list.controls[0].controls[1].controls[1]
            time_input.value = str(time_picker.value)
            time_input.update()

        def dismissed(e):
            print(f"Time picker dismissed, value is {time_picker.value}")

        time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=change_time,
            on_dismiss=dismissed,
        )

        date_picker = ft.DatePicker(
            on_change=change_date,
            on_dismiss=date_picker_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        self.page.overlay.append(time_picker)
        self.page.overlay.append(date_picker)
        self.page.update()
        suffix_button = ft.IconButton(
            ft.icons.CALENDAR_TODAY,
            on_click=lambda _: date_picker.pick_date()
        )
        date_field = InputWithSuffix(suffix_button)
        contols_list = ft.Column()
        if sename == "BGI":
            pass
        if sename == "JRM":
            contols_list.controls = [
                ft.Row(
                    controls=[
                        ft.Column(expand=2,
                                  controls=[
                                      ft.Text("Data"),
                                      date_field
                                  ]),
                        ft.Column(expand=2,
                                  controls=[
                                      ft.Text("Hora"),
                                      InputWithSuffix(
                                          ft.IconButton(
                                              icon=ft.icons.ACCESS_TIME,
                                              on_click=lambda
                                                  _: time_picker.pick_time()
                                          )
                                      )
                                  ]),
                        ft.Column(expand=1,
                                  controls=[
                                      ft.Text("Temperatura"),
                                      Input(password=False)]),
                    ]
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                Disjuntor("14V6", 3),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                Disjuntor("12T3", 1),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                Disjuntor("12M7", 1),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Row(
                    controls=[
                        Button("Enviar", self.save_form)
                    ]
                )
            ]
            return contols_list.controls

    def save_form(self, event):
        self.get_form_fields()

    def get_form_fields(self):
        data = self.content.controls[0].controls[0].controls[1].value
        hora = self.content.controls[0].controls[1].controls[1].value
        temp = self.content.controls[0].controls[2].controls[1].value
        disj1: Disjuntor = self.content.controls[2]
        disj2: Disjuntor = self.content.controls[4]
        disj3: Disjuntor = self.content.controls[6]
        try:
            press1 = disj1.get_press()
            press2 = disj2.get_press()
            press3 = disj3.get_press()
            print(data, hora, temp, press1, press2, press3, sep='\n')
        except Exception:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(str(Exception)))
            self.page.snack_bar.open = True
            self.page.update()
        # print(data, hora, temp, press1,press2, press3, sep='\n')


class InspectionPage(ft.View):
    def __init__(self, page: ft.Page, supabase, sename="JRM"):
        super().__init__(
            route="/cadastrar-insp",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.supabase = supabase
        self.page.appbar = ft.AppBar(bgcolor="green")
        self.body = PressureForm(self.page, sename)
        self.controls = [self.page.appbar, self.body]
