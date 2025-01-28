class Story:
    def __init__(self, name, description):
        self.name = None
        self.description = None
        self.paragraphs = []


class Paragraph:
    def __init__(self, text):
        self.text = None
        self.images = []
        self.audio = None
