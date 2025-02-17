#Importing all the necessary libraries and modules
from openai import OpenAI #OpenAI api client
import os
from dotenv import load_dotenv #module to load openai api key from .env file
import json


def generate_initial_list (prompt, json_schema): #Function that will generate a Json containing what was requested in the first place
    load_dotenv()  # geting the api key from .env file
    client = OpenAI()

    response = client.chat.completions.create( #asking GPT-4 to return the 6 most important and interesting mythologies in the world
        model= "gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Eres un hostoriador de mitologias"},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_schema",
                         "json_schema": {
                             "name": "first_list",
                             "schema": json_schema
                         }
                         },
    )
    return json.loads(response.choices[0].message.content)["items"] #printing the response from the api (the 6 most important and interesting mythologies in the world

def generate_story_list (list, story_num, json_schema, list_generating_prompt): #Function that will list n most important sorties of each mythology
    load_dotenv()  # geting the api key from .env file
    general_story_list = {}
    client = OpenAI()
    for group in list: #for each mithology in the list we will ask the api to return the n most important stories
        #TODO change if you want another kind of story

        prompt = "utilizando unicamente caracteres que json acepte" + list_generating_prompt + f"las {story_num} historias mas importantes e interesantes de la {group["name"]}"

        prompt = f"Devuelve en un json los nombre y una pequeña descripcion de las {story_num} historias mas interesantes, importantes y virales de la {group["name"]}, , utilizando solo caracteres que json acepte"
        response = client.chat.completions.create( #asking GPT-4 to return the 10 most important and interesting stories of each mythology
            model= "gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Eres un hostoriador de mitologias"},
                {"role": "user", "content": prompt}
            ],

            response_format={"type": "json_schema",
                             "json_schema": {
                                 "name": "list_of_each_group",
                                 "schema": json_schema
                             }
                             },

        )
        general_story_list[group["name"]] = json.loads(response.choices[0].message.content)["items"]

    return general_story_list #printing the response from the api (the 6 most important and interesting mythologies in the world


if __name__ == "__main__":

    json_schema = {
     "type": "object",
     "properties": {
         "items": {
             "type": "array",
             "items": {
                 "type": "object",
                 "properties": {
                     "name": {
                         "type": "string",
                         "description": "El nombre del elemento"
                     },
                     "description": {
                         "type": "string",
                         "description": "La descripción del elemento"
                     }
                 },
                 "required": ["name", "description"],
                 "additionalProperties": False
             }
         }
     },
     "required": ["items"],
     "additionalProperties": False
    }

    story_num = 10
    group_generating_prompt = "Devuelve un json con las 6 mitologias mas importantes e interesantes del mundo, utilizando solo caracteres que json acepte" #prompt used to generate the initial list of groups
    list_generating_prompt = f"Devuelve una el nombre y una pequeña descripcion de : " #prompt used to generate the list of stories of each group

    initial_list = generate_initial_list(group_generating_prompt, json_schema) #we generate the initial groups
    list_per_group = generate_story_list(initial_list, story_num, json_schema, list_generating_prompt) #we generate the list of stories of each group


    with open("archivos/stories_per_mythology.json", "w", encoding="utf-8") as file:
        json.dump(list_per_group, file,ensure_ascii=False, indent=4)

