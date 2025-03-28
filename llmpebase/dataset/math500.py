""" 
The datasource inference for the MATH dataset.
The detailed information of it is shown in 
https://people.eecs.berkeley.edu/~hendrycks/MATH.tar
"""

import os
import json
import glob
from collections import defaultdict

from llmpebase.dataset import base
from llmpebase.dataset.data_generic import (
    DatasetMetaCatalog,
    MATHDatasetCatalog,
    BaseQASample,
    BaseQASampleInfo,
    MATHDatasetStatistics,
)
from llmpebase.utils import tools


class AddableDict(dict):
    """A dict to merge two dicts by adding the values of the same key."""

    def update(self, other):
        for key, value in other.items():
            if key in self:
                self[key] += value
            else:
                self[key] = value


def count_category(category_path: str) -> tuple:
    """Count the data information in the category."""
    category_levels = defaultdict(int)
    collect_items = []
    qa_files = glob.glob(f"{category_path}/*.json")
    category_name = ""
    for filepath in qa_files:
        file_id = os.path.basename(filepath).split(".json")[0]

        # Load the data file
        with open(filepath, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            category_name = tools.format_term(data["type"])
            level = data["level"]

        collect_items.append(
            BaseQASampleInfo(
                sample_id=file_id,
                sample_field="Math",
                sample_problem=category_name,
                sample_dataset="MATH",
                sample_filepath=filepath,
            )
        )

        category_levels[level] += 1

    return category_name, category_levels, collect_items


class MATH500Dataset(base.BaseDataset):
    """
    An interface for the MATH dataset.
    """

    def __init__(self, data_meta_catalog: DatasetMetaCatalog, phase: str):
        super().__init__(data_meta_catalog, phase)

        self.customize_data_catalog = MATHDatasetCatalog

    def create_data_catalog(self):
        # Collect all category folders of the MATH dataset
        folders = [
            folder
            for folder in glob.glob(os.path.join(self.phase_data_path, "*"))
            if os.path.isdir(folder)
        ]
        # Visit each category folder to get data information
        category_info = defaultdict(dict)
        category_samples = defaultdict(list)
        difficulty_count = AddableDict()
        collect_items = []
        for category_path in folders:
            # Get the info of the category
            category_name, category_levels, items = count_category(category_path)
            # Update the category info to the category_info
            category_info[category_name]["num_samples"] = len(items)
            category_info[category_name].update(category_levels)
            difficulty_count.update(category_levels)
            collect_items.extend(items)
            current_idx = len(collect_items)
            # Add sample indexes to the category_samples
            category_samples[category_name].extend(
                range(current_idx - len(items), current_idx)
            )

        return MATHDatasetCatalog(
            data_phase=self.phase,
            data_samples=collect_items,
            category_samples=category_samples,
            problem_fields=["Math"],
            problem_categories={"Math": list(category_info.keys())},
            data_statistics=MATHDatasetStatistics(
                num_samples=len(collect_items),
                category_info={"Math": category_info},
                difficulty_count=difficulty_count,
            ),
        )

    def get_sample(self, idx: int):
        """Get one sample from the file."""
        sample_info = self.data_catalog.data_samples[idx]

        sample_filepath = sample_info["sample_filepath"]

        with open(sample_filepath, "r", encoding="utf-8") as json_file:
            # Load the JSON data from the file
            data = json.load(json_file)

        answer = data["solution"].rstrip()

        answer, conclusion, groundtruth = self.gt_extractor.forward(answer)

        return BaseQASample(
            question=data["problem"],
            answer=answer,
            conclusion=conclusion,
            groundtruth=groundtruth,
            auxiliary={
                "level": data["level"],
                "category": data["type"],
                "sample_info": sample_info,
            },
        )


class DataSource(base.DataSource):
    """The MATH datasource."""

    def __init__(self):
        super().__init__()

        self.base_dataset = MATH500Dataset

    def create_meta_catalog(self):
        """Configure the dataset."""
        return DatasetMetaCatalog(
            dataset_name="MATH-500",
            task_type="Mathematical Reasoning",
            dataset_path=self.data_path,
            split_path={
                "train": os.path.join(self.data_path, "MATH-500/train"),
                "test": os.path.join(self.data_path, "MATH-500/test"),
                "validation": os.path.join(self.data_path, "MATH-500/test"),
            },
        )
