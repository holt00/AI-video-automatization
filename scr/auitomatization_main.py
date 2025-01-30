import json
from data_structures import Story, Paragraph
from openai import OpenAI
import os
from dotenv import load_dotenv #module to load openai api key from .env file
import requests


load_dotenv()  # geting the api key from .env file
client = OpenAI()

json_schema_for_story = {
  "type": "object",
  "properties": {
    "parrafos": {
      "type": "array",
      "items": {
        "type": "string"
      },
    }
  },
  "required": ["parrafos"],
  "additionalProperties": False
}

def generate_story(story_dictionary, group): #This method generates the story splited by paragraphs. Story is a dictionary with the keys: name, description, completed

    story = Story(group = group ,name = story_dictionary["name"], description = story_dictionary["description"])

    prompt = "Quiero que narres la historia de " + story_dictionary["name"] + ". " + story_dictionary["description"] + "de manera epica y emocionante a la vez que sea adictiva y te mantenga enganchado. La narracion debe durar aproximadamete 3 minutos devuelve la historia separada por parrafos utilizando el esquema json"

    response = client.chat.completions.create(
        # asking GPT-4 to return the 6 most important and interesting mythologies in the world
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Eres un Historiador de mitologias y gran divulgador"},
            {"role": "user", "content": prompt }
        ],
        response_format={"type": "json_schema",
                         "json_schema": {
                             "name": "first_list",
                             "schema": json_schema_for_story
                         }
                         },
    )
    
    response = json.loads(response.choices[0].message.content)["parrafos"]


    for parraph in response:
        print(parraph)
        story.paragraphs.append(Paragraph(parraph))

    store_info_on_json(story.__to_dictionary__(), story.name + ".json", group + "/" + story.name)


    generate_images(story)


def generate_images(story): #This method generates the images for each paragraph of the story

    prompts = __generate_prompt_por_img__(story.name,story.paragraphs, story.group)

    for i in range(len(story.paragraphs)):
        story.paragraphs[i].prompt = prompts[i]
        print(prompts[i])

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompts[i],
            size="1024x1792",
            quality="standard",
            n=1,
        )

        story.paragraphs[i].img_url = response.data[0].url

        img_data = requests.get(story.paragraphs[i].img_url).content

        directory = f'../archivos/{story.group}/{story.name}'
        os.makedirs(directory, exist_ok=True)

        with open(f'../archivos/{story.group}/{story.name}/{story.name}_{i}.png', 'wb') as handler:
            handler.write(img_data)

        story.paragraphs[i].images = f'../archivos/{story.group}/{story.name}/{story.name}_{i}.png'

        store_info_on_json(story.__to_dictionary__(), story.name + ".json", story.group + "/" + story.name)



def __generate_prompt_por_img__(name,paragraphs, group):#This method generates the prompt for each image
    prompt = "por cada uno de estos parrafos quiero que me devuelvas un prompt de generacion de imagen en dall-e 3.0 para imagenes verticales, con un estilo visual realista, mitologico y consistente, sin texto y ocupantdo toda la resulucion. Los parrafos pertenecen al mito de " + name
    prompt +=  "de la mitologia" + group  + ". Incluye en el prompt la mayor informacion posible del parrafo y del contexto de la historia .Devuelve en un json con el campo items un array con los prompts"

    response = client.chat.completions.create(
        # asking GPT-4 to return the 10 most important and interesting stories of each mythology
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Eres un experto en generacion de imagenes con DAll-E 3.0"},
            {"role": "user", "content": prompt},
            {"role": "user", "content": " ".join(str(paragraphs))}
        ],

        response_format={"type": "json_schema",
                         "json_schema": {
                             "name": "list_of_each_group",
                             "schema": {
                              "type": "object",
                              "properties": {
                                "items": {
                                  "type": "array",
                                  "items": {
                                    "type": "string"
                                  }
                                }
                              },
                              "required": ["items"]
                            }

                         }
                         },

    )
    return json.loads(response.choices[0].message.content)["items"]



#TODO create the function that will generate the image audio for each image
def generate_audio(paragraph):
    pass

#TODO create the function that will arrange all the images and audio in a video
def generate_video(story):
    pass

def store_info_on_json(info,filename, directory):


    directory = f'../archivos/{directory}'
    os.makedirs(directory, exist_ok=True)

    with open(directory + "/" +filename, 'w', encoding='utf-8') as file:
        json.dump(info, file, ensure_ascii=False, indent=4)

def load_info_from_json(filename, directory):
    with open(f'../archivos/{directory}/{filename}', 'r', encoding='utf-8') as file:
        return json.load(file)


if __name__ == '__main__':

    with open('../archivos/stories_per_mythology.json', 'r', encoding='utf-8') as file:
        stories = json.load(file)

    for group in stories:
        for story in stories[group]:
            if not story["completed"]:
                try:
                    dictoionary = load_info_from_json(story["name"] + ".json", group)
                except FileNotFoundError:
                    dictoionary = None

                if dictoionary is None or "":
                    generate_story(story, group)
                    story["completed"] = True
                    break
                else:
                    for paragraph in dictoionary["paragraphs"]:
                        if paragraph["images"] is None or "":
                            generate_images(Story.__from_dictionary__(dictoionary))
                            story["completed"] = True
                            break
                    break
        break
#TODO cambiar esto para que se actualice el json
#TODO poner la creacion de audio y la creacionde video

