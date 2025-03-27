import os

import glob
from datasets import load_dataset

from llmpebase.dataset import base
from llmpebase.dataset.data_generic import (
    DatasetMetaCatalog,
    DatasetCatalog,
    BaseQASample,
    BaseQASampleInfo,
    DatasetStatistics,
)


class AIMEDatasetCatalog(MATHDatasetCatalog):
    __annotations__ = {
        "version_dist": dict[str, int],
        "scoring_stats": dict[str, int]
    }

class AIME2024Dataset(base.BaseDataset):
    def create_data_catalog(self):
        # 新增统计维度
        version_dist = defaultdict(int)
        scoring_stats = defaultdict(int)
        
        for filepath in glob.glob(f"{category_path}/**/*.json", recursive=True):
            with open(filepath) as f:
                data = json.load(f)
                
            # 版本分布统计
            version_dist[data["version"]] += 1
            
            # 评分类型统计
            scoring_stats[data["scoring_type"]] += 1

        return AIMEDatasetCatalog(
            problem_categories={
                "Version": ["I", "II"],
                "ScoringType": ["standard", "manual-grading"],
                "Subject": ["algebra", "geometry", "number_theory"]
            },
            data_statistics=AMCStatistics(
                version_dist=dict(version_dist),
                scoring_stats=dict(scoring_stats),
                ...
            )
        )

    def get_sample(self, idx: int):
        data = json.load(open(filepath))
        
        # 答案标准化处理
        answer = data["answer"].lstrip('0') or '0'  # 处理前导零
        
        return BaseQASample(
            question=data["problem"],
            answer=data["solution"],
            conclusion=answer,
            auxiliary={
                "version": data["version"],
                "scoring_type": data["scoring_type"],
                "is_final_problem": (data["problem_number"] == 15)
            }
        )