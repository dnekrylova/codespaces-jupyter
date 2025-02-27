from autogen_ext.models.openai import (
    AzureOpenAIChatCompletionClient,
    OpenAIChatCompletionClient,
)
import os
import dotenv
from autogen_ext.models.openai.config import ResponseFormat
from logging import FileHandler, Formatter, Logger, getLogger, INFO
from datetime import datetime
from colorama import Fore, Style

dotenv.load_dotenv()


def clear_console():
    os.system("cls")


def print_answer(answer):
    print(Style.BRIGHT + Fore.GREEN + f"Final answer:\n{answer}" + Style.RESET_ALL)


def get_azure_model_client():
    model_client = AzureOpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
        api_version="2024-08-01-preview",
        temperature=0,
    )
    return model_client


def get_openai_model_client():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"), temperature=0
    )
    return model_client


def get_openai_json_model_client():
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0,
        response_format=ResponseFormat({"type": "json_object"}),
    )
    return model_client


def get_logger(name: str) -> Logger:
    log_filename = datetime.now().strftime("%Y%m%d_%H%M%S.log")
    dir_path = os.path.join("fhl_logs", name)
    file_path = os.path.join(dir_path, log_filename)
    os.makedirs(dir_path, exist_ok=True)

    file_handler = FileHandler(file_path)
    formatter = Formatter("%(asctime)s:\n%(message)s\n\n")
    file_handler.setLevel(INFO)
    file_handler.setFormatter(formatter)
    logger = getLogger(name)
    logger.addHandler(file_handler)
    logger.setLevel(INFO)

    return logger
