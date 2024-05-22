import flet as ft

from app.generalcontrols import InspectionTile
from app.views.inspection_view import InspectionPage


class ViewerRegBodyController:
    def __init__(self, viewer_reg_body):
        self.viewer_reg_body = viewer_reg_body
        self.tab = self.viewer_reg_body.content.controls[1].controls[0]

    def populate_list_view(self):
        for i in range(9):
            list_tile = self.create_list_tile(9 - i)
            self.viewer_reg_body.content.controls[1].controls[0].tabs[
                0].content.controls.append(list_tile)

    def create_list_tile(self, index):
        return InspectionTile(index, self.viewer_reg_body.item_clicked)

    def item_clicked(self, event):
        print(event.control, "clicado!")

    def get_tab_name(self):
        tab_index = self._get_selected_tab_index()
        name = self.tab.tabs[tab_index].text
        return name

    def _get_selected_tab_index(self):
        return self.tab.selected_index


class MainPageController:
    def __init__(self, main_page):
        self.main_page = main_page

    def new_inspection(self, event, tab_name):
        self.main_page.page.data = tab_name
        self.main_page.page.update()
        rota = InspectionPage(self.main_page.page, self.main_page.supabase,
                              tab_name)
        self.main_page.page.views.append(rota)
        self.main_page.page.update()

    def show_drawer(self, event):
        self.main_page.drawer.open = True
        self.main_page.drawer.update()
