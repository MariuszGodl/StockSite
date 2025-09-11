from SyncScraper import SyncStockScraper
from Other.imports import *
from Other.constants import *
from industry_clasification import company_classifcation
from RemovePolishchars import strip_polish_chars
from ETLDayValue import etl_day_value

load_dotenv()

class GpwScraper(SyncStockScraper):
    """
    Concrete implementation of StockScraper for GPW (Giełda Papierów Wartościowych w Warszawie).
    This class implements the abstract methods defined in StockScraper.
    """
    def __init__(self):
        """
        Initializes the GpwScraper instance.
        With initial URLs for fetching data from GPW.
        """
        super().__init__()

        # Load configuration from JSON file
        with open(GPW_JSON, 'r') as file:
            self.config = json.load(file)

        self.__url_template = self.config['url_template']
        self.__downloads_path = os.path.normpath(os.path.join(os.getcwd(), self.config["downloads_path"]))
        self.error_file_path = os.path.normpath(os.path.join(os.getcwd(), self.config["error_file_path"]))
        self.options = Options()
        # self.options.add_argument("--window-size=100,100")
        self.options.add_experimental_option("prefs", {
            "download.default_directory": self.__downloads_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        self.service = Service(DRIVER_PATH)

    def accepting_cookies(self, cookie_accept, wait) -> None:
        if cookie_accept:
            try:
                # Wait for the cookie accept button to appear (adjust selector!)
                cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
                cookie_button.click()
            except (TimeoutException, NoSuchElementException):
                print("No cookie banner found or already accepted")


    def get_data(self, date, cookie_accept=True, remove_if_exist=False) -> None:
        """
        Fetches data for a given date from GPW.

        :param date: The date for which data is to be fetched in 'DD-MM-YYYY' format.
        :param cookie_accept: If True, accepts cookies on the website.
        :param remove_if_exist: If True, removes the file if it already exists before downloading.
        """
        file_name = self.config['file_prefix'] + str(date) + self.config['file_suffix']
        file_path = os.path.join(self.__downloads_path, file_name)

        if not self.check_if_file_exists(file_path, remove=False) or remove_if_exist:

            date_reversed = date.strftime('%Y-%m-%d')
            site = self.__url_template.format(date=date_reversed)
            self.driver.get(site)
            wait = WebDriverWait(self.driver, self.config['wait_time'])

            self.accepting_cookies(cookie_accept, wait)
            try:
                # Wait for the ability to download the file
                file_download = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-icon")))
                file_download.click()
            except (TimeoutException, NoSuchElementException):
                print("File from " + date + " no option to download")
                with open(self.error_file_path, 'a') as error_file:
                    error_file.write(
                        f"At time {datetime.datetime.now()} option to download {str(date)} not found after waiting "
                        f"{self.config['wait_time']} seconds.\n")

            print(f"Expected file path: {file_path}")

            # Check if the file already exists and remove it if necessary
            self.check_if_file_exists(file_path, remove=True)

            # Wait until the file is downloaded
            self.wait_until_file_downloaded(file_path, self.error_file_path, timeout=TIME_TO_DOWNLOAD)
            etl_day_value(file_name, True)

            return True

        return False  # File already exists, no need to download again


    def get_companies(self, mode):
        """
        Fetches a list of companies listed on the GPW.
        :param mode: if 0 take it from database if 1 get it from the data
        """
        # Implementation goes here
        # Request to the database
        # Returns a tuple with (ID, name, starting date)
        #TODO database
        if mode == 1 :
            ExchangePath = 'StockData/GPW'
            companies = set()
            unique = []
            for CurrentFile in os.listdir(ExchangePath):
                file_path = os.path.join(ExchangePath, CurrentFile)
                df = pd.read_excel(file_path)

                if 'Nazwa' in df.columns:
                    for company in df['Nazwa']:
                        if company not in companies:
                            unique.append(company)
                            companies.add(company)
            #print(unique)
            return unique
        else:
            try:
                conn = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                )
                if conn.is_connected():
                    print("Connected")

                cursor = conn.cursor()
                select_query = "SELECT Identifier FROM Company"

                cursor.execute(select_query)
                unique_companies = cursor.fetchall() 
                conn.commit()
                print("Record inserted successfully")

            except Error as e:
                print(f"Error: {e}")

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
                    print("MySQL connection closed")
            clean_list = [company[0] for company in unique_companies]
            return clean_list
        pass


    def get_yesterday_prices(self):
        """
        Fetches today's prices for the companies listed on the GPW.
        """
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        yesterday_date = datetime.datetime.now().date() - timedelta(days=1)
        self.get_data(yesterday_date)
        self.driver.quit()
        pass


    def get_historical_prices(self, start_date=None, end_date=None):
        """
        Fetches historical prices for a given company listed on the GPW.
        :param start_date: The start date for the historical prices in 'DD-MM-YYYY' format.
        :param end_date: The end date for the historical prices in 'DD-MM-YYYY' format.
        """
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        if start_date is None:
            start_date = datetime.datetime.strptime(self.config['initial_date'], "%Y-%m-%d").date()

        if end_date is None:
            end_date = datetime.datetime.now().date() - timedelta(days=1)

        current_date = end_date

        # Loop through the dates from end_date to start_date to fetch data
        wait = self.get_data(current_date)
        cookie_accept = True
        while current_date > start_date:
            current_date -= timedelta(days=1)

            # Check if the current date is a weekday (Monday to Friday)
            if current_date.weekday() not in [5, 6]:
                # TODO add a check if the data is a holiday
                # Wait if the data was just downloaded to avoid too many requests
                if wait:
                    time.sleep(self.config['wait_between_requests'])
                    cookie_accept = False
                wait = self.get_data(current_date, cookie_accept=cookie_accept)

        self.driver.quit()
        pass


    def scrape_basic_info_bankier(self, box_name, searched_info):

        box = self.driver.find_element(By.ID, box_name)
        # Inside that container, find the <td> with text 'Sektor:'
        label = box.find_element(By.XPATH, f'.//td[contains(text(),"{searched_info}:")]')
        # Get the next sibling <td> which contains the sector text
        searched = label.find_element(By.XPATH, "following-sibling::td").text
        return searched.upper()

    
    def scrape_company_description(self):

        # Find the container with id 'boxDesc'
        box_desc = self.driver.find_element(By.ID, "boxDesc")
        # Inside that container, find the <p> tag with the description text
        description = box_desc.find_element(By.TAG_NAME, "p").text
        return description
    

    def scrape_company_capitalization(self, company, cookie_accept=False):

        url = self.config['url_company_capitalization'].format(company=company)
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 5)#self.config['wait_time'])
        #self.accepting_cookies(cookie_accept, wait) 
        box_desc = self.driver.find_element(By.ID, "boxProfil")
        capitalization_str = box_desc.find_element(
            By.XPATH, ".//td[normalize-space(text())='Kapitalizacja:']/following-sibling::td[1]"
        ).text.strip()

        #print("Capitalization:", capitalization_str)
        capitalization = int(float(capitalization_str.replace("\xa0", "").replace(" ", "").replace(",", ".")))
        #print(capitalization)
        return capitalization
    

    def get_companies_info(self):
        """
        Fetches information about a specific company listed on the GPW.
        :param companies: The names of the companies for which information is to be fetched.
        """
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        cookie_accept = True
        companies = self.get_companies(1)
        print(f"\033[93m{len(companies)}\033[0m")
        for company in companies:
            site = self.config['url_company_info'].format(company=company)
            #add here if 404 continue
            self.driver.get(site)
            # check if page is 404
            time.sleep(3)
            if "#404" in self.driver.current_url:
                print(f"\033[31mSkipping {company}, redirected to 404.\033[0m")
                continue

            wait = WebDriverWait(self.driver, self.config['wait_time'])
            self.accepting_cookies(cookie_accept, wait)

            cookie_accept = False
            company_name = self.scrape_basic_info_bankier("boxBasicData", "Nazwa spółki")
            company_sector = self.scrape_basic_info_bankier("boxBasicData", "Sektor")
            company_shares = self.scrape_basic_info_bankier("boxBasicData", "Liczba akcji")
            company_shares = company_shares.replace(" ", "").replace(",", "")  # remove spaces and commas
            try:
                company_shares = int(company_shares)
            except ValueError:
                company_shares = 0
            company_ceo = self.scrape_basic_info_bankier("boxBasicData", "Prezes")
            company_country = self.scrape_basic_info_bankier("boxAddressData", "Kraj")
            company_city = self.scrape_basic_info_bankier("boxAddressData", "Miejscowość")
            company_info = self.scrape_company_description()
            
            capitalization = self.scrape_company_capitalization(company)
            industry, creation_date = company_classifcation(company_name=company_name, company_ticker=company, company_description=company_info)
            
            company_name = strip_polish_chars(company_name)
            company_sector = strip_polish_chars(company_sector)
            company_ceo = strip_polish_chars(company_ceo)
            company_city = strip_polish_chars(company_city)
            company_country = strip_polish_chars(company_country)
            company_info = strip_polish_chars(company_info)

