import flet as ft

from generalcontrols import InspectionTile
from views.inspection_view import InspectionPage

from daos.inspecao_dao import InspectionDAO


class MainPageController:

    def __init__(self, main_page):
        self.ui = main_page
        self.insp_list_views = {
            "JRM": self.ui.body.content.controls[1].controls[0].tabs[1],
            "BGI": self.ui.body.content.controls[1].controls[0].tabs[0]
        }

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
        list_of_inspections = dao.get_inspecoes()
        if list_of_inspections:
            for insp in list_of_inspections:
                print(insp)
                list_tile = self.create_list_tile(insp)
                insp_list_view = self.insp_list_views.get(insp[1])
                insp_list_view.content.controls.append(list_tile)
    #     else:
    #         self.create_fake_list()
    #
    # def create_fake_list(self, ):
    #     for i in range(9):
    #         list_tile = self.create_list_tile(9 - i)
    #         insp_list_view.content.controls.append(list_tile)

    def create_list_tile(self, index):
        return InspectionTile(index, self.ui.body.item_clicked)

    def get_tab_name(self):
        tab_index = self._get_selected_tab_index()
        name = self.ui.body.content.controls[1].controls[0].tabs[tab_index].text
        return name

    def _get_selected_tab_index(self):
        return self.ui.body.content.controls[1].controls[0].selected_index