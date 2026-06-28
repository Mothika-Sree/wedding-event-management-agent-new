class Parser:

    @staticmethod
    def clean_lines(text):

        return [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]