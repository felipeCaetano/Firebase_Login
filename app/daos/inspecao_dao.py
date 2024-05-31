from data_base import DATABASE, connect


class InspectionDAO:
    def __init__(self, db_name=DATABASE):
        self.db_name = db_name
        # self._create_inspections_table()

    def _create_inspections_table(self):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS inspecoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sename TEXT,
                    data TEXT,
                    hora TEXT,
                    temp TEXT,
                    press TEXT
                )
            ''')
            conn.commit()

    def add_inspection(self, sename, data, hora, temp, press):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO inspecoes (sename, data, hora, temp, press)
                VALUES (?, ?, ?, ?, ?)
            ''', (sename,
                  data,
                  hora,
                  temp,
                  " ".join([str(disjuntor.get_press()) for disjuntor in press])
                  ))
            conn.commit()

    def get_inspecoes(self):
        with connect() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM inspecoes')
            return cursor.fetchall()
