from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


def pageNavigation(driver, q, index, delay):

    # El parametro index depende del link al que queramos acceder (del navbar -> series o peliculas)

    url = 'https://www.starz.com/ar'

    driver.get(url)
    driver.maximize_window()

    time.sleep(delay)

    driver.find_element(By.XPATH,f'//*[@id="view-container"]/starz-header/header/div/div/div[1]/a[{index}]').click()
                                    
    time.sleep(delay)

    driver.find_element(By.XPATH,f'//*[@id="subview-container"]/starz-{q}/div/starz-block-page-render/div/starz-dynamic-container[{index - 1}]/div/div/div/starz-std-slider/div/div[1]/a').click()
    time.sleep(delay)
    driver.find_elements(By.XPATH, '//*[@id="subview-container"]/starz-view-all/div/div/div/div/div/div/section/nav/ul/li[1]')[0].click()

    time.sleep(delay)

    return


def getLinks (driver):
    links = [elem.find_element(By.TAG_NAME,'a').get_attribute('href') for elem in driver.find_elements(By.CLASS_NAME,"content-title")]

    # Elimino los duplicados.

    for link in links:
        if links.count(link) > 1:
            links.remove(link)

    return links


def getData(links, q, delay):

    x = []

    for link in links:

        d = {}

        driver.get(link)
        driver.maximize_window()

        time.sleep(delay)

        titulo = driver.find_element(By.ID, f'{q}DetailsH1')

        # Formateo el titulo

        if q == 'movies':
            if 'Ver' in titulo.text:
                titulo = titulo.text[4:]
                if 'online' in titulo:
                    titulo = titulo[:-7]
        else:
            titulo = titulo.text
        
        d['titulo'] = titulo

        metaData = driver.find_elements(By.CLASS_NAME,"meta-list")[0].find_elements(By.TAG_NAME,'li')

        if q == 'movies': 
            metalistKeys = ['calificacion', 'duracion', 'genero', 'año', 'sonido']
        else:
            metalistKeys = ['calificacion', 'episodios', 'género', 'año', 'sonido']

        for i in range(0,len(metaData)):
            d[metalistKeys[i]]=metaData[i].text
            
        d['link']=link
        
        desc = driver.find_elements(By.CLASS_NAME,"logline")[0].find_element(By.TAG_NAME,'P')
        d['sinopsis']=desc.text
        
        if q == 'movies':
            x.append(d)

        else: 
            d['zepisodios']=getEpisodesData(driver, delay)
            x.append(d)
        
    return x


def getEpisodesData(driver, delay):

    episodios = []

    seasons = driver.find_elements(By.CLASS_NAME,'season-number')

    links = [season.find_element(By.TAG_NAME,'a').get_attribute('href') for season in seasons]

    for link in links:

        driver.get(link)
        driver.maximize_window()

        time.sleep(delay)

        containers = driver.find_elements(By.CLASS_NAME,"title")

        for i in range(0,len(containers)):

            episode = {}
            titulo = containers[i].text

            if titulo != "":
                episode['titulo'] = titulo

                metaData = driver.find_elements(By.CLASS_NAME,"meta-list")[i+1].find_elements(By.TAG_NAME,'li')
                metalistKeys = ['calificacion', 'duracion', 'año', 'sonido']

                for j in range(0,len(metaData)):

                    episode[metalistKeys[j]]=metaData[j].text

                episodios.append(episode)
    

    return episodios

PATH = "C:\\Users\\Juanks\\Desktop\\Stuff\\CODING\\Python\\ScrapingTest\\chromedriver.exe"

driver = webdriver.Chrome(PATH)

data = {}

pageNavigation(driver, 'movies', 3, 2)

movieLinks = getLinks(driver)

data['peliculas'] = getData(movieLinks, 'movies', 2)

pageNavigation(driver, 'series', 2, 2)

serieLinks = getLinks(driver)

data['series'] = getData(serieLinks, 'series', 2)


with open('results.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii= False,  indent=4)

driver.close()