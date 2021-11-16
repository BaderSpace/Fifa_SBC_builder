from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import undetected_chromedriver as uc
import time
import csv
import os

op = uc.ChromeOptions()
op.add_argument('--log-level=3')
driver = uc.Chrome(options=op)
wait = WebDriverWait(driver, 50)


def get_the_squads():
    driver.get('https://www.futbin.com/squad-building-challenges')
    ch_name = input('Enter the challenge name: ')
    wait.until(EC.presence_of_element_located(
        (By.ID, "sbc-search"))).send_keys(ch_name)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    challenges = soup.find_all(
        'div', {'class': 'col-md-3 col-xs-6 set_col mb-5'})
    for i in challenges:
        if i.has_attr('style'):
            pass
        else:
            driver.get('https://www.futbin.com'+i.findChild('a',
                       {'style': 'text-decoration: none;'})['href'])
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    challenge_name = str(
        soup.find('h1', {'class': 'chal_page_name'}).text).strip()
    subChallnge_name = soup.find_all('div', {'class': 'chal_name'})
    create_folders(challenge_name, subChallnge_name)
    subChallnges = soup.find_all('div', {'class': "btn_holder"})
    for sc in subChallnges:
        driver.get('https://www.futbin.com'
                   + sc.findChild('a', {'class': 'chal_view_btn'})['href'])
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        subChNm = str(
            soup.find('h6', {'class': 'chal_page_name'}).text).strip()
        squads = soup.find_all('a', {'class': 'squad_url'})
        for squad in squads:
            r = requests.get("https://www.futbin.com" + squad['href'])
            squad_name = str(squad.text).strip()
            get_players_info(r, squad_name, challenge_name, subChNm)


def get_club_players():
    players_name = []
    players_rate = []
    players_pos = []
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'icon-club'))).click()
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'players-tile'))).click()
    while True:

        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'rating')))
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'name')))
        wait.until(EC.visibility_of_all_elements_located)
        wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'player')))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        players = soup.find_all('div', {'class': 'entityContainer'})
        for player in players:
            #check if loan or not
            loan_check = player.findChild(
                'div', {'class': 'ut-item-player-status--loan'}).text
            if len(loan_check) == 0:
                web_player_name = player.findChild(
                    'div', {'class': 'name'}).text
                web_player_rating = player.findChild(
                    'div', {'class': 'rating'}).text
                web_player_pos = player.findChild(
                    'div', {'class': 'position'}).text
                players_name.append(web_player_name)
                players_rate.append(web_player_rating)
                players_pos.append(web_player_pos)
            else:
                pass

        try:
            driver.find_element(By.CLASS_NAME, 'next').click()
        except:
            break

    with open('./club/club_players.csv', 'w+', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Player_name', 'Player_rate', 'Player_pos'])
        for i in range(len(players_name)):
            writer.writerow([players_name[i], players_rate[i], players_pos[i]])


def get_players_info(r, sqNm, pathName, subPathName):
    futbin_pNms = []
    futbin_pRts = []
    futbin_pPos = []
    futbin_Rpos = []
    soup = BeautifulSoup(r.text, "html.parser")
    players = soup.find_all(
        'div', {"class": 'card cardnum ui-droppable added'})

    for i in players:
        player_name = i.find('div', {'class': 'pcdisplay-name'}).text
        player_rating = i.find('div', {'class': 'pcdisplay-rat'}).text
        player_pos = i.find('div', {'class': 'pcdisplay-pos'}).text
        real_pos = i['data-formpos']
        futbin_pNms.append(player_name)
        futbin_pRts.append(player_rating)
        futbin_pPos.append(player_pos)
        futbin_Rpos.append(real_pos)

    with open(rf'./squads/{pathName}/{subPathName}/{sqNm}.csv', 'w+', encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Player_name', 'Player_rate',
                        'Player_pos', 'Player_form_pos'])
        for pl in range(len(futbin_pNms)):
            writer.writerow([futbin_pNms[pl], futbin_pRts[pl],
                            futbin_pPos[pl], futbin_Rpos[pl]])
        pass


def go_to_sbc():
    driver.find_element(By.CLASS_NAME, 'icon-sbc').click()

#Check the players if they're availble in the club or no


def Check_players_avalibilty():
    pass


def Login(usr, pas):
    driver.get('https://www.ea.com/fifa/ultimate-team/web-app/')
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//*[@id="Login"]/div/div/button[1]'))).click()
    wait.until(EC.presence_of_all_elements_located)
    driver.find_element(By.ID, 'email').send_keys(
        usr, Keys.TAB, pas, Keys.ENTER)
    wait.until(EC.presence_of_element_located(
        (By.ID, 'btnSendCode'))).click()
    Code = input("Enter the verfaction code: ")
    driver.find_element(By.NAME, 'oneTimeCode').send_keys(Code, Keys.ENTER)


def create_folders(chal_name, subChal_name):
    if not os.path.exists(rf'./squads/{chal_name}'):
        os.mkdir(rf'./squads/{chal_name}')
    else:
        pass
    for i in subChal_name:
        if not os.path.exists(rf'./squads/{chal_name}/{str(i.text).strip()}'):
            os.mkdir(rf'./squads/{chal_name}/{str(i.text).strip()}')
        else:
            pass


#Login()
#get_club_players()
get_the_squads()
#get_players_info()
#driver.quit()
