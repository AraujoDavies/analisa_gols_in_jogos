import logging
from os import getenv

import mysql.connector  # pip install mysql-connector-python
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.conexao = mysql.connector.connect(
            host=getenv('HOST_DATABASE'),
            user=getenv('USER_DATABASE'),
            password=getenv('PASSWORD_DATABASE'),
            database=getenv('TABLE_DATABASE'),
        )
        self.cursor = self.conexao.cursor()
        logging.info('DATABASE: Conexão aberta')

    def select(self, comando):
        """Data consult."""
        select = []
        try:
            self.cursor.execute(comando)
            select = self.cursor.fetchall()   # ex de resultado: [(1.29, 30)]
        except:
            logging.error('DATABASE: Select Fail')
        finally:
            self.cursor.close()
            self.conexao.close
            logging.info('DATABASE: Conexão fechada')
        return select

    def manipulation(self, comando):
        """Param "comando" can be Insert, update and delete."""
        try:
            self.cursor.execute(comando)
            self.conexao.commit()
        except:
            logging.error(f'DATABASE: DML Fail {comando}')
        finally:
            self.cursor.close()
            self.conexao.close
            logging.info('DATABASE: Conexão fechada')
