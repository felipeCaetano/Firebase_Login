import flet as ft
from gotrue.errors import AuthApiError

from generalcontrols import Body


class LogInPage(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(
            route="/login-user",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page = page
        self.supabase = supabase
        self.body = Body(
            title="Registra-BGI ENTRAR",
            btn_name="Login",
            msg1="Esqueceu a senha? ",
            msg2="Click aqui",
            route="/change-pass",
            func=self.log_user_in
        )

        self.controls = [self.body]

    def show_snack_bar(self, msg):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor='black'
        )
        self.page.snack_bar.open = True

    def log_user_in(self, event):
        if self.body.email.value != "" and self.body.password.value != "":
            try:
                data = self.supabase.auth.sign_in_with_password(
                    {
                        "email": self.body.email.value,
                        "password": self.body.password.value,
                    }
                )

                self.body.email.value = ""
                self.body.password.value = ""

                # acess_token = data.session.access_token
                # expires_in = data.session.expires_in
                # user_id = data.user.id
                # user_email = data.user.email
                # user_metadata = data.user.user_metadata
                self.page.update()

                self.page.go("/view-reg")
            except AuthApiError as e:
                if e.args[0] == "Invalid login credentials":
                    self.show_snack_bar("Login ou senha inválidos")
