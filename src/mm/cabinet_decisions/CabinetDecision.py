from dataclasses import dataclass
from functools import cache, cached_property

from utils import WWW, Log, TSVFile

log = Log("CabinetDecision")


@dataclass
class CabinetDecision:
    date_str: str
    decision_num: int
    title: str
    source_url: str
    decision_details: str

    REMOTE_DATA_URL = (
        "https://raw.githubusercontent.com"
        + "/nuuuwan/lk_cabinet_decisions"
        + "/refs/heads/main/data/cabinet_decisions.tsv"
    )

    @cached_property
    def key(self):
        return f"{self.date_str}-{self.decision_num:03d}"

    @staticmethod
    @cache
    def __get_data_list__():
        www = WWW(CabinetDecision.REMOTE_DATA_URL)
        tsv_file = TSVFile(www.download())
        data_list = tsv_file.read()
        print(data_list[0])
        data_list = [data for data in data_list if data.get("date_str")]
        log.info(f"Loaded {len(data_list)} cabinet decisions from {www.url}")
        return data_list

    @staticmethod
    @cache
    def list_all():
        return [
            CabinetDecision(
                date_str=data["date_str"],
                decision_num=int(data["decision_num"]),
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
