from functools import cached_property


class ReadMeHeader:
    @cached_property
    def header_lines(self):
        return [
            "# 🇱🇰 Manifesto Monitoring",
            "",
            "This repository contains utility libraries & tools for"
            " tracking, analyzing, & visualizing the implementation of the"
            " 2024 NPP manifesto — now the **de facto policy framework**"
            " of the 🇱🇰 Sri Lankan Government (2025).",
            "",
            "🛠️ Built for researchers, developers, journalists, & citizens"
            " who want **accountability & transparency** in governance.",
            "",
            "🔍 Use this repo to:",
            "",
            "- Track progress on key promises",
            "- Analyze policy implementation",
            "- Build visual dashboards & reports",
            "",
            "📢 Public Data. Share. Fork. Contribute.",
        ]
