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
        max_entries=50
    )


app = Flask(__name__)
app.config.from_object(config['dev'])

image_app = ClarifaiApp(api_key=config['dev'].API_KEY)
try:
    model = image_app.models.get(model_id="bd367be194cf45149e75f01d59f77ba7")
except Exception as e:
    print(str(e))


def validate_upload(rfiles):
    if 'image' not in rfiles:
        return 'No image part'
    image = rfiles['image']
    #print(image.filename)
    if not image or image.filename == '':
        return 'Please select an image'
    elif '.' not in image.filename:
        return 'Invalid file'
    elif image.filename.rsplit('.', 1)[1].lower() not in config['dev'].ALLOWED_EXTENSIONS:
        return 'Please select allowed image types: png, jpg, jpeg'
    return 'upload validated'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if request.method == 'POST':
        ingredients = []
        if form.validate_on_submit():
            for ing in form.ingredients.data:
                if ing['ingredient'] and ing['ingredient'] != '':
                    ingredients.append(ing['ingredient'])
        if not ingredients:
            flash('Enter at least one ingredient')
            return redirect(url_for('index'))
        recipes = RecipeModel().get_recipes(ingredients)
        if not recipes:
            flash('No matching recipes exist. Please try again.')
            flash('Hint: Did you enter valid ingredients?')
            return redirect(request.url)
        return render_template('recipes.html', recipes=recipes)
    return render_template('index.html', form=form)


@app.route('/upload-image', methods=['GET', 'POST'])
def upload_image():
    form = MainForm()
    if request.method == "POST":
        if request.files:
            message = validate_upload(request.files)
            if message == 'upload validated':
                image = request.files["image"].read()
                response = model.predict_by_bytes(image)
                ingredients = [x['name'] for x in response['outputs'][0]['data']['concepts']]
                #print(ingredients)
                for ing in ingredients:
                    if ing:
                        ing_form = IngForm()
                        ing_form.ingredient = ing
                        form.ingredients.append_entry(ing_form)
                return render_template('index.html',form=form)
            else:
                flash(message)
                return redirect(request.url)
    return render_template('index.html',form=form)


if __name__ == '__main__':
    app.run(debug=True)
