from flask import Flask, render_template, request, flash,redirect, url_for
from config import config
from models import RecipeModel
from clarifai.rest import ClarifaiApp
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, StringField
from wtforms.validators import Length


class IngForm(Form):
    ingredient = StringField('Ingredient', validators=[Length(max=30, message="Length of text exceeds 30 characters")],
                             render_kw={"placeholder": "Enter ingredient", "class":"col-sm-3 my-1"})


class MainForm(FlaskForm):
    ingredients = FieldList(
        FormField(IngForm),
        min_entries=1,
        max_entries=100
    )


app = Flask(__name__)
app.config.from_object(config['dev'])

print(config['dev'].API_KEY)
image_app = ClarifaiApp(api_key=config['dev'].API_KEY)
model = image_app.models.get(model_id="bd367be194cf45149e75f01d59f77ba7")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if request.method == 'POST':
        ingredients = []
        if form.validate_on_submit():
            print(form.ingredients.data)
            for ing in form.ingredients.data:
                if ing['ingredient'] and ing['ingredient'] != '':
                    ingredients.append(ing['ingredient'])
        print(ingredients)
        if not ingredients:
            flash('Enter atleast one ingredient')
            return redirect(url_for('index'))
        recipes = RecipeModel().get_recipes(ingredients)
        if not recipes:
            flash('No matching recipes exist')
            return render_template('recipes.html')
        return render_template('recipes.html', recipes=recipes)
    return render_template('index.html', form=form)


@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"].read()
            print(image, type(image))
            response = model.predict_by_bytes(image)
            print(response)
            ingredients = [x['name'] for x in response['outputs'][0]['data']['concepts']]
            print(ingredients)
            form = MainForm()
            for ing in ingredients:
                print(ing)
                if ing:
                    ing_form = IngForm()
                    ing_form.ingredient  = ing
                #print(ing_form.ingredient.data)
                    form.ingredients.append_entry(ing_form)
                print(form.ingredients.data)
            #recipes = RecipeModel().get_recipes(ingredients)
            #return render_template('recipes.html', recipes=recipes)
            return render_template('index.html',form=form)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
