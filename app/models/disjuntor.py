from datetime import datetime

from daos.disjuntor_dao import DisjuntorDAO


class Disjuntor:
    dao = DisjuntorDAO()

    def __init__(self, sename, name, press_num, press_nominal, press_oil,
                 horimeter, id=None):
        self.id = id
        self.sename =sename
        self.name = name
        self.press_num = press_num
        self.press_nominal = press_nominal
        self.press_oil = press_oil
        self.horimeter = horimeter
        self.last_comp = None

    def save(self):
        if self.id is None:
            self.id = self.dao.add_disjuntor(self)
        else:
            self.dao.update_disjuntor(self)

    def delete(self):
        self.dao.delete_disjuntor(self.id)

    @classmethod
    def load(cls, disjuntor_id):
        data = cls.dao.get_disjuntor_by_id(disjuntor_id)
        if data:
            return cls(
                sename=data[1],
                name=data[2],
                press_num=data[3],
                press_nominal=data[4],
                press_oil=data[5],
                horimeter=data[6],
                id=data[0]
            )

    def get_complementaçoes(self):
        return self.dao.get_complementacoes(self.id)

    def add_complememtacao(self, data_complementacao, tecnico, setor):
        self.dao.add_complementacao(
            self.id, data_complementacao, tecnico, setor
        )
