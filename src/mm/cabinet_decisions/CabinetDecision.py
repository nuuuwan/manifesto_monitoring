import time
from dataclasses import dataclass
from functools import cache, cached_property

from utils import WWW, Log, Time, TimeFormat, TimeUnit, TSVFile

log = Log("CabinetDecision")


@dataclass
class CabinetDecision:
    # ⚠️ WARNING: Does not use the same format as CabinetDecision (AbstractDoc)
    # Format "translated" in list_all.
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
    REMOTE_DATA_URL = (
        "https://raw.githubusercontent.com"
        + "/nuuuwan/lk_cabinet_decisions"
        + "/refs/heads/data"
        + "/data/lk_cabinet_decisions/docs_all.tsv"
    )
    LIMIT_DAYS = 28

    @cached_property
    def key(self):
        return f"{self.date_str}-{self.decision_num:03d}"

    @cached_property
    def is_new(self):

        limit_date_str = TimeFormat.DATE.format(
            Time(
                Time.now().ut
                - TimeUnit.SECONDS_IN.DAY * CabinetDecision.LIMIT_DAYS
            )
        )
        return self.date_str >= limit_date_str

    @cached_property
    def key_with_emoji(self):
        emoji = "🆕" if self.is_new else ""
        return f"{emoji} {self.key}"

    @staticmethod
    def __download_data__():
        www = WWW(CabinetDecision.REMOTE_DATA_URL)
        t_wait = 10
        while t_wait < 120:
            try:
                tmp_tsv_path = www.download()
                return tmp_tsv_path
            except Exception as e:
                log.error(f"Failed to download data: {e}")
                log.debug(f"Retrying in {t_wait} seconds...")
                time.sleep(t_wait)
                t_wait *= 2
        raise RuntimeError("Failed to download data after multiple attempts.")

    @staticmethod
    def __get_data_list__():
        tmp_tsv_path = CabinetDecision.__download_data__()
        tsv_file = TSVFile(tmp_tsv_path)
        data_list = tsv_file.read()
        data_list = [data for data in data_list if data.get("date_str")]
        log.info(
            f"Loaded {len(data_list)}"
            + f" cabinet decisions from {CabinetDecision.REMOTE_DATA_URL}"
        )
        return data_list

    @staticmethod
    @cache
    def list_all():
        return [
            CabinetDecision(
                date_str=data["date_str"],
                decision_num=int(data["num"]),
                title=data["description"],
                source_url=data["url_metadata"],
                decision_details=data["decision_details_body"],
            )
            for data in CabinetDecision.__get_data_list__()
        ]

    @staticmethod
    def idx():
        return {
            decision.key: decision for decision in CabinetDecision.list_all()
        }
