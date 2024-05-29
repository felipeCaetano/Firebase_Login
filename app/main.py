import flet as ft

from app.views.adddisjuntor_view import DisjuntorPage
from views.changpass_view import ChangePass
from views.inspection_view import InspectionPage
from views.login_view import LogInPage
from views.main_view import MainPage
from views.register_view import CreatePage
from supabase_login import get_supabase_object


def main(page: ft.Page):
    theme = ft.Theme()
    theme.page_transitions.macos = ft.PageTransitionTheme.NONE
    page.theme = theme
    page.title = "Registra Bongi"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#202020"

    supabase = get_supabase_object()
    create: ft.View = CreatePage(page, supabase)
    login: ft.View = LogInPage(page, supabase)
    change_pass: ft.View = ChangePass(page, supabase)
    view_reg: ft.View = MainPage(page, supabase)
    view_cad: ft.View = InspectionPage(page, supabase)
    view_disj: ft.View = DisjuntorPage(page, supabase)

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
        if page.route == "/cadastrar-insp":
            page.views.append(view_cad)
        if page.route == "/cadastrar-disj":
            page.views.append(view_disj)

        page.update()

    def view_pop(event):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/view-reg")


if __name__ == "__main__":
    ft.app(target=main)
