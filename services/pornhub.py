from bs4 import BeautifulSoup
import cloudscraper

URL = 'https://pt.pornhub.com'


def get_latest_videos():
    scraper = cloudscraper.create_scraper(delay=10, browser="chrome")
    page = scraper.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    videos = soup.find_all('li', attrs={'class': 'pcVideoListItem'})
    print(len(videos))
    if not len(videos): return get_latest_videos()
    list = []
    for index, video in enumerate(videos, start=1):
        if video.find('img'):
            image = video.find('img').get('src')
            video_link = video.find('img').get('data-mediabook')
            title = video.find('img').get('alt')
            print(video)
            list.append({'index': index, 'image': image, 'video': video_link, 'title': 'teste', 'title': title})
    if len(list): 
        return list



def search_video(search):
    search = search.replace(' ', '+')
    scraper = cloudscraper.create_scraper()
    page = scraper.get('{}/video/search?search={}'.format(URL, search))
    soup = BeautifulSoup(page.text, 'html.parser')
    return
    if soup.find('div', attrs={'class': 'no-result'}): 
        return []
    main_list = soup.find('div', attrs={'class': 'content'})
    animes = main_list.find_all('div', attrs={'id': 'archive-content'})
    list = []
    for index, anime in enumerate(animes, start=1):
        link = anime.find('a').get('href')
        image = anime.find('img').get('src')
        title = anime.find('')
        list.append({'index': index, 'title': title, 'image': image, 'link': link})
    return list

def get_anime_info(url):
    lista = []
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    content = soup.find('div', attrs={'id': 'seasons'})
    seasons = content.find_all('div', attrs={'class': 'se-c'})
    for index, item in enumerate(seasons, start=1):
        temporada = item.find('span', attrs={'class': 'title'}).text
        lista_episodios = (item.find('ul', attrs={'class': 'episodios'})).find_all('li')
        episodios = []
        for i, episodio in enumerate(lista_episodios, start=1):
            image = episodio.find('img').get('src')
            title = (episodio.find('div', attrs={'class': 'episodiotitle'})).find('a').text
            link = (episodio.find('div', attrs={'class': 'episodiotitle'})).find('a').get('href')
            episodios.append({'index': i, 'title': title, 'image': image, 'link': link})
        lista.append({'index': index,'title': temporada, 'list': episodios})
    return lista

def get_episodio_link(url):
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    iframe_video_link = soup.find('iframe', attrs={'class': 'metaframe rptss'}).get('src')
    return {'video': iframe_video_link}