import os
import sys
from pathlib import Path

import kaggle
import pandas as pd

sys.path.append(os.path.dirname(__file__))
from conf import Config
from py_logger import logger as _logger

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)


class DataLoader:
    """
    A class to handle downloading and loading data for Kaggle competitions or datasets.

    Attributes:
        competition_name (str): The name of the Kaggle competition.
        dataset_name (str): The name of the Kaggle dataset.
        download_path (Path): The path where the data will be downloaded.
    """

    def __init__(self, competition_name=None, dataset_name=None, download_path=None):
        """
        Initializes the DataLoader with the given competition name, dataset name, and download path.

        Args:
            competition_name (str, optional): The name of the Kaggle competition. Defaults to None.
            dataset_name (str, optional): The name of the Kaggle dataset. Defaults to None.
            download_path (Path, optional): The path where the data will be downloaded. Defaults to a 'data' directory.
        """
        self.competition_name = competition_name or Config.KAGGLE_COMPETITION_NAME
        self.dataset_name = dataset_name or Config.KAGGLE_DATASET_NAME
        self.download_path = download_path or Path(os.path.dirname(__file__), "../..", "data")

    def load(self):
        """
        Loads the training and test data from the download path. If the required files are not found,
        it downloads the data first.

        Returns:
            tuple: A tuple containing the training DataFrame and the test DataFrame.
        """
        # Check if the data is already downloaded (must contain submission.csv, test.csv, train.csv)
        required_files = ['submission.csv', 'test.csv', 'train.csv']
        missing_files = [file for file in required_files if not os.path.exists(os.path.join(self.download_path, file))]
        if missing_files:
            _logger.info(f"Missing files detected ({missing_files}), downloading data...")
            self.download_data()

        # Load the data
        train_df = pd.read_csv(os.path.join(self.download_path, 'train.csv'))
        test_df = pd.read_csv(os.path.join(self.download_path, 'test.csv'))
        
        return train_df, test_df
    
    def download_data(self):
        """
        Downloads the data from Kaggle based on the competition name or dataset name provided.

        Raises:
            ValueError: If neither competition_name nor dataset_name is provided.
        """
        if self.competition_name:
            kaggle.api.competition_download_files(self.competition_name, path=self.download_path)
        elif self.dataset_name:
            kaggle.api.dataset_download_files(self.dataset_name, path=self.download_path, unzip=True)
        else:
            raise ValueError("Either competition_name or dataset_name must be provided.")


if __name__ == "__main__":
    
    DataLoader().load()
