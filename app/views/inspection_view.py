import flet as ft

from email_server import EmailService
from generalcontrols import body_style, Input, InputWithSuffix, Button, PickDate, TimePicker
from views.disjuntor_view import Disjuntor

from daos.disjuntor_dao import DisjuntorDAO


class Controller:
    def __init__(self, form):
        self.ui = form

    def process_form(self):
        try:
            data, hora, temp, press1, press2, press3 = self.ui.get_form_fields()
            return True, data, hora, temp, press1, press2, press3
        except Exception as e:
            self.ui.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(e))
            )
            self.ui.page.snack_bar.open = True
            self.ui.page.update()
            return False, None, None, None, None, None, None


class PressureFormUI(ft.Container):
    def __init__(self, page, date_update, time_update, sename="SE BGI"):
        super().__init__(**body_style)
        self.page = page
        self.date_update = date_update
        self.time_update = time_update
        self.alignment = ft.alignment.top_center
        self.appbar = self.page.appbar
        self.customize_appbar(sename)
        self.time_picker = TimePicker(on_change=self.time_update)
        self.date_picker = PickDate(on_change=self.date_update)
        self.page.overlay.append(self.time_picker)
        self.page.overlay.append(self.date_picker)
        self.page.update()
        controls_list = self.create_controls(sename)
        self.content = ft.Column(controls=controls_list)

    def customize_appbar(self, sename):
        self.appbar.leading = ft.IconButton(ft.icons.MENU)
        self.appbar.title = ft.Text(f"SE {sename} Cadastrar Leituras")
        self.appbar.bgcolor = ft.colors.GREEN_ACCENT_100

    def create_controls(self, sename):
        contols_list = ft.Column()
        suffix_button = ft.IconButton(
            ft.icons.CALENDAR_TODAY,
            on_click=lambda _: self.date_picker.pick_date()
        )
        date_field = InputWithSuffix(suffix_button)
        if sename == "BGI":
            pass
        if sename == "JRM":
            dao = DisjuntorDAO()
            disjuntor_list = dao.get_disjuntores()
            print(f'{disjuntor_list=}')
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
                                                  _: self.time_picker.pick_time()
                                          )
                                      )
                                  ]),
                        ft.Column(
                            expand=1,
                            controls=[
                                ft.Text("Temperatura"),
                                Input(password=False)
                            ]
                        ),
                    ]
                ),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                Disjuntor("14V6", 3),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                Disjuntor("12T3", 1),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                Disjuntor("12M7", 1),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
            ]
            return contols_list.controls

    def get_form_fields(self):
        press1 = press2 = press3 = None
        data = self.content.controls[0].controls[0].controls[1].value
        hora = self.content.controls[0].controls[1].controls[1].value
        temp = self.content.controls[0].controls[2].controls[1].value
        disj1: Disjuntor = self.content.controls[2]
        print("DISJUNTOR: ", disj1)
        disj2: Disjuntor = self.content.controls[4]
        disj3: Disjuntor = self.content.controls[6]
        press1 = disj1.get_press()
        press2 = disj2.get_press()
        press3 = disj3.get_press()
        return data, hora, temp, press1, press2, press3

    def clear_fields(self):
        self.content.controls[0].controls[0].controls[1].value = ""
        self.content.controls[0].controls[1].controls[1].value = ""
        self.content.controls[0].controls[2].controls[1].value = ""
        self.content.controls[2].clear_press()
        self.content.controls[4].clear_press()
        self.content.controls[6].clear_press()
        self.page.update()


class InspectionPage(ft.View):
    def __init__(self, page: ft.Page, supabase, sename="JRM"):
        super().__init__(
            route="/cadastrar-insp",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.supabase = supabase
        self.sename = sename
        self.page.appbar = ft.AppBar(bgcolor=ft.colors.GREEN)
        self.body = PressureFormUI(self.page, self.date_input_update, self.time_input_update, sename)
        self.controller = Controller(self.body)
        self.email_service = EmailService()
        self.controls = [
            self.page.appbar,
            self.body,
            ft.Row(controls=[Button("Enviar", self.save_form)])]

    def date_input_update(self, event):
        date_input = self.body.content.controls[0].controls[0].controls[1]
        date_input.value = str(
            self.body.date_picker.value.strftime("%d/%m/%Y"))[0:10]
        date_input.update()

    def time_input_update(self, event):
        time_input = self.body.content.controls[0].controls[1].controls[1]
        time_input.value = str(self.body.time_picker.value)
        time_input.update()

    def save_form(self, event):
        status, data, hora, temp, press1, press2, press3 = self.controller.process_form()
        if status:
            self.email_service.send_mail(self.sename, data, hora, temp, press1, press2, press3)
            self.body.clear_fields()
