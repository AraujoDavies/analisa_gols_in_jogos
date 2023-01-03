from datetime import datetime

from codigo.database import Database
from codigo.gdrive import delete_values, update_values
from codigo.helpers import convert_data_in_datetime


def test_conversao_data_para_datetime():
    assert convert_data_in_datetime('16/05/1998', '14:00') == datetime(
        1998, 5, 16, 14, 0
    )


def test_database_insert_select_update_and_delete():
    Database().manipulation(
        "INSERT INTO `entradas`.`testes` (`nome`) VALUES ('TEST_NAME_VALIDATION');"
    )
    select = Database().select('select * from entradas.testes;')
    assert select[-1][1] == 'TEST_NAME_VALIDATION'   # insert and select ok.
    Database().manipulation(
        "UPDATE `entradas`.`testes` SET `nome` = 'NEW_TEST_NAME' WHERE (`nome` = 'TEST_NAME_VALIDATION');"
    )
    select = Database().select('select * from entradas.testes;')
    assert select[-1][1] == 'NEW_TEST_NAME'   # update and select ok.
    Database().manipulation(
        "DELETE FROM `entradas`.`testes` WHERE (`nome` = 'NEW_TEST_NAME');"
    )
    select = Database().select('select * from entradas.testes;')
    assert select[-1][1] != 'NEW_TEST_NAME'   # delete and select ok.


def test_de_update_do_gdrive():
    values = [['10-11-13', 'Brasil'], ['10-11-14', 'Argentina']]
    return_values = update_values(values)
    assert (
        return_values['spreadsheetId']
        == '1ene0rIqqgP5wDQJrLII2M5bhqfH21lHK7zyx0yJt7vc'
    )


def test_de_delete_do_gdrive():
    return_values = delete_values()
    assert (
        return_values['spreadsheetId']
        == '1ene0rIqqgP5wDQJrLII2M5bhqfH21lHK7zyx0yJt7vc'
    )
