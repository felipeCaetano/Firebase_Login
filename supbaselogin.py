import os

import flet as ft
import gotrue
from dotenv import load_dotenv
from gotrue.errors import AuthApiError
from supabase import create_client

load_dotenv()


def get_supabase_object():
    url: str = os.environ['SUPABASE_URL']
    key: str = os.environ['SUPABASE_KEY']

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
    # "width": 400,
    # "height": 420,
    "border_radius": 8,
    "padding": 0,
}


class Body(ft.Container):
    def __init__(self, title, btn_name, msg1, msg2, route, func):
        super().__init__(**body_style)
        self.email = Input(password=False)
        self.password = Input(password=True)
        self.name = Input(password=False)
        self.content = ft.Column(
            spacing=4,
            controls=[
                ft.Image(src='assets/chesf.png', width=148, height=50),
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Text(
                    title, size=25, color="#55a271", weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=10, color=ft.colors.GREEN_ACCENT),
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),

                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
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
                                           weight=ft.FontWeight.BOLD
                                       ),
                                       on_click=lambda _: self.page.go(route)
                                   )
                               ]
                           )
                       ]),
            ]
        )
        # self.width = 280
        # self.height = 600
        self.padding = 12
        self.border_radius = 35
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.WHITE, ft.colors.GREEN_50],
        )
        if btn_name == 'Cadastrar':
            self.content.controls.insert(
                5,
                ft.Divider(height=10, color=ft.colors.TRANSPARENT))
            self.content.controls.insert(6, ft.Text("Seu Nome", size=12))
            self.content.controls.insert(7, self.name)


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
                data: gotrue.AuthResponse = self.supabase.auth.sign_in_with_password(
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


class ChangePass(ft.View):
    def __init__(self, page: ft.Page, supabase):
        super().__init__(
            route="/change-pass",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
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
                        size=25,
                        color="#55a271",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
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


class ViewerRegBody(ft.Container):
    def __init__(self, appbar: ft.AppBar):
        super().__init__(**body_style)
        self.appbar = appbar
        self.expand = True
        self.appbar.leading = ft.IconButton("menu")
        self.appbar.title = ft.Text("Leituras dos Disjuntores")
        self.appbar.bgcolor = ft.colors.GREEN_ACCENT_100
        self.content = ft.Column(
            expand=True,
            spacing=4,
            scroll=ft.ScrollMode.ALWAYS,
            controls=[
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Column(
                    controls=[
                        ft.Tabs(
                            animation_duration=300,
                            divider_color="black",
                            tabs=[
                                ft.Tab(
                                    text="BGI",
                                    content=ft.Column(spacing=2),
                                ),
                                ft.Tab(
                                    text="JRM",
                                    content=ft.Text("This is Tab 3"),
                                ),
                            ],
                        ),
                    ]
                ),
            ]
        )
        # self.width = 280
        # self.height = 640
        self.padding = 0
        self.border_radius = 5
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.WHITE, ft.colors.GREEN_50],
        )
        self.populate_list_view()

    def populate_list_view(self):
        for i in range(9):
            list_tile = ft.TextButton(
                style=ft.ButtonStyle(
                    shape=ft.ContinuousRectangleBorder()
                ),
                content=ft.ListTile(
                    leading=ft.CircleAvatar(content=ft.Text(f"{"FC"}")),
                    title=ft.Text(f"{8-i}/05/2024"),
                    subtitle=ft.Text("Inspeção Realizada"),
                    hover_color=ft.colors.LIGHT_BLUE_ACCENT_100,
                    on_click=self.item_clicked,
                )
            )
            self.content.controls[1].controls[0].tabs[0].content.controls.append(list_tile)

    def item_clicked(self, event):
        print(event.control, "clicado!")


class ViewRegs(ft.View):
    def __init__(self, page, supabase):
        super().__init__(
            route="/view-reg",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        self.page = page
        self.supabase = supabase
        self.page.appbar = ft.AppBar(bgcolor="green")
        self.page.floating_action_button = ft.FloatingActionButton(icon=ft.icons.ADD, on_click=self.new_inspection)
        self.body = ViewerRegBody(self.page.appbar)
        self.controls = [self.page.appbar, self.body, self.page.floating_action_button]
        self.spacing = 0
        self.padding = 0

    def new_inspection(self, event):
        sename = "JRM"
        view_cad: ft.View = ViewCad(self.page, self.supabase, sename)
        self.page.views.append(view_cad)
        # self.page.go(
        #     "/cadastrar-insp"
        # )
        self.page.route = view_cad
        self.page.update()


class PressureForm(ft.Container):
    def __init__(self, appbar, sename="SE BGI"):
        super().__init__(**body_style)
        self.appbar = appbar
        self.appbar.leading = ft.IconButton("menu")
        self.appbar.title = ft.Text(f"{sename} Cadastrar Leituras")
        self.appbar.bgcolor = ft.colors.GREEN_ACCENT_100
        controls_list = self.create_controls(sename)
        self.content = ft.Column(
            controls=controls_list
        )

    def create_controls(self, sename):
        contols_list = ft.Column()
        if sename == "BGI":
            pass
        if sename == "JRM":
            contols_list.controls=[
                    ft.Row(
                        controls=[
                            ft.Column(controls=[ft.Text("Data"), Input(password=False)]),
                            ft.Column(controls=[ft.Text("Hora"), Input(password=False)]),
                        ]
                    )
                ]
            return contols_list.controls


class ViewCad(ft.View):
    def __init__(self, page: ft.Page, supabase, sename="JRM"):
        super().__init__(
            route="/cadastrar-insp",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.page = page
        self.supabase = supabase
        self.page.appbar = ft.AppBar(bgcolor="green")
        self.body = PressureForm(self.page.appbar, sename)
        self.controls = [self.page.appbar, self.body]


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
    view_cad: ft.View = ViewCad(page, supabase)

    def route_change(event):
        page.views.clear()
        if page.route == "/create-user":
            page.views.append(create)
        if page.route == "/login-user":
            page.views.append(login)
        if page.route == "/change-pass":
            page.views.append(change_pass)
        if page.route == "/view-reg":
            page.views.append(view_reg)
        # if page.route == "/cadastrar-insp":
        #     page.views.append(view_cad)

        page.update()

    page.on_route_change = route_change
    page.go("/view-reg")


if __name__ == "__main__":
    ft.app(target=main)
