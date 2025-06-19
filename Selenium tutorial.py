from Other.imports import *


DRIVERPATH = r"Other\chromedriver.exe"
DOWNLOADSPATH = r"StockData\GPW"

downloads_path = os.path.join(os.getcwd(), DOWNLOADSPATH)

options = Options()
options.add_experimental_option("prefs", {
    "download.default_directory": downloads_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

service = Service(DRIVERPATH)
driver = webdriver.Chrome(service=service, options=options)

Url = 'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date=11-06-2025&show_x=Poka%C5%BC+wyniki'
date = '11-06-2025'
__UrlFirst = 'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date='
__UrlLast = '&show_x=Poka%C5%BC+wyniki'
site = str(__UrlFirst + date + __UrlLast)
driver.get(site)

wait = WebDriverWait(driver, 5)

try:
    # Wait for the cookie accept button to appear (adjust selector!)
    cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    cookie_button.click()
    print("Cookie banner accepted")
except:
    print("No cookie banner found or already accepted")

try:
    # Wait for the cookie accept button to appear (adjust selector!)
    cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-icon")))
    cookie_button.click()
    print("Cookie banner accepted")
except:
    print("No cookie banner found or already accepted")

time.sleep(5)

Url = 'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date=11-06-2020&show_x=Poka%C5%BC+wyniki'
date = '11-06-2020'
__UrlFirst = 'https://www.gpw.pl/archiwum-notowan?fetch=0&type=10&instrument=&date='
__UrlLast = '&show_x=Poka%C5%BC+wyniki'
site = str(__UrlFirst + date + __UrlLast)
driver.get(site)

wait = WebDriverWait(driver, 5)

try:
    # Wait for the cookie accept button to appear (adjust selector!)
    cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    cookie_button.click()
    print("Cookie banner accepted")
except:
    print("No cookie banner found or already accepted")

try:
    # Wait for the cookie accept button to appear (adjust selector!)
    cookie_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-icon")))
    cookie_button.click()
    print("Cookie banner accepted")
except:
    print("No cookie banner found or already accepted")

time.sleep(5)
driver.quit()