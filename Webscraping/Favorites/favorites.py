import argparse, sqlite3, os, time, tempfile
from .. import CONNECT, INSERT, SELECT, UPDATE, DELETE, WEBDRIVER, EXT
from ..utils import IncrementalBar, PATH, ARTIST, get_tags, generate_tags, bs4, requests, re
import selenium.common.exceptions as exceptions
from selenium.webdriver.common.keys import Keys
from pathlib import Path

IGNORE = '(too large)|(read query)|(file was uploaded)|(request failed:)'
RATINGS = {3:'explicit', 2:'questionable', 1:'safe'}
MODE = ['checked=0', 'saved=0']

def page_handler(paths, upload, sankaku=0, gelbooru=0):
    
    if not paths: return
    if upload: limit = get_limit()
    progress = IncrementalBar('favorites', max=len(paths))

    for (path, href, src, site,) in paths:
        
        progress.next()
        DRIVER.get('http://iqdb.org/')
        try:
            if src: DRIVER.find('//*[@id="url"]', src, fetch=1)
            else: DRIVER.find('//*[@id="file"]', path, fetch=1)
        except exceptions.InvalidArgumentException:
            MYSQL.execute(UPDATE[4], (1, 0, path), commit=1)
            continue
        DRIVER.find('//input[@type="submit"]', click=True)
        if re.search(EXT[-12:], path, re.IGNORECASE): time.sleep(25)
        else: time.sleep(5)
        
        html = bs4.BeautifulSoup(DRIVER.page_source(), 'lxml')
        if html.find(text=re.compile(IGNORE)):
            MYSQL.execute(UPDATE[4], (1, 0, path), commit=1)
            continue
        try:
            targets = [
            target.find(href=re.compile('/gelbooru|/chan.san')) 
            for target in html.find(id='pages').contents 
            if type(target) != bs4.element.NavigableString and 
            target.findAll(href=re.compile('/gelbooru|/chan.san')) and 
            target.findAll(text=re.compile('(Best)|(Additional) match'))
            ]
        except: continue
        
        if targets: saved = favorite(targets)
        elif upload and (sankaku < limit or gelbooru < 50):
            saved, type_ = upload_image(path, href, src, site)  
            if type_ == 1: sankaku += 1
            elif type_ == 0: gelbooru += 1
        else: saved = False
                        
        if saved and src is None: os.remove(path)
        MYSQL.execute(UPDATE[4], (1, int(saved), path), commit=1)

    print()

def favorite(targets, saved=False):

    for match in targets:

        DRIVER.get(f'https:{match.get("href")}')

        if'gelbooru' in match.get('href'):
            try: DRIVER.find('//*[text()="Add to favorites"]', click=True)
            except: pass
        else:
            element = DRIVER.find('//*[@title="Add to favorites"]')
            try: element.click()
            except exceptions.ElementClickInterceptedException:
                DRIVER.active_element().click()
                element.click()
            except exceptions.ElementNotInteractableException: pass
            except: pass

        saved = True
    
    return saved

