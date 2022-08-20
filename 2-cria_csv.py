# Importa as opções do Firefox
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
import json
from time import sleep 
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# abrindo o Navegador e Request
service = ChromeService(executable_path=ChromeDriverManager().install())
f = webdriver.Chrome(service=service)
wdw = WebDriverWait(f, 30, poll_frequency=1)
jogos = []

with open('urls.json') as all_urls:
    urls = json.load(all_urls)

def trata_html(input):
    return " ".join(input.split()).replace('> <','><')

def wait(f):
    """
        Clica na aba 'Últimos 10 jogos' e retorna TRUE se o click ocorreu de fato
    """
    try:
        click = f.find_element(By.XPATH, '//li[@data-id = "last_10g"][@market="teams_goals"]')
        click.click()
        last_ten = f.find_element(By.XPATH, '//li[@data-id = "last_10g"][@market="teams_goals"][contains(@class, "current")]')
        if bool(last_ten) == False: 
            print('esperando click nos "10 ultimos" ')
        return bool(last_ten)
    except:
        print('wait nao confirmou click')

def html_bs4():
    """
        Cria o obj soup e passa p função de tratamento
    """
    jogo = {}
    wdw.until(wait, 'Não foi possível coletar dados pois a def wait nao retornou TRUE')
    sleep(1)
    html = f.find_element(By.XPATH, '//div[@id="main-container"]').get_attribute("outerHTML")
    html = trata_html(html)
    soup = BeautifulSoup(html, 'html.parser')
    gm = soup.find_all('td', text = 'G.Marc') # todos os "gols marcados
    gs = soup.find_all('td', text = 'G.Sofr') # todos os "gols Sofridos"
    # indices 3, 4 e 5
    gm_casa = [] 
    gs_casa = []
    # indice 9, 10 e 11
    gm_fora = []
    gs_fora = []
    # soma todos os gols do 2°T
    qt_gols_2T = 0
    # soma dos minutos 46 a 75 INDICE 3 e 4 + 9 e 10
    daronco = 0
    # soma dos 15 minutos finais INDECE 5 + 11
    limit = 0
    for i in range(len(gm)):
        if i == 3 or i == 4 or i == 5: 
            gm_casa.append(int(gm[i].findNext('td').text)) # gols marcados - casa
            gs_casa.append(int(gs[i].findNext('td').text)) # gols sofridos - casa
            soma_gols = int(gm[i].findNext('td').text) + int(gs[i].findNext('td').text) 
            qt_gols_2T += soma_gols
            if i != 5:
                sumdaronco = int(gm[i].findNext('td').text) + int(gs[i].findNext('td').text) 
                daronco += sumdaronco
            else:
                sumlimit = int(gm[i].findNext('td').text) + int(gs[i].findNext('td').text) 
                limit += sumlimit
        elif i == 9 or i == 10 or i == 11: 
            gm_fora.append(int(gm[i].findNext('td').text)) # gols marcados - fora
            gs_fora.append(int(gs[i].findNext('td').text)) # gols sofridos - fora
            soma_gols = int(gm[i].findNext('td').text) + int(gs[i].findNext('td').text)
            qt_gols_2T += soma_gols
            if i != 11:
                sumdaronco = int(gm[i].findNext('td').text) + int(gs[i].findNext('td').text) 
                daronco += sumdaronco
            else:
                sumlimit = int(gm[i].findNext('td').text) + int(gs[i].findNext('td').text) 
                limit += sumlimit
    
    match_info =  soup.find('div', class_='global').find('div', class_='stats stat-area'
    ).find('td', class_="stats-game-head-teamname hide-mobile").findParent('tr')
    
    mandante = match_info.find_all('td')[0].find_all('a')[1].text
    visitante = match_info.find_all('td')[2].find_all('a')[1].text
    data = match_info.find_all('td')[1].find_all('ul')[1].find_all('li')[0].text
    campeonato = match_info.find_all('td')[1].find_all('ul')[1].find_all('li')[1].text

    data = data.replace(" - ", "-").split('-')
    jogo['dia'] = data[0]
    jogo['hora'] = data[1]
    jogo['campeonato'] = campeonato
    jogo['mandante'] = mandante
    jogo['visitante'] = visitante
    jogo['qt_gols_2T'] = qt_gols_2T
    jogo['daronco'] = daronco
    jogo['limit'] = limit
    jogo['gm_casa'] = gm_casa
    jogo['gs_casa'] = gs_casa
    jogo['gm_fora'] = gm_fora
    jogo['gs_fora'] = gs_fora

    jogos.append(jogo)
    print(f'Successfuly!! jogo do {mandante} adicionado')

try:
    for i in urls.keys(): # range => quantidade de dias q quer analisar
        for url in urls[i]:
            f.get(url)
            wait(f)
            html_bs4()
except:  
    print('ERROR: processo de execução caindo no except - Verificar planilha e urls.json')
finally:
    dataset = pd.DataFrame(jogos)
    dataset.to_csv(f"{'./jogos_da_semana.csv' if len(urls.keys()) > 2 else './jogos_do_fim_de_semana.csv'}", sep=';', index = False, encoding = 'utf-8-sig')       
print(jogos)
f.quit()