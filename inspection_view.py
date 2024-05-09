import datetime

import flet as ft

from generalcontrols import body_style, Input


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
            alignment=ft.alignment.center,
            controls=controls_list
        )

    def create_controls(self, sename):
        pickednum = 0

        def datepicked(e):
            date_picker.pick_date()
            contols_list.controls[0].controls[1].controls[1].focus()

        def change_date(e):
            print(f"Date picker changed, value is {date_picker.value}")
            date_input_update()

        def date_input_update():
            date_input = contols_list.controls[0].controls[0].controls[1]
            date_input.value = date_picker.value
            date_input.update()

        def date_picker_dismissed(e):
            print(f"Date picker dismissed, value is {date_picker.value}")

        date_picker = ft.DatePicker(
            on_change=change_date,
            on_dismiss=date_picker_dismissed,
            first_date=datetime.datetime(2023, 10, 1),
            last_date=datetime.datetime(2024, 10, 1),
        )

        self.page.overlay.append(date_picker)

        contols_list = ft.Column()
        if sename == "BGI":
            pass
        if sename == "JRM":
            contols_list.controls = [
                ft.Row(
                    expand=False,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Data"),
                                Input(
                                    on_focus=datepicked,
                                    password=False,
                                )
                            ]),
                        ft.Column(
                            controls=[ft.Text("Hora"), Input(password=False)]),
                    ]
                )
            ]
            return contols_list.controls


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
