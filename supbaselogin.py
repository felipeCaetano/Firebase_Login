import os
import traceback

import flet as ft
from gotrue.errors import AuthApiError
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_supabase_object():
    url: str = "https://fxoyfmdeqmbncgzedrsq.supabase.co"
    key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ4b3lmbWRlcW1ibmNnemVkcnNxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQ0ODYyOTUsImV4cCI6MjAzMDA2MjI5NX0.bZ_B7fO6T0eLOvVpy6iKSI_0obSowxxp21Z82qqRs9A"

    supabase = create_client(url, key)
    return supabase


input_style = {
    "height": 38,
    "focused_border_color": "#55a271",
    "border_radius": 5,
    "cursor_height": 16,
    "cursor_color": "#55a271",
    "content_padding": 10,
    "border_width": 1.5,
    "text_size": 12,
}


class Input(ft.TextField):
    def __init__(self, password):
        super().__init__(**input_style, password=password)


button_style = {
    "expand": True,
    "height": 38,
    "bgcolor": "#55a271",
    "style": ft.ButtonStyle(shape={"": ft.RoundedRectangleBorder(radius=5)}),
    "color": "white",

}


class Button(ft.ElevatedButton):
    def __init__(self, text, function):
        super().__init__(**button_style, text=text, on_click=function)


body_style = {
    "width": 400,
    "height": 420,
    "border_radius": 8,
    "padding": 10,
}


class Body(ft.Container):
    def __init__(self, title, btn_name, msg1, msg2, route, func):
        super().__init__(**body_style)
        self.email = Input(password=False)
        self.password = Input(password=True)
        self.content = ft.Column(
            spacing=4,
            controls=[
                ft.Image(src='assets/chesf.png', width=148, height=50),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text(title, size=25, color="#55a271", weight='bold',
                        text_align='center'),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Divider(height=10, color=ft.colors.GREEN_ACCENT),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                ft.Text("Email", size=12),
                self.email,
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Password", size=12),
                self.password,
                ft.Divider(height=15, color=ft.colors.TRANSPARENT),
                ft.Row(controls=[Button(btn_name, func)]),
                ft.Divider(height=25, color=ft.colors.TRANSPARENT),
                ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                       controls=[
                           ft.Text(
                               msg1, size=12, opacity=.7,
                               spans=[
                                   ft.TextSpan(
                                       msg2,
                                       style=ft.TextStyle(
                                           weight='bold'),
                                       on_click=lambda _: self.page.go(route)
                                   )
                               ]
                           )
                       ]),
            ]
        )
        self.width = 280
        self.height = 600
        self.padding = 12
        self.border_radius = 35
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.WHITE, ft.colors.GREEN_50],
        )


class LogInPage(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(
            route="/login-user",
            vertical_alignment='center',
            horizontal_alignment='center'
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
                self.page.data = data
                self.page.go("/view-reg")
            except AuthApiError as e:
                print(e)
                if e.args[0] == "Invalid login credentials":
                    self.show_snack_bar("Login ou senha inválidos")
            self.page.update()


class ChangePass(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(
            route="/change-pass",
            vertical_alignment='center',
            horizontal_alignment='center'
        )
        self.page = page
        self.supabase = supabase
        self.email = Input(password=False)
        self.body = ft.Container(
            width=280,
            height=600,
            padding=12,
            border_radius=35,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.WHITE, ft.colors.GREEN_50]
            ),
            content=ft.Column(
                spacing=4,
                controls=[
                    ft.Image(
                        src='assets/chesf.png', width=148, height=50
                    ),
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.Text(
                        "Nova Senha",
                        size=25, color="#55a271",
                        weight='bold',
                        text_align='center'
                    ),
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.Divider(height=10, color=ft.colors.GREEN_ACCENT),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Text("Email", size=12),
                    self.email,
                    ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                    ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            Button("Enviar", self.reset_password)
                        ]
                    ),
                    ft.Divider(height=25, color=ft.colors.TRANSPARENT),
                    ft.Row(
                        controls=[
                            ft.Text(
                                "Você receberá um email para continuar",
                                size=10)
                        ]
                    )
                ]
            )
        )
        self.controls = [self.body]

    def reset_password(self, event):
        try:
            self.supabase.auth.reset_password_email(self.email.value)
            self.page.go('/login-user')
        except AuthApiError as e:
            if e.args[0] == "Password recovery requires an email":
                self.show_snack_bar("Insira seu email!")
            if e.args[0] == "Unable to validate email address: invalid format":
                self.show_snack_bar("Formato de email inválido!")
            self.page.update()

    def show_snack_bar(self, msg):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor='black'
        )
        self.page.snack_bar.open = True


class CreatePage(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(
            route="/create-user",
            vertical_alignment="center",
            horizontal_alignment="center"
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
                print("Criando usuário")
                res = self.supabase.auth.sign_up(
                    {
                        "email": self.body.email.value,
                        "password": self.body.password.value,
                    }
                )
                self.body.email.value = ""
                self.body.password = ""
                self.update()
            if self.body.email.value == "" or self.body.password == "":
                self.show_snack_bar("Informe e-mail e senha!")
            self.page.update()
        except AuthApiError as e:
            print(e)
            if e.args[0] == "Signup requires a valid password":
                self.show_snack_bar("Informe a senha!")
            self.page.update()

    def show_snack_bar(self, msg):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(msg),
            bgcolor='black'
        )
        self.page.snack_bar.open = True


class ViewRegs(ft.View):
    def __init__(self, page, supabase):
        super().__init__(
            route="/view-reg",
            vertical_alignment='center',
            horizontal_alignment='center')
        self.page = page
        self.supabase = supabase


def main(page: ft.Page):
    theme = ft.Theme()
    theme.page_transitions.macos = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.title = "Flet With Supabase"
    # page.bgcolor = '#f0f3f6'
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#202020"
    page.snack_bar = ft.SnackBar(
        content=ft.Text("Hello, world!"),
        action="Alright!",
    )

    supabase = get_supabase_object()
    create: ft.View = CreatePage(page, supabase)
    login: ft.View = LogInPage(page, supabase)
    change_pass: ft.View = ChangePass(page, supabase)
    view_reg: ft.View = ViewRegs(page, supabase)

    def route_change(route):
        page.views.clear()
        if page.route == "/create-user":
            page.views.append(create)
        if page.route == "/login-user":
            page.views.append(login)
        if page.route == "/change-pass":
            page.views.append(change_pass)
        if page.route == "/view-reg":
            page.views.append(view_reg)

        page.update()

    page.on_route_change = route_change
    page.go("/create-user")


if __name__ == "__main__":
    ft.app(target=main)
