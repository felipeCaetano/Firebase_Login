import flet as ft
from app.controllers.disjuntor_controller import DisjuntorController
from app.generalcontrols import Button, NavigationDrawer


class DisjuntorPage(ft.View):
    def __init__(self, page: ft.Page, supabase, sename="JRM"):
        super().__init__(
            route="/cadastrar-disj",
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        self.sename = sename
        self.page = page
        self.supabase = supabase
        self.controller = DisjuntorController()
        self.appbar = self.create_appbar()
        self.page.appbar = self.appbar
        self.page.update()
        self.drawer = NavigationDrawer(on_change=None)
        self.body = ft.Column()
        self.controls = [
            self.page.appbar,
            self.body,
            ft.Row(
                controls=[
                    Button("Adicionar Disjuntor", self.add_disjuntor_form)
                ]
            )
        ]
        self.load_disjuntores()

    def create_appbar(self):
        return ft.AppBar(
            leading=ft.IconButton(ft.icons.ARROW_BACK, on_click=self.go_back),
            title=ft.Text("Cadastrar Disjuntores"),
            bgcolor=ft.colors.GREEN_ACCENT_100
        )

    def go_back(self, event):
        self.page.route = "/view-reg"
        self.page.go(self.page.route)

    def load_disjuntores(self):
        self.body.controls.clear()
        disjuntores = self.controller.get_disjuntores()
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Subestação")),
                ft.DataColumn(ft.Text("Disjuntor")),
                ft.DataColumn(ft.Text("Pressostatos"), numeric=True),
                ft.DataColumn(ft.Text("Press. Nominal"), numeric=True),
                ft.DataColumn(ft.Text("Press. Óleo"), numeric=True),
                ft.DataColumn(ft.Text("Horimetro"), numeric=True),
                ft.DataColumn(ft.Text("")),
                ft.DataColumn(ft.Text(""))
            ]
        )
        if disjuntores:
            for disjuntor in disjuntores:
                table.rows.append(
                    ft.DataRow([
                        ft.DataCell(ft.Text(f"{disjuntor[1]}")),
                        ft.DataCell(ft.Text(f"{disjuntor[2]}")),
                        ft.DataCell(ft.Text(f"{disjuntor[3]}")),
                        ft.DataCell(ft.Text(f"{disjuntor[4]}")),
                        ft.DataCell(ft.Text(f"{disjuntor[5]}")),
                        ft.DataCell(ft.Text(f"{disjuntor[6]}")),
                        ft.DataCell(ft.IconButton(
                            ft.icons.DELETE,
                            on_click=lambda e, d=disjuntor:
                            self.delete_disjuntor(e, d)
                        )),
                        ft.DataCell(ft.IconButton(
                            ft.icons.EDIT,
                            on_click=lambda e, d=disjuntor:
                            self.edit_disjuntor_form(e, d)
                        )),
                    ])
                )
            self.body.controls.append(table)
        else:
            self.body.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Não há disjuntores cadastrados")
                        ]
                    )
                )
            )
        self.page.update()

    def add_disjuntor_form(self, event):
        dialog = ft.AlertDialog(
            title=ft.Text("Adicionar Disjuntor"),
            content=ft.Column(controls=[
                ft.TextField(label="Subestação"),
                ft.TextField(label="Nome"),
                ft.TextField(label="Número de Pressostatos"),
                ft.TextField(label="Pressão Nominal"),
                ft.TextField(label="Pressão Óleo"),
                ft.TextField(label="Horas Trabalhadas"),
            ]),
            actions=[
                Button("Cancelar",
                       lambda e: self.page.dialog.on_dismiss),
                Button("Salvar", self.save_disjuntor),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def save_disjuntor(self, event):
        sename = self.page.dialog.content.controls[0].value
        nome = self.page.dialog.content.controls[1].value
        press_num = int(self.page.dialog.content.controls[2].value)
        pressao_nominal = float(
            self.page.dialog.content.controls[3].value.replace(',', '.')
        )
        press_oil = self.page.dialog.content.controls[4].value
        horimeter = self.page.dialog.content.controls[5].value
        self.controller.add_disjuntor(
            sename, nome, press_num, pressao_nominal, press_oil, horimeter
        )
        self.page.dialog.open = False
        self.load_disjuntores()

    def edit_disjuntor_form(self, event, disjuntor):
        dialog = ft.AlertDialog(
            title=ft.Text("Editar Disjuntor"),
            content=ft.Column(controls=[
                ft.TextField(label="Nome", value=disjuntor[2]),
                ft.TextField(
                    label="Número de Pressostatos",
                    value=str(disjuntor[3])
                ),
                ft.TextField(
                    label="Pressão Nominal",
                    value=str(disjuntor[4])),
                ft.TextField(
                    label="Pressão Óleo",
                    value=str(disjuntor[5])),
                ft.TextField(
                    label="Horas Trabalhadas",
                    value=str(disjuntor[6])),
            ]),
            actions=[
                Button("Cancelar",
                       lambda e: self.page.dialog.on_dismiss),
                Button("Salvar",
                       lambda e, d=disjuntor: self.update_disjuntor(e, d)),
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def update_disjuntor(self, event, disjuntor):
        nome = self.page.dialog.content.controls[0].value
        press_num = int(self.page.dialog.content.controls[1].value)
        press_nom = float(self.page.dialog.content.controls[2].value)
        press_oil = self.page.dialog.content.controls[3].value
        horimeter = self.page.dialog.content.controls[4].value
        self.controller.update_disjuntor(
            disjuntor[0], nome, press_num, press_nom, press_oil, horimeter)
        self.page.dialog.open = False
        self.load_disjuntores()

    def delete_disjuntor(self, event, disjuntor):
        self.controller.delete_disjuntor(disjuntor[0])
        self.load_disjuntores()

    def view_complementacoes(self, event, disjuntor):
        complementacoes = self.controller.get_complementacoes(disjuntor[0])
        dialog_content = ft.Column()
        for comp in complementacoes:
            dialog_content.controls.append(ft.Text(
                f"Data: {comp[0]}, Técnico: {comp[1]}, Setor: {comp[2]}"))

        dialog = ft.AlertDialog(
            title=ft.Text(f"Complementações de {disjuntor.name}"),
            content=dialog_content,
            actions=[
                Button("Fechar",
                       lambda e: self.page.dialog.on_dismiss),
                Button("Adicionar Complementação",
                       lambda e, d=disjuntor: self.add_complement_form(e, d)
                       ),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def add_complement_form(self, event, disjuntor):
        dialog = ft.AlertDialog(
            title=ft.Text("Adicionar Complementação"),
            content=ft.Column(controls=[
                ft.TextField(label="Data (YYYY-MM-DD)"),
                ft.TextField(label="Técnico"),
                ft.TextField(label="Setor"),
            ]),
            actions=[
                ft.Button(
                    "Cancelar",
                    on_click=lambda e: self.page.dialog.on_dismiss
                ),
                ft.Button(
                    "Salvar",
                    on_click=lambda e, d=disjuntor: self.save_complement(e, d)
                ),
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def save_complement(self, event, disjuntor):
        data_complementacao = self.page.dialog.content.controls[0].value
        tecnico = self.page.dialog.content.controls[1].value
        setor = self.page.dialog.content.controls[2].value
        self.controller.add_complementacao(disjuntor[0], data_complementacao,
                                           tecnico, setor)
        self.page.dialog.dismiss()
        self.view_complementacoes(event, disjuntor)
