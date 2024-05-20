from functools import partial

import flet as ft
import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyAhiuD4LCCFLKxy7pUgjl2EpzY9bYnucx4",
    "authDomain": "registra-bgi.firebaseapp.com",
    "projectId": "registra-bgi",
    "storageBucket": "registra-bgi.appspot.com",
    "messagingSenderId": "607130284346",
    "appId": "1:607130284346:web:4477872dd79292ec89a003",
    "measurementId": "G-0TXN2K2Q8F",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


class UserWidget(ft.Column):
    def __init__(self, title, sub_title, btn_name, func):
        super().__init__()
        self.func = func
        self.horizontal_alignment = ft.MainAxisAlignment.CENTER
        self.title = title
        self.sub_title = sub_title
        self.btn_name = btn_name
        self._sign_in = ft.Container(
            content=ft.ElevatedButton(
                on_click=partial(self.func),
                content=ft.Text(
                    self.btn_name,
                    weight=ft.FontWeight.BOLD,
                    size=11
                ),
                style=ft.ButtonStyle(
                    shape={"": ft.RoundedRectangleBorder(radius=8)},
                    color={
                        "": 'white'
                    },
                    bgcolor={"": 'black'}
                ),
                height=48,
                width=255,
            )
        )
        self._title = ft.Container(
            alignment=ft.alignment.center,
            padding=15,
            content=ft.Text(
                self.title,
                size=25,
                text_align='center',
                weight='bold',
                color="black"
            )
        )
        self._sub_title = ft.Container(
            alignment=ft.alignment.center,
            content=ft.Text(
                self.sub_title,
                size=12,
                text_align='center',
                weight='bold',
                color="black"
            )
        )
        self.controls = [
            ft.Row(
                alignment='center',
                spacing=4,
                controls=[
                    ft.Image(
                        src="../assets/chesf.png",
                        width=148,
                        height=50
                    ),]),
            self._title,
            self._sub_title,
            ft.Column(
                spacing=12,
                controls=[
                    self.input_text_field('E-mail', False),
                    self.input_text_field('Senha', True),
                ],
            ),
            ft.Container(padding=5),
            self._sign_in,
            ft.Container(padding=5),
            ft.Column(
                horizontal_alignment='center',
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "Or continue with",
                            size=10,
                            color='black'
                        )
                    ),
                    self.SignInOption("../assets/microsoft.png", "Microsoft"),
                    self.SignInOption("../assets/google.png", "Google")
                ]
            )
        ]

    def input_text_field(self, text, hide):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.TextField(
                hint_text=text,
                height=48,
                width=255,
                bgcolor="#f0f3f6",
                text_size=12,
                color='black',
                border_radius=15,
                border_color='transparent',
                filled=True,
                cursor_color='black',
                hint_style=ft.TextStyle(
                    size=11,
                    color='black',
                ),
                password=hide
            )
        )

    def SignInOption(self, path, name):
        return ft.Container(
            content=ft.ElevatedButton(
                style=ft.ButtonStyle(
                    shape={"": ft.RoundedRectangleBorder(radius=8)},
                    color={"": 'white'},
                    bgcolor={"": '#f0f3f6'}
                ),
                content=ft.Row(
                    alignment='center',
                    spacing=4,
                    controls=[
                        ft.Image(
                            src=path,
                            width=48,
                            height=48
                        ),
                        ft.Text(
                            name,
                            color='black',
                            size=10,
                            width='bold',
                        ),
                    ],
                )
            ),
        )


def main(page: ft.Page):
    page.title = "Flet With Firebase"
    page.bgcolor = '#f0f3f6'
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER

    def _main_column():
        return ft.Container(
            width=280, height=600, bgcolor='white', padding=12,
            border_radius=35,
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_center,
                end=ft.alignment.bottom_center,
                colors=[ft.colors.BLUE, ft.colors.YELLOW],
            ),
            content=ft.Column(
                spacing=20,
                horizontal_alignment='center',
            )
        )

    def _register_user(event):
        try:
            auth.create_user_with_email_and_password(
                _register_.controls[3].controls[0].content.value,
                _register_.controls[3].controls[1].content.value,
            )
            print("registration ok")
        except Exception as e:
            print(e)

    def _sign_in(event):
        try:
            user = auth.sign_in_with_email_and_password(
                _sign_in_.controls[3].controls[0].content.value,
                _sign_in_.controls[3].controls[1].content.value,
            )
            info = auth.get_account_info(user['idToken'])
            print(info)
            _sign_in_.controls[3].controls[0].content.value = None
            _sign_in_.controls[3].controls[1].content.value = None
        except Exception as e:
            print("Wrong e-mail or password")

    _sign_in_ = UserWidget(
        "Registra-BGI",
        "Enter your account details bellow",
        "Sign In",
        _sign_in
    )
    _register_ = UserWidget(
        "Registra-BGI",
        "Register your Email and Password bellow.",
        "Register",
        _register_user
    )

    _sign_in_main = _main_column()
    _sign_in_main.content.controls.append(ft.Container(padding=15))
    _sign_in_main.content.controls.append(_sign_in_)

    _reg_main = _main_column()
    _reg_main.content.controls.append(ft.Container(padding=15))
    _reg_main.content.controls.append(_register_)

    page.add(
        ft.Row(
            alignment='center',
            vertical_alignment='center',
            spacing=25,
            controls=[
                _sign_in_main,
                #_reg_main
            ]
        )
    )


if __name__ == '__main__':
    ft.app(target=main, assets_dir='../assets')
