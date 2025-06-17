import os
from dataclasses import dataclass
from functools import cached_property

from utils import JSONFile, Log

log = Log("CabinetDecision")


@dataclass
class CabinetDecision:
    date_str: str
    decision_num: int
    title: str
    source_url: str
    decision_details: str

    DIR_PY = os.environ["DIR_PY"]
    DIR_DATA = os.path.join(DIR_PY, "lk_cabinet_decisions", "data")
    DIR_CABINET_DECISIONS = os.path.join(DIR_DATA, "cabinet_decisions")
    CABINET_DESICIONS_TABLE_PATH = os.path.join(
        DIR_DATA, "cabinet_decisions.tsv"
    )

    @cached_property
    def key(self):
        return f"{self.date_str}-{self.decision_num:03d}"

    @staticmethod
    def __get_data_file_path_list__():
        data_file_path_list = []
        for root, _, files in os.walk(CabinetDecision.DIR_CABINET_DECISIONS):
            for file_name in files:
                if file_name.endswith(".json"):
                    file_path = os.path.join(root, file_name)
                    data_file_path_list.append(file_path)
        return data_file_path_list

    @staticmethod
    def __get_data_list__():
        data_list = []
        for file_path in CabinetDecision.__get_data_file_path_list__():
            data = JSONFile(file_path).read()
            data_list.append(data)
        data_list.sort(key=lambda x: x["key"], reverse=True)
        return data_list

    @staticmethod
    def list_all():
        return [
            CabinetDecision(
                date_str=data["date_str"],
                decision_num=data["decision_num"],
                title=data["title"],
                source_url=data["source_url"],
                decision_details=data["decision_details"],
            )
            for data in CabinetDecision.__get_data_list__()
        ]

    @staticmethod
    def idx():
        return {
            decision.key: decision for decision in CabinetDecision.list_all()
        }
