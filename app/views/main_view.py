import flet as ft

from generalcontrols import body_style

from app.controllers.bodycontroller import ViewerRegBodyController, \
    MainPageController
from app.generalcontrols import NavigationDrawer


class ViewerRegBody(ft.Container):
    def __init__(self, appbar: ft.AppBar):
        super().__init__(**body_style)
        self.appbar = appbar
        self.expand = True
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
                            divider_color=ft.colors.BLACK,
                            tabs=[
                                ft.Tab(
                                    text="BGI",
                                    content=ft.Column(spacing=2)
                                ),
                                ft.Tab(
                                    text="JRM",
                                    content=ft.Column(spacing=2)
                                ),
                            ],
                        ),
                    ]
                ),
            ]
        )
        self.padding = 0
        self.border_radius = 5
        self.gradient = ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=[ft.colors.WHITE, ft.colors.GREEN_50],
        )
        self.controller = ViewerRegBodyController(self)
        self.controller.populate_list_view()

    def item_clicked(self, event):
        self.controller.item_clicked(event)


class MainPage(ft.View):
    def __init__(self, page, supabase):
        super().__init__(
            route="/view-reg",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        self.page = page
        self.supabase = supabase
        self.drawer = NavigationDrawer(on_change=self.on_nav_change)
        self.page.appbar = self.create_appbar()
        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ADD, on_click=self.new_inspection)
        self.body = ViewerRegBody(self.page.appbar)
        self.controls = [self.page.appbar, self.body,
                         self.page.floating_action_button]
        self.spacing = 0
        self.padding = 0
        self.controller = MainPageController(self)

    def create_appbar(self):
        appbar = ft.AppBar()
        appbar.leading = ft.IconButton(
            ft.icons.MENU,
            on_click=self.show_drawer
        )
        appbar.title = ft.Text("Leituras dos Disjuntores")
        appbar.bgcolor = ft.colors.GREEN_ACCENT_100
        return appbar

    def create_nav_drawer(self):
        return ft.NavigationDrawer(
        )

    def on_nav_change(self, event):
        self.drawer.open = False
        self.drawer.update()
        self.page.route = "/cadastrar-disj"
        self.page.go(self.page.route)

    def new_inspection(self, event):
        tab_name = self.body.controller.get_tab_name()
        self.controller.new_inspection(event, tab_name)

    def show_drawer(self, event):
        self.drawer.open = True
        self.drawer.update()
