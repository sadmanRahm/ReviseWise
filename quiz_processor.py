class QuizProcessor:
    def __init__(self, responses):
        self.responses = responses

    def calculate_style(self):
        normalise = {
            "visual": "Visual",
            "vis": "Visual",
            "auditory": "Auditory",
            "audio": "Auditory",
            "read/write": "Read/Write",
            "readwrite": "Read/Write",
            "rw": "Read/Write",
            "kinaesthetic": "Kinaesthetic",
            "kinesthetic": "Kinaesthetic",
            "k": "Kinaesthetic"
        }

        scores = {"Visual": 0, "Auditory": 0, "Read/Write": 0, "Kinaesthetic": 0}

        for ans in self.responses:
            key = ans.strip().lower()
            if key in normalise:
                scores[normalise[key]] += 1

        total_answers = scores["Visual"] + scores["Auditory"] + scores["Read/Write"] + scores["Kinaesthetic"]
        if total_answers == 0:
            return "Visual"

        return max(scores, key=scores.get)