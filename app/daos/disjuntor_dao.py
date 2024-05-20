from data_base import DATABASE, connect


class DisjuntorDAO:
    def __init__(self, database=DATABASE):
        self.database = database

    def add_disjuntor(self, disjuntor):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO disjuntor (sename, name, press_num, pressao_nominal)
                VALUES (?, ?, ?, ?)
            ''',
                (disjuntor.sename, disjuntor.name, disjuntor.press_num,
                 disjuntor.pressao_nominal)
            )
            conn.commit()
            return cursor.lastrowid

    def get_disjuntores(self):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM disjuntor')
            return cursor.fetchall()

    def get_disjuntor_by_id(self, disjuntor_id):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM disjuntor WHERE id = ?', (disjuntor_id,)
            )
            return cursor.fetchone()

    def update_disjuntor(self, disjuntor):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE disjuntor
                SET name = ?, press_num = ?, pressao_nominal = ?
                WHERE id = ?
            ''', (disjuntor.name, disjuntor.press_num,
                  disjuntor.press_nominal, disjuntor.id))
            conn.commit()

    def delete_disjuntor(self, disjuntor_id):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'DELETE FROM disjuntor WHERE id = ?', (disjuntor_id,)
            )
            conn.commit()

    def add_complementacao(self, disjuntor_id, data_complementacao, tecnico, setor):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO complementacoes (disjuntor_id, data_complementacao, tecnico, setor)
                VALUES (?, ?, ?, ?)
            ''', (disjuntor_id, data_complementacao, tecnico, setor))
            conn.commit()

    def get_complementacoes(self, disjuntor_id):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT data_complementacao, tecnico, setor FROM complementacoes WHERE disjuntor_id = ?',
                (disjuntor_id,))
            return cursor.fetchall()