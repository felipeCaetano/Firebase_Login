import flet as ft
from gotrue.errors import AuthApiError

from generalcontrols import Body

from app.auth import AuthService
from app.controllers.login_controller import LogInController


class LogInPage(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(
            route="/login-user",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page = page
        self.auth_service = AuthService(supabase)
        self.controller = LogInController(self.auth_service, self)
        self.body = Body(
            title="Registra-BGI ENTRAR",
            btn_name="Login",
            msg1="Esqueceu a senha? ",
            msg2="Click aqui",
            route="/change-pass",
            func=self.handle_login
        )

        self.controls = [self.body]

    def show_snack_bar(self, msg):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor=ft.colors.BLACK
        )
        self.page.snack_bar.open = True

    def handle_login(self, event):
        email_value = self.body.email.value
        password_value = self.body.password.value
        self.controller.log_user_in(email_value, password_value)

    def clear_inputs(self):
        self.body.email.value = ""
        self.body.password.value = ""
