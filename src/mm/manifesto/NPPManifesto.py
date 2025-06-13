from mm.manifesto.NPPManifestoBase import NPPManifestoBase
from mm.manifesto.NPPManifestoParser import NPPManifestoParser
from mm.manifesto.NPPManifestoParserContents import NPPManifestoParserContents
from mm.manifesto.NPPManifestoParserDetails import NPPManifestoParserDetails


class NPPManifesto(
    NPPManifestoBase,
    NPPManifestoParser,
    NPPManifestoParserContents,
    NPPManifestoParserDetails,
):
    pass
