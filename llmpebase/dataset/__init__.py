"""
An interface of datasets
"""
import logging

from llmpebase.dataset.gsm8k import DataSource as gsm8k_datasource
from llmpebase.dataset.mmlu import DataSource as mmlu_datasource
from llmpebase.dataset.game24 import DataSource as game24_datasource
from llmpebase.dataset.math import DataSource as math_datasource
from llmpebase.dataset.bbh import DataSource as bbh_datasource
from llmpebase.dataset.theoremqa import DataSource as theoremqa_datasource
from llmpebase.dataset.csqa import DataSource as csqa_datasource
from llmpebase.dataset.aqua import DataSource as aqua_datasource
from llmpebase.dataset.svamp import DataSource as svamp_datasource
# from llmpebase.dataset.aime2024 import DataSource as aime2024_datasource
# from llmpebase.dataset.amc2023 import DataSource as amc2023_datasource
# from llmpebase.dataset.gaokao_mathqa import DataSource as gaokao_mathqa_datasource
from llmpebase.dataset.math500 import DataSource as math500_datasource

datasources = {
    "GSM8K": gsm8k_datasource,
    "MMLU": mmlu_datasource,
    "GameOf24": game24_datasource,
    "MATH": math_datasource,
    "BBH": bbh_datasource,
    "TheoremQA": theoremqa_datasource,
    "CSQA": csqa_datasource,
    "AQUA": aqua_datasource,
    "SVAMP": svamp_datasource,
    # "AIME2024": aime2024_datasource,
    # "AMC2023": amc2023_datasource,
    # "gaokao-mathqa": gaokao_mathqa_datasource,
    "MATH-500": math500_datasource
}


def define_dataset(data_config):
    """Define the datasets based on the config file."""
    data_name = data_config["data_name"]
    logging.info("Define the dataset %s", data_name)
    return datasources[data_name]()
