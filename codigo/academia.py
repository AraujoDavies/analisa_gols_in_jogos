import logging
from datetime import datetime
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class AcademiaDasApostas:
    def __init__(self, driver=False, remote=False):
        """
        Atenção aos parâmetros que definem como o browser será instanciado.

        driver = False: mean class create a webdriver local session
        driver = webdriver: mean receives a webdriver session

        remote = True: mean chrome in container.
        """
        if remote is True:   # selenium grid
            self.driver = webdriver.Remote(
                command_executor='http://localhost:4444',
                options=webdriver.ChromeOptions(),
            )
        elif driver is False:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service)
        elif bool(driver):
            self.driver = driver
        self.driver.get('https://www.academiadasapostasbrasil.com/')
        self.driver.maximize_window()

    def expand_all_matches(self):
        """Click 2x partidas escondidas."""
        partidas_escondidas = self.driver.find_elements(
            'xpath', '//td[contains(@class, "footer")]'
        )
        tentativas = 0
        while bool(partidas_escondidas):
            tentativas += 1
            if tentativas > 10:
                break
            try:
                partidas_escondidas[0].click()
            except:
                logging.warning(
                    'expand_all_matches: except não conseguiu expandir.'
                )
            partidas_escondidas = self.driver.find_elements(
                'xpath', '//td[contains(@class, "footer")]'
            )
        if bool(partidas_escondidas) is False:
            logging.warning('expand_all_matches: Expansão finalizada com sucesso!')

    def coletando_url_e_informacoes_iniciais(self):
        """Coleta e retorna os dados iniciais dos confrontos."""
        informacoes_iniciais = []
        html = self.driver.find_element(
            'xpath', '//div[@id="fh_main_tab"]//tbody'
        ).get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        jogos_tr = soup.findAll('tr')
        dia = self.driver.find_element(
            'xpath', '//div[@class="date-filter"]//label'
        )
        dia = dia.get_attribute('data-displaydate')

        if dia == 'Hoje' or type(dia) is None:
            dia = f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}'
        else:
            dia = dia.split()[1]

        for jogo in jogos_tr:
            dict = {}
            dict['data'] = dia
            data_inicio = jogo.find('td', class_='hour').text
            hora, minuto = data_inicio.split()[1].split(':')
            dict['horario_do_jogo'] = f'{hora}:{minuto}'

            for td in jogo.findAll('td'):
                if 'original-title' in td.attrs:
                    dict['campeonato'] = td.attrs['original-title']
                if 'team-a' in td.attrs['class']:
                    dict['time_mandante'] = td.text.replace('\n', '')
                if 'team-b' in td.attrs['class']:
                    dict['time_visitante'] = td.text.replace('\n', '')

            dict['url'] = jogo.find('td', class_='score').find('a')['href']
            informacoes_iniciais.append(dict)
            # break # hack
        logging.warning(
            f'coletando_url_e_informacoes_iniciais: {dia}, quantidade de itens: {len(informacoes_iniciais)}'
        )
        return informacoes_iniciais

    def click_to_go_next_day_matches(self):
        """Click to load list games next day."""
        try:
            url_primeiro_jogo = self.driver.find_element(
                'xpath', '//td[@class = "score "]//a'
            )
            url_old = url_primeiro_jogo.get_attribute('href')
            url_new = url_primeiro_jogo.get_attribute('href')

            while url_new == url_old:
                btn_next_list = self.driver.find_elements(
                    'xpath', '//span[@class="aa-icon-next date-increment"]'
                )
                btn_next_list[0].click()
                sleep(3)
                url_new = self.driver.find_element(
                    'xpath', '//td[@class = "score "]//a'
                ).get_attribute('href')
                if url_new != url_old:
                    logging.warning(
                        'click_to_go_next_day_matches: clicou com sucesso.'
                    )
                    return True
        except:
            logging.error('click_to_go_next_day_matches: clique FALHOU!')
            return False

    def coletar_info_de_gols(self, url):
        """
        Coletar gols feitos e sofridos nos últimos 10 jogos do mandante jogando em casa e do visitante jogando fora.
        Além das deviidas somas por tempo de jogo, HT e FT.

        retorna uma lista com a quantidade de gols incluindo somatória do HT e do FT.
        """

        self.driver.get(url)
        dados_dos_gols = {}

        # aguarda carregamento do elemento
        click_last_ten_matches = self.driver.find_elements(
            'xpath',
            '//li[@data-id = "last_10g"][@market="teams_goals"][contains(@class, "current")]',
        )
        count_element_not_found = 0
        while bool(click_last_ten_matches) is False:
            click = self.driver.find_element(
                'xpath', '//li[@data-id = "last_10g"][@market="teams_goals"]'
            )
            click.click()
            # print(f'coletar_info_de_gols: {count_element_not_found} segundos para clique funcionar')
            count_element_not_found += 1
            if count_element_not_found > 15:
                raise TimeoutError(
                    'Não clicou para exibir valores dos últimos 10 jogos'
                )
            click_last_ten_matches = self.driver.find_elements(
                'xpath',
                '//li[@data-id = "last_10g"][@market="teams_goals"][contains(@class, "current")]',
            )
            sleep(1)

        # analisa os dados com ajuda do SOUP
        html = self.driver.find_element(
            'xpath', '//div[@id="main-container"]'
        ).get_attribute('outerHTML')
        html = ' '.join(html.split()).replace('> <', '><')
        soup = BeautifulSoup(html, 'html.parser')
        gols_marcados = soup.find_all(
            'td', string='G.Marc'
        )   # todos os "gols marcados
        gols_sofridos = soup.find_all(
            'td', string='G.Sofr'
        )   # todos os "gols Sofridos"

        dados_dos_gols['feitos_mandante_0_15'] = int(
            0
            if gols_marcados[0].findNext('td').string == ''
            else gols_marcados[0].findNext('td').string
        )
        dados_dos_gols['feitos_mandante_15_30'] = int(
            0
            if gols_marcados[1].findNext('td').string == ''
            else gols_marcados[1].findNext('td').string
        )
        dados_dos_gols['feitos_mandante_30_45'] = int(
            0
            if gols_marcados[2].findNext('td').string == ''
            else gols_marcados[2].findNext('td').string
        )
        dados_dos_gols['feitos_mandante_45_60'] = int(
            0
            if gols_marcados[3].findNext('td').string == ''
            else gols_marcados[3].findNext('td').string
        )
        dados_dos_gols['feitos_mandante_60_75'] = int(
            0
            if gols_marcados[4].findNext('td').string == ''
            else gols_marcados[4].findNext('td').string
        )
        dados_dos_gols['feitos_mandante_75_90'] = int(
            0
            if gols_marcados[5].findNext('td').string == ''
            else gols_marcados[5].findNext('td').string
        )

        dados_dos_gols['feitos_visitante_0_15'] = int(
            0
            if gols_marcados[6].findNext('td').string == ''
            else gols_marcados[6].findNext('td').string
        )
        dados_dos_gols['feitos_visitante_15_30'] = int(
            0
            if gols_marcados[7].findNext('td').string == ''
            else gols_marcados[7].findNext('td').string
        )
        dados_dos_gols['feitos_visitante_30_45'] = int(
            0
            if gols_marcados[8].findNext('td').string == ''
            else gols_marcados[8].findNext('td').string
        )
        dados_dos_gols['feitos_visitante_45_60'] = int(
            0
            if gols_marcados[9].findNext('td').string == ''
            else gols_marcados[9].findNext('td').string
        )
        dados_dos_gols['feitos_visitante_60_75'] = int(
            0
            if gols_marcados[10].findNext('td').string == ''
            else gols_marcados[10].findNext('td').string
        )
        dados_dos_gols['feitos_visitante_75_90'] = int(
            0
            if gols_marcados[11].findNext('td').string == ''
            else gols_marcados[11].findNext('td').string
        )

        dados_dos_gols['sofridos_mandante_0_15'] = int(
            0
            if gols_sofridos[0].findNext('td').string == ''
            else gols_sofridos[0].findNext('td').string
        )
        dados_dos_gols['sofridos_mandante_15_30'] = int(
            0
            if gols_sofridos[1].findNext('td').string == ''
            else gols_sofridos[1].findNext('td').string
        )
        dados_dos_gols['sofridos_mandante_30_45'] = int(
            0
            if gols_sofridos[2].findNext('td').string == ''
            else gols_sofridos[2].findNext('td').string
        )
        dados_dos_gols['sofridos_mandante_45_60'] = int(
            0
            if gols_sofridos[3].findNext('td').string == ''
            else gols_sofridos[3].findNext('td').string
        )
        dados_dos_gols['sofridos_mandante_60_75'] = int(
            0
            if gols_sofridos[4].findNext('td').string == ''
            else gols_sofridos[4].findNext('td').string
        )
        dados_dos_gols['sofridos_mandante_75_90'] = int(
            0
            if gols_sofridos[5].findNext('td').string == ''
            else gols_sofridos[5].findNext('td').string
        )

        dados_dos_gols['sofridos_visitante_0_15'] = int(
            0
            if gols_sofridos[6].findNext('td').string == ''
            else gols_sofridos[6].findNext('td').string
        )
        dados_dos_gols['sofridos_visitante_15_30'] = int(
            0
            if gols_sofridos[7].findNext('td').string == ''
            else gols_sofridos[7].findNext('td').string
        )
        dados_dos_gols['sofridos_visitante_30_45'] = int(
            0
            if gols_sofridos[8].findNext('td').string == ''
            else gols_sofridos[8].findNext('td').string
        )
        dados_dos_gols['sofridos_visitante_45_60'] = int(
            0
            if gols_sofridos[9].findNext('td').string == ''
            else gols_sofridos[9].findNext('td').string
        )
        dados_dos_gols['sofridos_visitante_60_75'] = int(
            0
            if gols_sofridos[10].findNext('td').string == ''
            else gols_sofridos[10].findNext('td').string
        )
        dados_dos_gols['sofridos_visitante_75_90'] = int(
            0
            if gols_sofridos[11].findNext('td').string == ''
            else gols_sofridos[11].findNext('td').string
        )

        # gols_feitos_sofridos = [feitos_mandante_0_15, feitos_mandante_15_30, feitos_mandante_30_45, feitos_mandante_45_60,
        # feitos_mandante_60_75, feitos_mandante_75_90, feitos_visitante_0_15, feitos_visitante_15_30, feitos_visitante_30_45,
        # feitos_visitante_45_60, feitos_visitante_60_75, feitos_visitante_75_90, sofridos_mandante_0_15, sofridos_mandante_15_30,
        # sofridos_mandante_30_45, sofridos_mandante_45_60, sofridos_mandante_60_75, sofridos_mandante_75_90, sofridos_visitante_0_15,
        # sofridos_visitante_15_30, sofridos_visitante_30_45, sofridos_visitante_45_60, sofridos_visitante_60_75, sofridos_visitante_75_90]

        dados_dos_gols['zero15'] = (
            dados_dos_gols['feitos_mandante_0_15']
            + dados_dos_gols['feitos_visitante_0_15']
            + dados_dos_gols['sofridos_mandante_0_15']
            + dados_dos_gols['sofridos_visitante_0_15']
        )
        dados_dos_gols['quinze30'] = (
            dados_dos_gols['feitos_mandante_15_30']
            + dados_dos_gols['feitos_visitante_15_30']
            + dados_dos_gols['sofridos_mandante_15_30']
            + dados_dos_gols['sofridos_visitante_15_30']
        )
        dados_dos_gols['trinta45'] = (
            dados_dos_gols['feitos_mandante_30_45']
            + dados_dos_gols['feitos_visitante_30_45']
            + dados_dos_gols['sofridos_mandante_30_45']
            + dados_dos_gols['sofridos_visitante_30_45']
        )
        dados_dos_gols['quarentacinco60'] = (
            dados_dos_gols['feitos_mandante_45_60']
            + dados_dos_gols['feitos_visitante_45_60']
            + dados_dos_gols['sofridos_mandante_45_60']
            + dados_dos_gols['sofridos_visitante_45_60']
        )
        dados_dos_gols['sessenta75'] = (
            dados_dos_gols['feitos_mandante_60_75']
            + dados_dos_gols['feitos_visitante_60_75']
            + dados_dos_gols['sofridos_mandante_60_75']
            + dados_dos_gols['sofridos_visitante_60_75']
        )
        dados_dos_gols['setentacinco90'] = (
            dados_dos_gols['feitos_mandante_75_90']
            + dados_dos_gols['feitos_visitante_75_90']
            + dados_dos_gols['sofridos_mandante_75_90']
            + dados_dos_gols['sofridos_visitante_75_90']
        )

        dados_dos_gols['ht'] = (
            dados_dos_gols['zero15']
            + dados_dos_gols['quinze30']
            + dados_dos_gols['trinta45']
        )
        dados_dos_gols['ft'] = (
            dados_dos_gols['quarentacinco60']
            + dados_dos_gols['sessenta75']
            + dados_dos_gols['setentacinco90']
        )

        return dados_dos_gols
