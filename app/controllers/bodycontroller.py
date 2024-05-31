import flet as ft

from generalcontrols import InspectionTile
from views.inspection_view import InspectionPage

from daos.inspecao_dao import InspectionDAO


class MainPageController:
    def __init__(self, main_page):
        self.ui = main_page

    def new_inspection(self, event, tab_name):
        self.ui.page.data = tab_name
        self.ui.page.update()
        rota = InspectionPage(
            self.ui.page,
            self.ui.supabase,
            tab_name
        )
        self.ui.page.views.append(rota)
        self.ui.page.update()

    def show_drawer(self, event):
        self.ui.drawer.open = True
        self.ui.drawer.update()

    def populate_list_view(self):
        dao: InspectionDAO = InspectionDAO()
        insp_list_view = self.ui.body.content.controls[1].controls[0].tabs[0]
        list_of_inspections = dao.get_inspecoes()
        if list_of_inspections:
            for i in list_of_inspections:
                print(i)
        else:
            self.create_fake_list(insp_list_view)

    def create_fake_list(self, insp_list_view):
        for i in range(9):
            list_tile = self.create_list_tile(9 - i)
            insp_list_view.content.controls.append(list_tile)

    def create_list_tile(self, index):
        return InspectionTile(index, self.ui.body.item_clicked)

    def get_tab_name(self):
        tab_index = self._get_selected_tab_index()
        name = self.ui.body.content.controls[1].controls[0].tabs[tab_index].text
        return name

    def _get_selected_tab_index(self):
        return self.ui.body.content.controls[1].controls[0].selected_index