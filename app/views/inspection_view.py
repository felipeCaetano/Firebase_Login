import flet as ft

from email_server import EmailService
from generalcontrols import body_style, Input, InputWithSuffix, Button, \
    PickDate, TimePicker
from views.disjuntor_view import Disjuntor

from daos.disjuntor_dao import DisjuntorDAO

from app.generalcontrols import LeadingLine


class Controller:
    def __init__(self, form):
        self.ui = form

    def process_form(self):
        try:
            fields = self.get_form_fields()
            return True, *fields
        except Exception as e:
            self.ui.page.snack_bar = ft.SnackBar(
                content=ft.Text(str(e))
            )
            self.ui.page.snack_bar.open = True
            self.ui.page.update()
            return False, *(None,) * len(fields)

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
        self.content = controls_list

    def customize_appbar(self, sename):
        self.appbar.leading = ft.IconButton(ft.icons.MENU)
        self.appbar.title = ft.Text(f"SE {sename} Cadastrar Leituras")
        self.appbar.bgcolor = ft.colors.GREEN_ACCENT_100

    def create_controls(self, sename):
        contols_list = ft.Column()
        dao = DisjuntorDAO()
        contols_list.controls.append(
            LeadingLine(self.date_picker, self.time_picker)
        )
        disjuntor_list = dao.get_disjuntores_by_se(sename)
        for disjuntor in disjuntor_list:
            contols_list.controls.extend(
                [ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                 Disjuntor(disjuntor[2], disjuntor[3])]
            )
        return contols_list


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
        self.body = PressureFormUI(
            self.page,
            self.date_input_update,
            self.time_input_update,
            self.page.data
        )
        self.controller = Controller(self.body)
        self.email_service = EmailService()
        self.controls = [
            self.page.appbar,
            self.body,
            ft.Row(controls=[Button("Enviar", self.save_form)])]
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
            print(data, hora, temp, *press)
            self.email_service.send_mail(self.sename, data, hora, temp, press)
            self.controller.clear_fields()
