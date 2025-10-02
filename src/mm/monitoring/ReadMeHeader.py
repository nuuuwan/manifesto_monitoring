from functools import cached_property

from mm.monitoring.charts.ProgressChart import ProgressChart


class ReadMeHeader:
    @cached_property
    def progress_chart_lines(self):
        ProgressChart().draw()
        return [
            f"![{ProgressChart.CHART_PATH}]({ProgressChart.CHART_PATH})",
            "",
        ]

    @cached_property
    def header_lines(self):
        return (
            [
                "# 🇱🇰 Manifesto Monitoring",
                "",
                "This repository contains utility libraries & tools for"
                " tracking, analyzing, & visualizing the implementation of the"
                " 2024 NPP manifesto — now the **de facto policy framework**"
                " of the 🇱🇰 Sri Lankan Government (2025).",
                "",
            ]
            + self.progress_chart_lines
            + [
                "🛠️ Built for researchers, developers, journalists, & citizens"
                " who want **accountability & transparency** in governance.",
                "",
                "📢 Public Data. Share. Fork. Contribute.",
                "",
            ]
        )
