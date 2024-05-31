import flet as ft
from daos.disjuntor_dao import DisjuntorDAO
from email_server import EmailService
from generalcontrols import LeadingLine
from generalcontrols import body_style, Button, PickDate, TimePicker
from views.disjuntor_view import Disjuntor

from daos.inspecao_dao import InspectionDAO


class InspectionController:
    def __init__(self, form, sename):
        self.inspection_dao = InspectionDAO()
        self.ui = form
        self.sename = sename

    def create_controls(self):
        controls_list = ft.Column()
        disjuntor_list = self.get_disjuntors_list()
        if disjuntor_list:
            controls_list.controls.append(
                LeadingLine(self.ui.date_picker, self.ui.time_picker)
            )
            for disjuntor in disjuntor_list:
                controls_list.controls.extend(
                    [ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                     Disjuntor(disjuntor[2], disjuntor[3])]
                )
        else:
            controls_list.controls.append(
                ft.Text("Não existem Disjuntores Cadastrados.")
            )
        self.ui.content.controls = controls_list.controls

    def get_disjuntors_list(self):
        dao = DisjuntorDAO()
        return dao.get_disjuntores_by_se(self.sename)

    def process_form(self):
        try:
            fields = self.get_form_fields()
            return True, *fields
        except Exception as e:
            self.show_snackbar(str(e))
            return False, *(None,) * len(fields)

    def show_snackbar(self, e):
        self.ui.page.snack_bar = ft.SnackBar(content=ft.Text(str(e)))
        self.ui.page.snack_bar.open = True
        self.ui.page.update()

    def get_form_fields(self):
        fields = []

        def extract_fields(controls):
            for control in controls:
                if isinstance(control, ft.TextField):
                    fields.append(control.value)
                elif isinstance(control, Disjuntor):
                    fields.append(control)
                elif hasattr(control, 'controls'):
                    extract_fields(control.controls)

        extract_fields(self.ui.content.controls)
        return fields

    def clear_fields(self):
        def clear(controls):
            for control in controls:
                if isinstance(control, ft.TextField):
                    control.value = ""
                elif isinstance(control, Disjuntor):
                    control.clear_press()
                elif hasattr(control, 'controls'):
                    clear(control.controls)

        clear(self.ui.content.controls)
        self.ui.page.update()

    def save_to_db(self, sename, data, hora, temp, press):
        self.inspection_dao.add_inspection(sename, data, hora, temp, press)


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
        self.content = ft.Column()

    def customize_appbar(self, sename):
        self.appbar.title = ft.Text(
            f"SE {sename} Cadastrar Leituras",
            size=14
        )
        self.appbar.bgcolor = ft.colors.GREEN_ACCENT_100


class InspectionPage(ft.View):
    def __init__(self, page: ft.Page, supabase, sename="BGI"):
        super().__init__(
            route="/cadastrar-insp",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.supabase = supabase
        self.sename = sename
        self.page.appbar = ft.AppBar(bgcolor=ft.colors.GREEN)
        self.body = PressureFormUI(
            self.page,
            self.date_input_update,
            self.time_input_update,
            self.page.data
        )
        self.controller = InspectionController(self.body, self.sename)
        self.controller.create_controls()
        self.email_service = EmailService()
        self.controls = [self.page.appbar, self.body]
        if len(self.body.content.controls) > 1:
            self.controls.append(
                ft.Row(controls=[Button("Enviar", self.save_form)])
            )
        self.page.update()

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
        status, data, hora, temp, *press = self.controller.process_form()
        if status:
            # self.email_service.send_mail(self.sename, data, hora, temp, press)
            self.controller.save_to_db(self.sename, data, hora, temp, press)
            self.controller.clear_fields()
            self.page.data = {
                "data": data,
                "hora": hora,
                "temp": temp,
                "press": press
            }
            self.page.update()
            self.page.views.pop()
            top_view = self.page.views[-1]
            top_view.controller.populate_list_view()
            self.page.go(top_view.route)

