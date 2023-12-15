import sqlite3
from types import TracebackType
import typing
from contextlib import contextmanager


class Connection(typing.ContextManager):
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        return self

    def __exit__(self, exc_type: typing.Optional[typing.Type[BaseException]], exc_val: typing.Optional[BaseException], exc_tb: typing.Optional[TracebackType]):
        self.connection.commit()
        self.connection.close()

    def execute(self, query: str, params: tuple):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor


@contextmanager
def open_connection(db_path) -> 'Connection':
    with Connection(db_path) as connection:
        yield connection


def initialize_database(db_path):
    with open_connection(db_path) as connection:
        connection.execute(
            'CREATE TABLE IF NOT EXISTS working_log ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'employee_id INTEGER,'
            'time INTEGER,'
            'date DATE'
            ')', ())
        connection.execute(
            'CREATE TABLE IF NOT EXISTS employee_rates ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'employee_id INTEGER,'
            'hour_rate INTEGER'
            ')', ())
        connection.execute(
            'INSERT INTO employee_rates (employee_id, hour_rate) VALUES (?, ?)',
            (1, 10)
        )


class WorkingHourManager:
    DB_PATH = 'db.sqlite3'

    @staticmethod
    def log(employee_id, time, date) -> None:
        with open_connection(WorkingHourManager.DB_PATH) as connection:
            connection.execute(
                'INSERT INTO working_log (employee_id, time, date) VALUES (?, ?, ?)',
                (employee_id, time, date)
            )

    @staticmethod
    def total(employee_id, date_from, date_to):
        with open_connection(WorkingHourManager.DB_PATH) as connection:
            result = connection.execute(
                'SELECT SUM(time) FROM working_log WHERE employee_id = ? AND date >= ? AND date <= ?',
                (employee_id, date_from, date_to,)
            ).fetchone()
            return result[0] if result[0] else 0

    @staticmethod
    def salary(employee_id, date_from, date_to):
        with open_connection(WorkingHourManager.DB_PATH) as connection:
            response = connection.execute(
                'SELECT hour_rate FROM employee_rates WHERE employee_id = ?',
                (employee_id,)
            ).fetchone()
            
            hour_rate = response[0] if response else 0

            if not hour_rate:
                return 'Hour rate for employee not specified'

            total_time = WorkingHourManager.total(employee_id, date_from, date_to)

            return total_time * hour_rate
