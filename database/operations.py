from typing import Tuple, List

from .connection import UseDatabase


def select(db_config: dict, sql: str) -> Tuple[Tuple, List[str]]:
    """
    Выполняет запрос (SELECT) к БД с указанным конфигом и запросом.
    Args:
        db_config: dict - Конфиг для подключения к БД.
        sql: str - SQL-запрос.
    Return:
        Кортеж с результатом запроса и описанеим колонок запроса.
    """
    result = tuple()
    schema = []
    with UseDatabase(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]
        result = cursor.fetchall()
    return result, schema

def select_dict(db_config: dict, sql: str) -> List:
    result = []
    with UseDatabase(db_config) as cursor:

        if cursor is None:
            raise ValueError('Курсор не создан')

        cursor.execute(sql)
        schema = [column[0] for column in cursor.description]

        for row in cursor.fetchall():
            result.append(dict(zip(schema, row)))

    return result

def call_proc(db_config: dict, proc_name: str, *args):
    with UseDatabase(db_config) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        param_list = []

        for arg in args:
            print('arg=', arg)
            param_list.append(int(arg))

        print('param_list=', param_list)
        result = cursor.callproc(proc_name, param_list)
    return result

def insert(db_config:dict, _sql: str):
    with UseDatabase(db_config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not found')
        result = cursor.execute(_sql)
    return result

def update(db_config:dict, _sql:str):
    with UseDatabase(db_config) as cursor:
        if cursor is None:
            raise ValueError('Update cursor not found')
        result = cursor.execute(_sql)
    return result

#добавить проверку, существует ли отчет в обработчике (select count(*) ...) если 0 то..