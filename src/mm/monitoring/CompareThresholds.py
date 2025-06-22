class CompareThresholds:
    THRESHOLDS = {
        "high": 0.6,
        "medium": 0.55,
        "low": 0.5,
        "nil": 0.0,
    }

    EMOJIS = {
        "high": "🔴",
        "medium": "🟠",
        "low": "🟡",
        "nil": "⚪️",
    }

    COLORS = {
        "high": "#f00",
        "medium": "#f80",
        "low": "#ff0",
        "nil": "#fff2",
    }

    TEXTUAL = {
        "high": "Strongly Aligned",
        "medium": "Moderately Aligned",
        "low": "Weakly Aligned",
        "nil": "No Significant Alignment",
    }

    @staticmethod
    def get_group_title(group):
        return f"{CompareThresholds.EMOJIS[group]} {group.capitalize()}"

    @staticmethod
    def get_group(similarity):
        for group, threshold in CompareThresholds.THRESHOLDS.items():
            if similarity >= threshold:
                return group
        return "nil"

    @staticmethod
    def get_similarity_markdown(similarity):
        group = CompareThresholds.get_group(similarity)
        emoji = CompareThresholds.EMOJIS[group]
        return f"{emoji} {similarity:.0%}"
