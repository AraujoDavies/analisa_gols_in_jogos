from academia import AcademiaDasApostas
from database import Database
from helpers import convert_data_in_datetime
from time import sleep
import logging

logging.basicConfig(level=logging.WARNING, filename="codigo.log", encoding='utf-8', format="%(asctime)s - %(levelname)s: %(message)s")

if __name__ == '__main__':
    logging.warning('Iniciando rotina...')
    # coletando informações no site da academia das apostas, jogos X dias (3 por default)
    academia = AcademiaDasApostas()
    info_iniciais = []
    dias = 5
    for dia in range(dias):
        academia.expand_all_matches()
        info_iniciais += academia.coletando_url_e_informacoes_iniciais()
        # se for o ultimo dia nao precisa clicar para a próx página
        if dia != dias -1: 
            academia.click_to_go_next_day_matches()
        logging.warning(f'Urls do dia {dia + 1/dias} coletadas')

    logging.warning('Inserindo urls coletadas no Database.')
    # salvando informações inicias no banco de dados
    for info_item in info_iniciais:
        data = convert_data_in_datetime(info_item['data'], info_item['horario_do_jogo'])
        campeonato = info_item['campeonato']
        time_home = info_item['time_mandante']
        time_away = info_item['time_visitante']
        url = info_item['url']
        comando = f"SELECT url FROM academia_apostas.analise_gols WHERE url = '{url}';"
        url_check = Database().select(comando)
        if bool(url_check): # se a url já existe no banco pule para o próximo
            logging.info(f'Url: {url} já está no Database')
            continue
        comando = f"INSERT INTO `academia_apostas`.`analise_gols` (data, campeonato, time_home, time_away, url) VALUES ('{data}', '{campeonato}', '{time_home}', '{time_away}', '{url}');"
        Database().manipulation(comando)

    logging.warning('Começando análise individuais de gols...')
    # pegar informações complementares (quantos gols/tempo)
    comando = f"SELECT url, HT FROM academia_apostas.analise_gols;"
    urls = Database().select(comando)
    for url in urls:
        # se info complementares(qt de gols) for NULL ai pode fazer a analise
        info_complementares_is_none = url[1] == None
        if info_complementares_is_none:
            try:
                dados_dos_gols = academia.coletar_info_de_gols(url[0])
                comando = f"""
UPDATE `academia_apostas`.`analise_gols` SET `HT` = '{dados_dos_gols['ht']}', `FT` = '{dados_dos_gols['ft']}', 
`0 - 15` = '{dados_dos_gols['zero15']}', `15 - 30` = '{dados_dos_gols['quinze30']}',
`30 - 45` = '{dados_dos_gols['trinta45']}', `45 - 60` = '{dados_dos_gols['quarentacinco60']}', 
`60 - 75` = '{dados_dos_gols['sessenta75']}', `75 - 90` = '{dados_dos_gols['setentacinco90']}',
`FM 0 - 15` = '{dados_dos_gols['feitos_mandante_0_15']}', `FM 15 - 30` = '{dados_dos_gols['feitos_mandante_15_30']}',
`FM 30 - 45` = '{dados_dos_gols['feitos_mandante_30_45']}', `FM 45 - 60` = '{dados_dos_gols['feitos_mandante_45_60']}', 
`FM 60 - 75` = '{dados_dos_gols['feitos_mandante_60_75']}', `FM 75 - 90` = '{dados_dos_gols['feitos_mandante_75_90']}',
`SM 0 - 15` = '{dados_dos_gols['sofridos_mandante_0_15']}', `SM 15 - 30` = '{dados_dos_gols['sofridos_mandante_15_30']}', 
`SM 30 - 45` = '{dados_dos_gols['sofridos_mandante_30_45']}', `SM 45 - 60` = '{dados_dos_gols['sofridos_mandante_45_60']}', 
`SM 60 - 75` = '{dados_dos_gols['sofridos_mandante_60_75']}', `SM 75 - 90` = '{dados_dos_gols['sofridos_mandante_75_90']}', 
`FV 0 - 15` = '{dados_dos_gols['feitos_visitante_0_15']}', `FV 15 - 30` = '{dados_dos_gols['feitos_visitante_15_30']}',
`FV 30 - 45` = '{dados_dos_gols['feitos_visitante_30_45']}', `FV 45 - 60` = '{dados_dos_gols['feitos_visitante_45_60']}',
`FV 60 - 75` = '{dados_dos_gols['feitos_visitante_60_75']}', `FV 75 - 90` = '{dados_dos_gols['feitos_visitante_75_90']}',
`SV 0 - 15` = '{dados_dos_gols['sofridos_visitante_0_15']}', `SV 15 - 30` = '{dados_dos_gols['sofridos_visitante_15_30']}', 
`SV 30 - 45` = '{dados_dos_gols['sofridos_visitante_30_45']}', `SV 45 - 60` = '{dados_dos_gols['sofridos_visitante_45_60']}',
`SV 60 - 75` = '{dados_dos_gols['sofridos_visitante_60_75']}', `SV 75 - 90` = '{dados_dos_gols['sofridos_visitante_75_90']}'
WHERE (`url` = '{url[0]}');"""

                Database().manipulation(comando)
                sleep(20) # acrescentar um jogo a cada 20 segundo pra não forçar o servidor
            except:
                logging.error(f'Falha na análise individual da url: {url[0]}')
                continue
    logging.warning('Finalizando rotina. até amanhã <3')