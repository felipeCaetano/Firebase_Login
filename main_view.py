import flet as ft

from generalcontrols import body_style


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
                    title=ft.Text(f"{8 - i}/05/2024"),
                    subtitle=ft.Text("Inspeção Realizada"),
                    hover_color=ft.colors.LIGHT_BLUE_ACCENT_100,
                    on_click=self.item_clicked,
                )
            )
            self.content.controls[1].controls[0].tabs[
                0].content.controls.append(list_tile)

    def item_clicked(self, event):
        print(event.control, "clicado!")


class MainPage(ft.View):
    def __init__(self, page, supabase):
        super().__init__(
            route="/view-reg",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        self.page = page
        self.supabase = supabase
        self.page.appbar = ft.AppBar(bgcolor="green")
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.new_inspection)
        self.body = ViewerRegBody(self.page.appbar)
        self.controls = [self.page.appbar, self.body,
                         self.page.floating_action_button]
        self.spacing = 0
        self.padding = 0

    def new_inspection(self, event):
        sename = "JRM"
        # view_cad: ft.View = ViewCad(self.page, self.supabase, sename)
        self.page.go(
            "/cadastrar-insp"
        )