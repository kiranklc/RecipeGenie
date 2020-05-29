from flask import Flask, flash, render_template, request, redirect, url_for
from config import config
from models import RecipeModel


app = Flask(__name__)
app.config.from_object(config['prod'])


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        ingredients = []
        if request.form['ing1']:
            ingredients.append(request.form['ing1'])
        if request.form['ing2']:
            ingredients.append(request.form['ing2'])
        if request.form['ing3']:
            ingredients.append(request.form['ing3'])
        if request.form['ing4']:
            ingredients.append(request.form['ing4'])
        if request.form['ing5']:
            ingredients.append(request.form['ing5'])
        if request.form['ing6']:
            ingredients.append(request.form['ing6'])
        print(ingredients)
        recipes = RecipeModel().get_recipes(ingredients)
        return render_template('recipes.html', recipes=recipes)

    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True)
