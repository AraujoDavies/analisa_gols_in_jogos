import json
import logging
from datetime import datetime
from time import sleep

from academia import AcademiaDasApostas
from database import Database
from gdrive import delete_values, update_values
from helpers import convert_data_in_datetime

logging.basicConfig(
    level=logging.WARNING,
    filename='analise_gols.log',
    encoding='utf-8',
    format='%(asctime)s - %(levelname)s: %(message)s',
)

with open(
    'codigo/campeonatos_nao_analisados.json', mode='r', encoding='utf-8'
) as campeonatos:
    ligas_nao_analisadas = json.load(campeonatos)

if __name__ == '__main__':
    logging.warning('Iniciando rotina...')
    # coletando informações no site da academia das apostas, jogos X dias
    academia = AcademiaDasApostas(remote=True)
    info_iniciais = []
    dias = 2 # analisa 2 dias apenas para a planilha não ficar mto pesada
    for dia in range(dias):
        academia.expand_all_matches()
        info_iniciais += academia.coletando_url_e_informacoes_iniciais()
        # se for o ultimo dia nao precisa clicar para a próx página
        if dia != dias - 1:
            academia.click_to_go_next_day_matches()
        logging.warning(f'Urls do dia {dia + 1}/{dias} coletadas')

    logging.warning('Inserindo urls coletadas no Database.')

    campeonatos_nao_analisados_exibidos_no_log = (
        []
    )   # variavel de controle. Vai exibir apenas uma vez no log o campeonato não desejado
    # salvando informações inicias no banco de dados
    for info_item in info_iniciais:
        data = convert_data_in_datetime(
            info_item['data'], info_item['horario_do_jogo']
        )
        campeonato = info_item['campeonato']
        # filtrando campeonatos que serão incluidos no banco de dados para análise
        if campeonato in ligas_nao_analisadas:
            if campeonato not in campeonatos_nao_analisados_exibidos_no_log:
                campeonatos_nao_analisados_exibidos_no_log.append(campeonato)
                logging.warning(
                    f'Campeonato: {campeonato} não será análisado!'
                )
            continue
        time_home = info_item['time_mandante']
        time_away = info_item['time_visitante']
        url = info_item['url']
        comando = f"SELECT url FROM academia_apostas.analise_gols WHERE url = '{url}';"
        url_check = Database().select(comando)
        if bool(url_check):   # se a url já existe no banco pule para o próximo
            logging.info(f'Url: {url} já está no Database')
            continue
        comando = f"""INSERT INTO `academia_apostas`.`analise_gols` (data, campeonato, time_home, time_away, url) 
VALUES ("{data}", "{campeonato}", "{time_home}", "{time_away}", "{url}");"""
        Database().manipulation(comando)

    logging.warning('Verificando jogos com datas antigas...')
    # remover eventos que ja iniciaram
    comando = 'SELECT data, url FROM academia_apostas.analise_gols;'
    datas_urls = Database().select(comando)
    data_atual = datetime.today()

    for dado in datas_urls:
        data = dado[0]
        url = dado[1]
        if data < data_atual and data.day != data_atual.day: # deletar jogos do dia anterior pra trás
            comando = f"DELETE FROM `academia_apostas`.`analise_gols` WHERE (`url` = '{url}');"
            Database().manipulation(comando)

    # pegar informações complementares (quantos gols/tempo)
    comando = 'SELECT url, HT FROM academia_apostas.analise_gols;'
    urls = Database().select(comando)

    logging.warning(
        f'Começando análise individuais de gols... ({len(urls)} jogos no DB).'
    )

    contador_de_jogos_analisados = 0
    contador_de_jogos_analisados_com_erro = 0
    for url in urls:
        # se info complementares(qt de gols) for NULL ai pode fazer a analise
        info_complementares_is_none = url[1] is None
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
                sleep(
                    10
                )   # acrescentar um jogo a cada X segundos pra não forçar o servidor
                contador_de_jogos_analisados += 1
            except:
                logging.error(f'Falha na análise individual da url: {url[0]}')
                contador_de_jogos_analisados_com_erro += 1
                continue

    logging.warning(
        f"""Análise individual de gols finalizada... ({contador_de_jogos_analisados} scrapy relizados.
        Erros = {contador_de_jogos_analisados_com_erro})."""
    )

    # acrescentar itens no google sheet
    # vericar token antes
    try:
        update_values([['test_before_insere']])
        logging.warning('Token está funcionando.')
    except:
        logging.error('Aguardando revalidação do Token do google')
        input('Aguardando revalidação do Token do google (qqr tecla to continue)')

    try:
        comando = 'SELECT * FROM academia_apostas.analise_gols;'
        dados = Database().select(comando)

        planilha = []
        for dado in dados:
            data = dado[1]
            campeonato = dado[2]
            mandante = dado[3]
            visitante = dado[4]
            url = dado[5]
            ht = dado[6]
            ft = dado[7]
            zero15 = dado[8]
            quinze30 = dado[9]
            trinta45 = dado[10]
            quarentacinco60 = dado[11]
            sessenta75 = dado[12]
            setentacinco90 = dado[13]

            row = [
                str(data),
                campeonato,
                mandante,
                visitante,
                ht,
                ft,
                zero15,
                quinze30,
                trinta45,
                quarentacinco60,
                sessenta75,
                setentacinco90,
            ]
            planilha.append(row)

        delete_values()   # primeiro limpa a planilha
        update_values(planilha)   # depois insere
        logging.warning('Valores do banco de dados inseridos no gsheet')
    except:
        logging.error('Falha ao inserir dados do DB no Gsheet')

    logging.warning('Finalizando rotina. até amanhã <3')