# -- Company Table
# CREATE TABLE Company (
#     ID INT AUTO_INCREMENT PRIMARY KEY,
#     Identifier VARCHAR(10) NOT NULL CHECK (Identifier REGEXP '^[A-Za-z0-9 ]+$'), 
#     CompanyName VARCHAR(100) NOT NULL CHECK (CompanyName REGEXP '^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż &-.,;:]+$'),
#     CEO VARCHAR(100) NOT NULL CHECK (CEO REGEXP '^[A-Za-z0-9ĄąĆćĘęŁłŃńÓóŚśŹźŻż &-.,;:]+$'),
#     Industry VARCHAR(100) NOT NULL CHECK (Industry REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż &-.,;:]+$'),
#     Info VARCHAR(5000) NOT NULL,
#     NrOfShares INT NOT NULL CHECK (NrOfShares > 0),
#     Country VARCHAR(100) NOT NULL CHECK (Country REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż &-.,;:]+$'),
#     City VARCHAR(100) NOT NULL CHECK (City REGEXP '^[A-Za-zĄąĆćĘęŁłŃńÓóŚśŹźŻż &-.,;:]+$'),
#     Capitalization INT NOT NULL CHECK (Capitalization > 0),
#     CreationDate DATE NOT NULL,
#     DestructionDate DATE,
#     UNIQUE(Identifier)
# );


            print(
                "\n".join(
                    f"{name} ({type(value)}): {value}"
                    for name, value in [
                        ("company", company),
                        ("company_name", company_name),
                        ("company_ceo", company_ceo),
                        ("industry", industry),
                        ("company_info", company_info),
                        ("company_shares", company_shares),
                        ("company_country", company_country),
                        ("company_city", company_city),
                        ("capitalization", capitalization),
                        ("creation_date", creation_date),
                    ]
                )
            )
            try:
                conn = mysql.connector.connect(
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    database=os.getenv("DB_NAME"),
                )
                if conn.is_connected():
                    print("Connected")

                cursor = conn.cursor()
                
                insert_query = """
                    INSERT INTO Company
                    (Identifier, CompanyName, CEO, Industry, Info, NrOfShares, Country, City, Capitalization, CreationDate, DestructionDate)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                data_tuple = (
                    company,
                    company_name,
                    company_ceo,
                    industry,
                    company_info,
                    company_shares,
                    company_country,
                    company_city,
                    capitalization,
                    creation_date,
                    None
                )

                cursor.execute(insert_query, data_tuple)
                conn.commit()
                #select the company, need CompanyId and then connect it to GPW
                print("Record inserted successfully")

            except Error as e:
                print(f"Error: {e}")

            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
                    print(f"\033[31mMySQL connection closed\033[0m")
            #
            time.sleep(self.config['wait_between_requests'])
        self.driver.quit()
        pass

