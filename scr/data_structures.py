
class Story:
    def __init__(self, group,name, description):
        self.group = group
        self.name = name
        self.description = description
        self.paragraphs = []


    def __str__ (self):
        string = "De"+ str(self.group) + "\n" + str(self.name) + ": " + str(self.description) + "\n" + "\n"
        for paragraph in self.paragraphs:
            string += str(paragraph) + "\n"
        return string

    def __to_dictionary__(self): #This function will return a dictionary with the story information
        dict = {
            "group": self.group,
            "name": self.name,
            "description": self.description,
            "paragraphs": []
        }
        for paragraph in self.paragraphs: #As paragraphs is a list of objects, we need to convert each object to a dictionary before appending it to the list
            dict["paragraphs"].append(paragraph.__to_dictionary__())

        return dict

    @staticmethod
    def __from_dictionary__( dictionary): #This function will return a story object from a dictionary
        group = dictionary["group"]
        name = dictionary["name"]
        description = dictionary["description"]
        paragraphs = []
        for paragraph in dictionary["paragraphs"]: #As paragraphs is a list of dictionaries, we need to convert each dictionary to an object before appending it to the list
            paragraphs.append(Paragraph.__from_dictionary__(paragraph))
        story = Story(name, description)
        story.paragraphs = paragraphs
        return story

class Paragraph:
    def __init__(self, text):
        self.text = text
        self.images = None
        self.prompt = None
        self.audio = None

    def __str__ (self):
        return str(self.text)

    def __to_dictionary__(self): #This function will return a dictionary with the paragraph information
        return {
            "text": self.text,
            "images": self.images,
            "prompt": self.prompt,
            "audio": self.audio
        }

    @staticmethod
    def __from_dictionary__(dictionary): #This function will return a paragraph object from a dictionary
        text = dictionary["text"]
        images = dictionary["images"]
        prompt = dictionary["prompt"]
        audio = dictionary["audio"]
        paragraph = Paragraph(text)
        paragraph.images = images
        paragraph.prompt = prompt
        paragraph.audio = audio
        return paragraph