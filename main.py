from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
import undetected_chromedriver as uc
import time
import json

op = uc.ChromeOptions()
op.add_argument('--log-level=3')
driver = uc.Chrome(options=op)
wait = WebDriverWait(driver, 50)


def get_the_squads():
    global r
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
    driver.get('https://www.futbin.com'+soup.find('a',
               {'class': "chal_view_btn"})['href'])
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    r = requests.get("https://www.futbin.com"
                     + soup.find('a', {'class': 'squad_url'})['href'])
    pass


def get_club_players():
    players_list = []
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'icon-club'))).click()
    wait.until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'players-tile'))).click()
    while True:
        wait.until(EC.presence_of_all_elements_located)
        players = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'entityContainer')))
        for player in players:
            try:
                #check if loan or not
                loan_check = player.find_element(
                    By.CLASS_NAME, 'ut-item-player-status--loan').text
                if len(loan_check) >= 1:
                    continue
                else:
                    pass
                web_player_name = player.find_element(
                    By.CLASS_NAME, 'name').text
                web_player_rating = player.find_element(
                    By.CLASS_NAME, 'rating').text
                players_list.append(web_player_name)
            except:
                continue
        try:
            driver.find_element(By.CLASS_NAME, 'next').click()
        except:
            break
    for i in players_list:
        print(i)


def get_players_info():
    soup = BeautifulSoup(r.text, "html.parser")
    players = soup.find_all(
        'div', {"class": 'card cardnum ui-droppable added'})

    for i in players:
        player_name = i.find('div', {'class': 'pcdisplay-name'}).text
        player_rating = i.find('div', {'class': 'pcdisplay-rat'}).text
        player_pos = i.find('div', {'class': 'pcdisplay-pos'}).text
        real_pos = i['data-formpos']
        print(player_name, player_pos, player_rating, real_pos)


def go_to_sbc():
    driver.find_element(By.CLASS_NAME, 'ut-tab-bar-item icon-sbc').click()


def Check_player_avalibilty():
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


Login('shnb_07@hotmail.com', 'Asd3546789')
get_club_players()
#get_the_squads()
#get_players_info()
time.sleep(10)
#driver.quit()
