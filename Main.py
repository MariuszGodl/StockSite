from GpwScraper import GpwScraper
from Other.imports import *


def main():
    """
    Main function to run the GPW scraper.
    """
    load_dotenv()

    gpw_scraper = GpwScraper()
    # date = datetime.date(2025, 6, 19) - datetime.timedelta(days=1)
    # gpw_scraper.get_data(date)
    # gpw_scraper.get_yesterday_prices()
    # gpw_scraper.get_historical_prices(
    #     datetime.date(1990, 1, 1),
    #     datetime.date(1999,5, 30))
    # print(datetime.date(2025, 6, 16).weekday())
    gpw_scraper.get_companies_info()


if __name__ == "__main__":
    main()

