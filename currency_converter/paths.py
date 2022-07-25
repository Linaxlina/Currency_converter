import pathlib

# constants
PROJECT_ROOT_FOLDER = pathlib.Path(__file__).parent
DATA_FOLDER = PROJECT_ROOT_FOLDER.joinpath("conversion_data")
LOG_FILE_NAME = PROJECT_ROOT_FOLDER.joinpath("my_conversions").joinpath("all_conversions.csv")
COUNTRIES_DATA_FILE = DATA_FOLDER.joinpath("country_code_and_details.json")




