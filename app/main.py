import flet as ft

from views.adddisjuntor_view import DisjuntorPage
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

    views = {
        "/create-user": CreatePage(page, supabase),
        "/login-user":  LogInPage(page, supabase),
        "/change-pass": ChangePass(page, supabase),
        "/cadastrar-insp": InspectionPage(page, supabase),
        "/cadastrar-disj": DisjuntorPage(page, supabase),
        "/view-reg": MainPage(page, supabase),
    }
    def route_change(event):
        page.views.clear()
        view = views.get(page.route)
        if view:
            page.views.append(view)
        page.update()

    def view_pop(event):
        page.views.pop()
        if page.views:
            top_view = page.views[-1]
            page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go("/view-reg")


if __name__ == "__main__":
    ft.app(target=main)