def upload_image(path, href, src, site):

    match site:
        case 'foundry':
            
            artist = href.split('/')[3]
            href = f'http://www.hentai-foundry.com{href}'
            
        case 'furaffinity':
            
            artist = src.split('/')[4]
            href = f'https://www.furaffinity.net{href}'
            src = 'http:' + src
            
        case 'pixiv':
            
            artist = path.split('\\')[-1].split('-')[0].strip()
            if href is None:
                href = f"/artworks/{path.split('-')[-1].strip().split('_')[0]}"
            href = f'https://www.pixiv.net{href}'
            
        case 'twitter':
            
            artist = href.split('/')[1]
            href = f'https://twitter.com{href}'
    
    artist = ARTIST.get(artist.lower(), 0)
    if not (artist and src): return False, None
        
    with tempfile.NamedTemporaryFile(suffix='.jpg') as temp:
        
        temp.write(bytes(requests.get(src).content)) 
        tags = get_tags(DRIVER, Path(temp.name))
        if 'comic' in tags: return False, 0

        general, rating = generate_tags(
            general=tags, rating=True, exif=False
            )
        tags = ' '.join(set(tags.split() + general.split() + [artist])).replace('qwd', '')
        if tags.count(' ') < 10: tags + 'tagme'
        
        if site: # sankaku
            DRIVER.get('https://chan.sankakucomplex.com/post/upload')
            DRIVER.find('//*[@id="post_file"]', keys=temp.name)
            DRIVER.find('//*[@id="post_source"]', keys=href)
            DRIVER.find('//*[@id="post_tags"]', keys=tags)
            DRIVER.find(f'//*[@id="post_rating_{RATINGS[rating]}"]', click=True)
            DRIVER.find('//*[@value="Upload"]', click=True)
            DRIVER.find('//*[@title="Add to favorites"]', click=True)
        
        else: # gelbooru
            DRIVER.get('https://gelbooru.com/index.php?page=post&s=add')
            DRIVER.find('//*[@id="fileUpload"]', keys=temp.name)
            DRIVER.find('//*[@name="source"]', keys=href)
            DRIVER.find('//*[@id="tags"]', keys=tags)
            DRIVER.find(f'//*[@id="post_rating_{RATINGS[rating][:1]}"]', click=True)
            DRIVER.find('//*[@value="Upload"]', click=True)
            DRIVER.find('Add to favorites', click=True)
        
        return True, site
  
def get_limit():
    
    DRIVER.get('https://chan.sankakucomplex.com/user/upload_limit')
    html = bs4.BeautifulSoup(DRIVER.page_source(), 'lxml')
    return int(html.find('strong').text)

def edit(search, replace):
    
    address = '/html/body/div[4]/div/div[2]/div[8]/form/table/tfoot/tr/td/input'
    driver = WEBDRIVER(0, None, wait=30)
    driver.login('sankaku', 'chan')
    driver.get(f'https://chan.sankakucomplex.com?tags={search}')
    html = bs4.BeautifulSoup(driver.page_source(), 'lxml')
    hrefs = [
        target.get('href') for target in 
        html.findAll('a', {'onclick': True}, href=re.compile('/p+'))
        ]

    for href in hrefs:

        driver.get(f'https://chan.sankakucomplex.com{href}')
        time.sleep(6)
        html = bs4.BeautifulSoup(driver.page_source(), 'lxml')
        tags = html.find('textarea').contents[0]

        text = re.sub(search.replace('*', '.*'), replace, tags)
        driver.find('//*[@id="post_tags"]').clear()
        driver.find('//*[@id="post_tags"]', keys=text)

        try: element = driver.find(address, click=True)
        except exceptions.ElementClickInterceptedException: 
            driver.active_element().click()
            element.click()
        
def initialize():
    
    data = sqlite3.connect(r'Webscraping\Pixivutil2\db.sqlite')
    MYSQL.execute(
        INSERT[2], data.execute(SELECT[5]).fetchall(), many=1, commit=1
        )
    data.close()
    
    paths = [
        (str(path), None, path.parent.name) 
        for path in (PATH / 'Images').glob('*\*')
        ]

    MYSQL.execute(INSERT[2], paths, many=1, commit=1)
    MYSQL.execute(DELETE[3], commit=1)

def main(initial=True, headless=True, depth=0, upload=0):

    global MYSQL, DRIVER
    MYSQL = CONNECT('desktop')
    DRIVER = WEBDRIVER(headless, wait=30)
    
    if initial: initialize()
    page_handler(
        MYSQL.execute(SELECT[4].format(MODE[upload]), fetch=1)[-depth:], upload
        )
    DRIVER.close()
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='favorites', 
        )
    parser.add_argument(
        '-i', '--init', type=int,
        help='Initial argument (default 1)',
        default=1
        )
    parser.add_argument(
        '-he', '--head', type=bool,
        help='Headless argument (default True)',
        default=True
        )
    parser.add_argument(
        '-d', '--depth', type=int,
        help='Depth argument (default 0)',
        default=0
        )
    parser.add_argument(
        '-u', '--upload', type=int,
        help='Upload argument (default 0)',
        default=0
        )

    args = parser.parse_args()
    
    main(args.init, args.head, args.depth, args.upload)