import datetime

import flet as ft

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
    def __init__(self, password, width=255):
        super().__init__(**input_style, password=password, width=width)


class InputWithSuffix(ft.TextField):
    def __init__(self, suffix: ft.IconButton):
        super().__init__(**input_style, suffix=suffix)


class LeadingLine(ft.Row):
    date_suffix_button = ft.IconButton(ft.icons.CALENDAR_TODAY)
    time_suffix_button = ft.IconButton(ft.icons.ACCESS_TIME)
    date_field = InputWithSuffix(date_suffix_button)
    time_field = InputWithSuffix(time_suffix_button)

    def __init__(self, date_picker: ft.DatePicker, time_picker: ft.TimePicker):
        super().__init__()
        self.date_picker = date_picker
        self.time_picker = time_picker
        self.date_field.suffix.on_click = self.on_pick_date
        self.time_field.suffix.on_click = self.on_pick_time
        self.controls = [
            ft.Column(expand=2, controls=[ft.Text("Data"), self.date_field]),
            ft.Column(expand=2, controls=[ft.Text("Hora"), self.time_field]),
            ft.Column(expand=1,
                      controls=[ft.Text("Temp."), Input(password=False)])
        ]

    def on_pick_date(self, event):
        self.date_picker.pick_date()

    def on_pick_time(self, event):
        self.time_picker.pick_time()


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
                ft.Image(src='../assets/chesf.png', width=148, height=50),
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


class PickDate(ft.DatePicker):
    def __init(self, on_change):
        super().__init__(on_change=on_change)
        self.first_date = datetime.datetime(2023, 10, 1),
        self.last_date = datetime.datetime(2024, 10, 1),


class TimePicker(ft.TimePicker):
    def __init__(self, on_change):
        super().__init__(on_change=on_change)
        self.confirm_text = "Confirmar"
        self.error_invalid_text = "Hora fora de alcance"
        self.help_text = "Escolha a hora."


class NavigationDrawer(ft.NavigationDrawer):
    def __init__(self, on_change):
        super().__init__(on_change=on_change)
        self.controls = [
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Cadastrar Disjunttores",
                icon=ft.icons.DYNAMIC_FORM_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DYNAMIC_FORM),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ]


class InspectionTile(ft.TextButton):
    def __init__(self, inspection, function):
        super().__init__(
            style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder())
        )
        self.inspection = inspection
        self.content = ft.ListTile(
            leading=ft.CircleAvatar(content=ft.Text(f"{"FC"}")),
            title=ft.Text(f"{inspection[2]}"),
            subtitle=ft.Text("Inspeção Realizada"),
            hover_color=ft.colors.LIGHT_BLUE_ACCENT_100,
            on_click=function,
        )
