import os
import re
from functools import cached_property

from PyPDF2 import PdfReader


class NPPManifestoPDFBase:
    REMOTE_URL = "https://www.npp.lk/up/policies/en/npppolicystatement.pdf"
    LOCAL_PATH = os.path.join("data", "manifestos", "npp_manifesto.pdf")

    @cached_property
    def raw_text(self):
        reader = PdfReader(self.LOCAL_PATH)
        raw_text = ""
        for page in reader.pages:
            raw_text += page.extract_text() + "\n"

        raw_text = raw_text.strip()
        while '\n\n\n' in raw_text:
            raw_text = raw_text.replace('\n\n\n', '\n\n')
        return raw_text

    @cached_property
    def lines(self):
        lines = self.raw_text.split("\n")
        lines = [re.sub(r"\s+", " ", line).strip() for line in lines]
        return lines

    