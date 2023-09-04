from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from app.query.form import RecipeForm
from initial_test import Recipes, check_if_ingredient
from constants import const
import pandas as pd
import os
import requests
from foodbert.food_extractor.food_model import FoodModel
from constants import const

appid = const["appid"]
api_key = const["api_key"]

def get_ingredients(food):
    ingredients = []
    for i in food:
        ingredient_tag = len(i['Ingredient'])
        if ingredient_tag > 0:
            print(ingredient_tag)
            for j, k in enumerate(i['Ingredient']):
                ingredients.append(i['Ingredient'][j]["text"])
    return ingredients

def query_food_api(query, appid, api_key):
    query = str(query)
    r = requests.get(
        'https://api.edamam.com/api/recipes/v2',
        headers={'Accept': 'application/json'},
        params={
            'app_id': appid,
            'app_key': api_key,
            'type': 'any',
            'q': query
        })
    data = r.json()
    return data

def get_recipe_info(data):
    recipes_dict = {}
    total_matches = data["count"]
    for i in range(0, total_matches):
        recipes_dict[data["hits"][0]['recipe']["label"]] = {
            "source":data["hits"][0]['recipe']["source"],
            "url":data["hits"][0]['recipe']["url"],
            "cautions":data["hits"][0]['recipe']["cautions"]
        }
    return recipes_dict


def split(txt, seps):
    # https://stackoverflow.com/questions/4697006/python-split-string-by-list-of-separators
    default_sep = seps[0]

    # we skip seps[0] because that's the default separator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]