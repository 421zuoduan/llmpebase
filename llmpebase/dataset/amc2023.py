import os

import glob
from datasets import load_dataset
from collections import defaultdict

from llmpebase.dataset import base
from llmpebase.dataset.data_generic import (
    DatasetMetaCatalog,
    DatasetCatalog,
    BaseQASample,
    BaseQASampleInfo,
    DatasetStatistics,
)

class AMC2023Dataset(base.BaseDataset):

    def create_data_catalog(self):
        # 新增统计维度
        year_info = defaultdict(lambda: defaultdict(int))
        contest_info = defaultdict(lambda: defaultdict(int))
        
        for filepath in glob.glob(f"{category_path}/**/*.json", recursive=True):
            # 解析路径结构 AMC10/2023/algebra/
            path_parts = filepath.split(os.sep)
            contest = path_parts[-3]
            year = path_parts[-2]
            subject = path_parts[-1]

            # 更新统计信息
            year_info[year][contest] += 1
            contest_info[contest][year] += 1

        return AMCDatasetCatalog(
            problem_categories={
                "Year": list(year_info.keys()),
                "Contest": ["AMC10", "AMC12"],
                "Subject": ["algebra", "geometry"]
            },
            data_statistics=AMCStatistics(
                year_distribution=year_info,
                contest_distribution=contest_info
            )
        )

    def get_sample(self, idx: int):
        data = json.load(open(filepath))
        return BaseQASample(
            question=data["problem"],
            answer=data["solution"],
            conclusion=data["answer"],
            auxiliary={
                "year": data["year"],
                "contest": data["contest"],
                "problem_number": data["problem_number"],
                "difficulty": data["difficulty"]
            }
        )

class DataSource(base.DataSource):
    def create_meta_catalog(self):
        return DatasetMetaCatalog(
            dataset_name="AMC2023",
            task_type="Competition Mathematics",
            split_path={
                "train": "AMC2023/train",
                "test": "AMC2023/test"
            }
        )