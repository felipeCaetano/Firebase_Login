import flet as ft
from gotrue.errors import AuthApiError

from generalcontrols import Body


class CreatePage(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(
            route="/create-user",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.page = page
        self.supabase = supabase
        self.body = Body(
            title="Registra-BGI  Cadastre-se",
            btn_name="Cadastrar",
            msg1="Tem uma conta? ",
            msg2="Entrar",
            route="/login-user",
            func=self.create_user
        )

        self.controls = [self.body]

    def create_user(self, event):
        try:
            if self.body.email.value != "" and self.body.password.value != "":
                res = self.supabase.auth.sign_up(
                    {
                        "email": self.body.email.value,
                        "password": self.body.password.value,
                    }
                )

                self.body.email.value = ""
                self.body.password.value = ""
                self.body.name.value = ""
                self.update()
            if self.body.email.value == "" or self.body.password == "":
                self.show_snack_bar("Informe e-mail e senha!")
            self.page.update()
        except AuthApiError as e:
            if e.args[0] == "Signup requires a valid password":
                self.show_snack_bar("Informe a senha!")
            self.page.update()

    def show_snack_bar(self, msg):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor='black'
        )
        self.page.snack_bar.open = True
