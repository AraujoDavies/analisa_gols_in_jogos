from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from codigo.academia import AcademiaDasApostas

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_expansao_das_partidas_escondidas():
    AcademiaDasApostas(driver).expand_all_matches()
    partidas_escondidas = driver.find_elements('xpath', '//td[contains(@class, "footer")]')
    assert partidas_escondidas == []

def test_coleta_de_informacoes_iniciais_dos_jogos():
    list_info_jogos = AcademiaDasApostas(driver).coletando_url_e_informacoes_iniciais()
    assert len(list_info_jogos) > 1

def test_click_que_abre_nova_lista_de_jogos():
    assert AcademiaDasApostas(driver).click_to_go_next_day_matches() == True

def test_coleta_de_infos_de_gols():
    url = 'https://www.academiadasapostasbrasil.com/stats/match/inglaterra/premier-league/wolverhampton/man-utd/3JnZMV3K5mVxv'
    assert bool(AcademiaDasApostas(driver).coletar_info_de_gols(url)) == True

