# Enunciado: 
#   Obtener todas las películas y series
#   Obtener la metadata de cada contenido: título, año, sinopsis, link, duración (solo para movies)
#   Guardar la información obtenida en una base de datos, en archivo .json o .csv automáticamente
#   PLUS: Episodios de cada serie
#   PLUS: Metadata de los episodios
#   PLUS: Si es posible obtener mas información/metadata por cada contenido
#   PLUS: Identificar modelo de negocio
# Fecha límite para entrega: martes 25 de enero hasta las 19:00hs.
#
# Sitio a realizar el scraping: https://www.starz.com/ar
#
# Requisitos:
#   Tenes la libertad de utilizar la librería que quieras para realizarlo. 
#   Subir a GitHub el script trabajado junto con un archivo de los resultados que se obtienen al correr el script creado (JSON, xlsx, csv, etc)



from selenium import webdriver
import time
from selenium.webdriver.common.by import By

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

        data = []

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
        
        data.append(titulo)

        metaData = driver.find_elements(By.CLASS_NAME,"meta-list")[0].find_elements(By.TAG_NAME,'li')

        for i in metaData:
            data.append(i.text)

        data.append(link)
        
        desc = driver.find_elements(By.CLASS_NAME,"logline")[0].find_element(By.TAG_NAME,'P')
        data.append(desc.text)
        
        if q == 'movies':
            x.append(data)
        else: 
            x.append(getEpisodesData(driver, data, delay))

    return x


def getEpisodesData(driver, data, delay):

    y = []

    seasons = driver.find_elements(By.CLASS_NAME,'season-number')
    data.append(f'{len(seasons)} temporadas')

    links = [season.find_element(By.TAG_NAME,'a').get_attribute('href') for season in seasons]

    for link in links:

        driver.get(link)
        driver.maximize_window()

        time.sleep(delay)

        containers = driver.find_elements(By.CLASS_NAME,"title")

        for i in range(0,len(containers)):

            episode = []
            title = containers[i].text
            

            if title != "":

                episode.append(title)

                metaData = driver.find_elements(By.CLASS_NAME,"meta-list")[i+1].find_elements(By.TAG_NAME,'li')

                for j in metaData:
                    episode.append(j.text)
            
            y.append(episode)

            

    data.append(y)

    return data

PATH = "C:\\Users\\Juanks\\Desktop\\Stuff\\CODING\\Python\\ScrapingTest\\chromedriver.exe"

driver = webdriver.Chrome(PATH)




pageNavigation(driver, 'movies', 3, 2)

movieLinks = getLinks(driver)

peliculas = [getData(movieLinks, 'movies', 2)]


pageNavigation(driver, 'series', 2, 2)

serieLinks = getLinks(driver)

series = [getData(serieLinks, 'series', 2)]

print(peliculas)

print(series)

