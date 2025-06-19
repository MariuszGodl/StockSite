from GpwScraper import GpwScraper
from Other.imports import *


def main():
    """
    Main function to run the GPW scraper.
    """
    gpw_scraper = GpwScraper()
    date = str('11-06-2025')
    date = datetime.strptime(date, '%d-%m-%Y').date()
    gpw_scraper.get_data(date)


if __name__ == "__main__":
    main()

