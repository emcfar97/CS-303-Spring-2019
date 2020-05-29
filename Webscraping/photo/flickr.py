from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException, ElementClickInterceptedException
import mysql.connector as sql
    
DATAB = sql.connect(
    user='root', password='SchooL1@', database='userData', 
    host='192.168.1.43' if __file__.startswith(('e:\\', 'e:/')) else '127.0.0.1'
    )
CURSOR = DATAB.cursor()
SITE = 'flickr'
TYPE = 'Erotica 2'

def initialize(driver, url='/photos/140284163@N04/favorites/page1', query=0):
    
    def next_page(page):
             
        try: return page.get('href')[:-1]
        except IndexError: return False

    if not query:
        CURSOR.execute(SELECT[0], (SITE,))
        query = set(CURSOR.fetchall())
    driver.get(f'https://www.flickr.com{url}')
    for _ in range(2):
        driver.find_element_by_tag_name('html').send_keys(Keys.END)
        time.sleep(2)

    html = bs4.BeautifulSoup(driver.page_source, 'lxml')
    while True:
        try:
            hrefs = [
                (target.get('href'), SITE) for target in 
                html.findAll('a', class_='overlay', href=True)
                if (target.get('href'),) not in query
                ]
            break
        except sql.errors.OperationalError: continue
    while True:
        try: CURSOR.executemany(INSERT[0], hrefs); break
        except sql.errors.OperationalError: continue
        
    next = next_page(html.find('a', {'data-track':'paginationRightClick'}))
    if hrefs and next: initialize(driver, next, query)
    while True:
        try: DATAB.commit(); break
        except sql.errors.OperationalError: continue
    
def page_handler(driver, hrefs):

    if not hrefs: return
    size = len(hrefs)
    hasher = hashlib.md5()
    view = 'view.photo-notes-scrappy-view'
    elment = 'view.photo-well-scrappy-view.requiredToShowOnServer'

    for num, (href,) in enumerate(hrefs):
        
        progress(size, num, SITE)
        driver.get(f'https://www.flickr.com{href}')
        
        try:
            element = driver.find_element_by_class_name(view)
            ActionChains(driver).move_to_element(element).perform()
            for _ in range(50):
                try: driver.find_element_by_class_name(elment).click()
                except ElementClickInterceptedException: break
            else: continue

            image = driver.find_element_by_class_name('zoom-large').get_attribute('src')
            tags = get_tags(driver, image)
            tags, rating, exif = generate_tags(
                type='Erotica 2', general=tags, custom=True, rating=True
                )
            name = get_name(image, 0)
            save_image(name, image, exif)

        except:
            try:
                video = driver.find_element_by_xpath(
                    '//*[@id="video_1_html5_api"]'
                    )
                image = video.get_attribute('src')
                ext = image.split('.')[-1]
                data = requests.get(image).content
                hasher.update(data)
                with open(name, 'wb') as file: file.write(data) 
                ext = image.split('.')[-1]
                name = save_image(
                    join(PATH, 'エラティカ ニ', f'{hasher.hexdigest()}.{ext}'), image
                    )
                tags = get_tags(driver, name)
                tags, rating = generate_tags(
                    type='Erotica 2', general=tags, 
                    custom=True, rating=True, exif=False
                    )

            except:
                try:
                    status = driver.find_element_by_class_name('statusCode')
                    if status.text == '404':
                        for _ in range(50):
                            try:
                                CURSOR.execute(UPDATE[3], (
                                    f'404 - {href}', None, None, 
                                    None, None, None, 0, href)
                                    )
                                DATAB.commit()
                                break
                            except: continue
                        continue
                except: continue
            
        hash_ = get_hash(name) 
        
        while True:
            try:
                CURSOR.execute(UPDATE[3], (
                    name, ' ', f" {tags} ", rating, image, hash_, 0, href)
                    )
                DATAB.commit()
                break
            except sql.errors.IntegrityError:
                name, ext = name.split('.')
                name = f'{name}1.{ext}'
                CURSOR.execute(UPDATE[3], (
                    name, ' ', f" {tags} ", rating, image, hash_, 0, href)
                    )
                DATAB.commit()
                break
            except (sql.errors.OperationalError, sql.errors.DatabaseError): continue
    
    progress(size, size, SITE)

def setup(initial=True):
    
    try:
        driver = get_driver(headless=True)
        login(driver, SITE)
        if initial: initialize(driver)
        CURSOR.execute(SELECT[2],(SITE,))
        page_handler(driver, CURSOR.fetchall())
    except WebDriverException:
        if input(f'{SITE}: Browser closed\nContinue? ').lower() in 'yes': 
            setup(False)
    except Exception as error:
        print(f'{SITE}: {error}')
        
    try: driver.close()
    except: pass
    DATAB.close()

if __name__ == '__main__':
    
    from utils import *
    setup()

else: from .utils import *