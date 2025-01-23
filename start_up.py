#Importing all the necessary libraries and modules
from openai import OpenAI #OpenAI api client
import os
from dotenv import load_dotenv #module to load openai api key from .env file
import json


def generate_initial_list (): #Function that will generate a Json containing what was requested in the first place
    load_dotenv()  # geting the api key from .env file
    client = OpenAI()

    prompt = "Devuelve un json con las 6 mitologias mas importantes e interesantes del mundo" #prompt to be used for the completion

    response = client.chat.completions.create(
        model= "gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Eres un hostoriador de mitologias"},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_schema",
                         "json_schema": {
                             "name": "first_list",
                             "schema": {
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
                         }
                         },
    )
    return json.loads(response.choices[0].message.content) #printing the response from the api (the 6 most important and interesting mythologies in the world

def generate_story_list (list, story_num): #Function that will list n most important sorties of each mythology
    load_dotenv()  # geting the api key from .env file
    client = OpenAI()

    #for mytology in list:
    mytology = list["items"][0]["name"]
    prompt = f"Devuelve en un json los nombre y una pequeña descripcion de los {story_num} mitos mas importantes de la {mytology}"
    response = client.chat.completions.create(
        model= "gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Eres un hostoriador de mitologias"},
            {"role": "user", "content": prompt}
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
                         }
                         },

    )
    return json.loads(response.choices[0].message.content) #printing the response from the api (the 6 most important and interesting mythologies in the world


if __name__ == "__main__":
    story_num = 10
    initial_list = generate_initial_list()
    list_per_group = generate_story_list(initial_list, story_num)
    for m in list_per_group["items"]:
        print(m["name"])
        print(m["description"])
        print("\n")

