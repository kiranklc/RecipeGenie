from flask import Flask, flash, render_template, request, redirect, url_for
from config import config
from models import RecipeModel
import base64
from clarifai.rest import ClarifaiApp


app = Flask(__name__)
app.config.from_object(config['dev'])

print(config['dev'].API_KEY)
image_app = ClarifaiApp(api_key=config['dev'].API_KEY)
model = image_app.models.get(model_id="bd367be194cf45149e75f01d59f77ba7")


@app.route('/', methods=['GET', 'POST'])
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


@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        tags = []
        if request.files:
            image = request.files["image"].read()
            print(image, type(image))
            response = model.predict_by_bytes(image)
            print(response)
            ingredients = [x['name'] for x in response['outputs'][0]['data']['concepts']]
            print(ingredients)
            recipes = RecipeModel().get_recipes(ingredients)
            return render_template('recipes.html', recipes=recipes)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
