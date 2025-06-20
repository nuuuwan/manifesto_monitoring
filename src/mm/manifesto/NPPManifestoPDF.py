from mm.manifesto.NPPManifesto import NPPManifesto
from mm.manifesto.NPPManifestoPDFBase import NPPManifestoPDFBase
from mm.manifesto.NPPManifestoPDFContents import NPPManifestoPDFContents
from mm.manifesto.NPPManifestoPDFDetails import NPPManifestoPDFDetails


class NPPManifestoPDF(
    NPPManifestoPDFBase, NPPManifestoPDFContents, NPPManifestoPDFDetails
):
    def get_manifesto(self) -> NPPManifesto:
        return NPPManifesto(
            l1_topics=self.l1_topics,
        )
