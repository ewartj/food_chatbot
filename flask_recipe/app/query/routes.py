from app.query import bp

from flask import render_template, redirect, url_for
from constants import const
import pandas as pd
from foodbert.food_extractor.food_model import FoodModel
from constants import const
from app.query.form import RecipeForm
from app.query.functions import (get_ingredients, query_food_api)
model = FoodModel("chambliss/distilbert-for-food-extraction")

appid = const["appid"]
api_key = const["api_key"]

@bp.route("/recipe", methods=['GET', 'POST'])
def recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        data = str(form.query.data)
        ingrediants = model.extract_foods(data)
        ingredients_identified = get_ingredients(ingrediants)
        data = query_food_api(ingredients_identified, appid, api_key)
        df = pd.json_normalize(data["hits"], max_level=2)
        try:
            output_data = df[["recipe.label","recipe.source","recipe.url","recipe.cautions",
            "recipe.ingredientLines","recipe.cuisineType",
            "recipe.mealType","recipe.dishType"]]
            output_data.rename(columns=lambda x: x.replace("recipe.",""), inplace=True)
            output_data.reset_index(inplace=True)
            output_data.to_csv("db.csv")
            return redirect(url_for('query.result'))
        except:
             return redirect(url_for('query.none'))
    return render_template('recipe.html', form=form)

@bp.route("/result", methods=['GET', 'POST'])
def result():
    return render_template("result.html", result=result)

@bp.route("/none", methods=['GET', 'POST'])
def none():
    return render_template("none.html")

@bp.route("/result_db", methods=['GET', 'POST'])
def result_db():
    output_data = pd.read_csv("db.csv")
    output_json = output_data.to_json(orient='table',index=False)
    return output_json