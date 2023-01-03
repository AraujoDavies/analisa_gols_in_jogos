from datetime import datetime


def convert_data_in_datetime(data: str, horario_do_jogo: str):
    """
    Convert params data and hour in datetime.

    input: '10/01/2023' and '12:30' | output datetime(2023, 01, 10, 12, 30).
    """
    dia, mes, ano = data.split('/')
    hora, minuto = horario_do_jogo.split(':')
    data_convert = datetime(
        int(ano), int(mes), int(dia), int(hora), int(minuto)
    )
    return data_convert
