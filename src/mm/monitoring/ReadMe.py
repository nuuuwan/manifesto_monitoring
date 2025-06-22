from functools import cached_property

from utils import File, Log

from mm.cabinet_decisions import CabinetDecision
from mm.manifesto import NPPManifestoPDF
from mm.monitoring.charts.HeatMap import HeatMap
from mm.monitoring.CompareManifesto import CompareManifesto
from mm.monitoring.ReadMeCompare import ReadMeCompare
from mm.monitoring.ReadMeHeader import ReadMeHeader

log = Log("ReadMe")


class ReadMe(ReadMeHeader, ReadMeCompare):
    README_PATH = "README.md"
    SOURCE_URL = "https://www.npp.lk/up/policies/en/npppolicystatement.pdf"

    def __init__(self):
        self.compare_manifesto = CompareManifesto()
        self.data_list = self.compare_manifesto.similarity_data_list
        self.manifesto_idx = NPPManifestoPDF().get_manifesto().all_idx
        self.manifesto_to_datalist = {
            x["manifesto_key"]: x for x in self.data_list
        }
        self.cabinet_decision_idx = CabinetDecision.idx()

    @cached_property
    def heatmap_lines(self):
        HeatMap().draw()
        return [
            f"![{HeatMap.CHART_PATH}]({HeatMap.CHART_PATH})",
            "",
        ]

    @cached_property
    def lines(self):
        return self.header_lines + self.heatmap_lines + self.compare_lines

    def build(self):
        File(self.README_PATH).write_lines(self.lines)
        log.info(f"Wrote {self.README_PATH} ({len(self.lines)} lines)")
