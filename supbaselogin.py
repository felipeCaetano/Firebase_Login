import os
import flet as ft
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_supabase_object():
    url: str = os.environ["SUPABASE_URL"]
    key: str = os.environ["SUPABASE_KEY"]

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
                ft.Text(title, size=21, color="#55a271"),
                ft.Divider(height=5, color=ft.colors.TRANSPARENT),
                ft.Divider(height=5, color=ft.colors.WHITE10),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Email", size=10),
                self.email,
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text("Password", size=10),
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
            title="SuperBase - Log in user",
            btn_name="Login",
            msg1="Forgot Password? ",
            msg2="Click here",
            route="/login-user",
            func=self.log_user_in
        )

        self.controls = [self.body]

    def log_user_in(self, event):
        if self.body.email.value != "" and self.body.password != "":
            data = self.supabase.auth.sign_in_with_password(
                {
                    "email": self.body.email.value,
                    "password": self.body.password.value,
                }
            )
            self.body.email.value = ""
            self.body.password = ""
            self.update()


class CreatePage(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(route="/create-user",
                         vertical_alignment="center",
                         horizontal_alignment="center")
        self.page = page
        self.supabase = supabase
        self.body = Body(
            title="SuperBase - Sign in user",
            btn_name="Create Account",
            msg1="Have an account?",
            msg2="Sign In",
            route="/login-user",
            func=self.create_user
        )

        self.controls = [self.body]

    def create_user(self, event):
        if self.body.email.value != "" and self.body.password != "":
            res = self.supabase.auth.sign_up(
                {
                    "email": self.body.email.value,
                    "password": self.body.password.value,
                }
            )
            self.body.email.value = ""
            self.body.password = ""
            self.update()


def main(page: ft.Page):
    theme = ft.Theme()
    theme.page_transitions.macos = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.bgcolor = "#202020"
    supabase = get_supabase_object()
    create: ft.View = CreatePage(page, supabase)
    login: ft.View = LogInPage(page, supabase)

    def route_change(route):
        page.views.clear()
        if page.route == "/create-user":
            page.views.append(create)
        if page.route == "/login-user":
            page.views.append(login)

        page.update()

    page.on_route_change = route_change
    page.go("/create-user")


if __name__ == "__main__":
    ft.app(target=main)
