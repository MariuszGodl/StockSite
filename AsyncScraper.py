from abc import ABC, abstractmethod
from Other.imports import *
from Other.constants import *


class AsyncStockScraper(ABC):

    @abstractmethod
    async def get_data(self, date) -> None:
        """
        Abstract method to fetch data for a given date.
        Must be implemented by subclasses.

        :param date: The date for which data is to be fetched in 'DD-MM-YYYY' format.
        """
        pass

    @abstractmethod
    async def get_companies(self) -> None:
        """
        Abstract method to get a list of companies from given stock exchange.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def get_yesterday_prices(self) -> None:
        """
        Abstract method to get today's prices for the companies.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    async def get_historical_prices(self, start_date, end_date) -> None:
        """
        Abstract method to get historical prices for a given company.
        Must be implemented by subclasses.

        :param start_date: The start date for the historical prices in 'DD-MM-YYYY' format.
        :param end_date: The end date for the historical prices in 'DD-MM-YYYY' format.
        """
        pass

    @abstractmethod
    async def get_companies_info(self, companies) -> None:
        """
        Abstract method to get information about a specific company.
        Must be implemented by subclasses.

        :param companies: The names of the companies for which information is to be fetched.
        """
        pass

    @staticmethod
    async def wait_until_file_downloaded(file_path, error_file_path, timeout=30) -> bool:
        """
        Waits until a file is downloaded.

        :param file_path: The name of the file to wait for.
        :param timeout: Maximum time to wait for the file in seconds.
        :param error_file_path: Path to the error log file.
        :return: True if the file is downloaded, False if not.
        """
        print(file_path)
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(file_path):
                print(f"File {file_path} downloaded successfully.")
                return True
            time.sleep(1)

        # If the file is not found after the timeout
        with open(error_file_path, 'a') as error_file:
            error_file.write(f"At time {datetime.datetime.now()} File {file_path} not found after waiting {timeout} seconds.\n")
        print(f"File {file_path} not found in the download directory after waiting {timeout} seconds.")
        return False

    @staticmethod
    async def check_if_file_exists(file_path, remove=False) -> bool:
        """
        Checks if a file exists at the given path.

        :param file_path: The path to the file to check.
        :param remove: If True, the file will be removed if it exists.
        :return: True if the file exists, False otherwise.
        """
        if os.path.exists(file_path):
            if remove:
                os.remove(file_path)
                print(f"File {file_path} removed.")
            return True

        return False













