import sqlite3
from datetime import datetime

DATABASE = 'leitura_disjuntores.db'


def connect():
    return sqlite3.connect(DATABASE)


def create_table():
    with connect() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS disjuntor (
                id INTEGER PRIMARY KEY,
                sename TEXT NOT NULL,
                name TEXT NOT NULL,
                press_num INTEGER NOT NULL,
                pressao_nominal REAL,
                press_oil REAL,
                horimeter REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complementacoes (
                id INTEGER PRIMARY KEY,
                disjuntor_id INTEGER,
                data_complementacao TEXT,
                tecnico TEXT,
                setor TEXT,
                FOREIGN KEY(disjuntor_id) REFERENCES disjuntor(id)
            )
        ''')
        conn.commit()


create_table()
