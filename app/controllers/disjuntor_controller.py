from app.models.disjuntor import Disjuntor


class DisjuntorController:
    def __init__(self):
        pass

    def get_disjuntores(self):
        return Disjuntor.dao.get_disjuntores()

    def add_disjuntor(self, sename, name, press_num, pressao_nominal,
                      press_oil, horimeter):
        disjuntor = Disjuntor(
            sename=sename,
            name=name,
            press_num=press_num,
            press_nominal=pressao_nominal,
            press_oil=press_oil,
            horimeter=horimeter
        )
        disjuntor.save()

    def update_disjuntor(self, disjuntor_id, name, press_num,
                         pressao_nominal, press_oil, horimeter):
        disjuntor = Disjuntor.load(disjuntor_id)
        disjuntor.name = name
        disjuntor.press_num = press_num
        disjuntor.pressao_nominal = pressao_nominal
        disjuntor.press_oil = press_oil
        disjuntor.horimeter = horimeter
        disjuntor.save()

    def delete_disjuntor(self, disjuntor_id):
        disjuntor = Disjuntor.load(disjuntor_id)
        disjuntor.delete()

    def get_complementacoes(self, disjuntor_id):
        disjuntor = Disjuntor.load(disjuntor_id)
        return disjuntor.get_complementacoes()

    def add_complementacao(self, disjuntor_id, data_complementacao, tecnico,
                           setor):
        disjuntor = Disjuntor.load(disjuntor_id)
        disjuntor.add_complementacao(data_complementacao, tecnico, setor)
