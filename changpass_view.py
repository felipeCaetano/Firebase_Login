import flet as ft
import gotrue.errors

from generalcontrols import Input, Button


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
        except gotrue.errors.AuthApiError as e:
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
