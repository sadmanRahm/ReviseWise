class ForumModerator:
    def __init__(self):
        self.blocked_words = [
            "kill",
            "suicide",
            "hate crime",
            "bomb",
            "terrorist"
        ]

        self.filtered_words = [
            "stupid",
            "idiot",
            "dumb",
            "hate",
            "loser",
            "trash"
        ]

    def moderate_post(self, content):
        lowered = content.lower()

        for word in self.blocked_words:
            if word in lowered:
                return None, f"Your post was blocked because it contained banned content: '{word}'."

        cleaned = content
        for word in self.filtered_words:
            cleaned = cleaned.replace(word, "***")
            cleaned = cleaned.replace(word.capitalize(), "***")

        return cleaned, None