# RecipeGenie
Get recipes from available ingredients.

A web application to get recipes from available ingredients at home. User can either enter ingredients manually or upload an image. 

While entering manually, ingredients can be added or removed.

On uploading an image the ingredients from the image and related terms are populated on the form. User can add or remove ingredients.

After selecting the ingredients and clicking on 'Get Recipes', a list of recipes that can be prepared with the ingredients are displayed.

This web application is built using Flask, jQuery, Boot Strap and connects to MongoDB hosted on Azure. Clarifai API is used for ingredient recognition.

A typical user story for a user interacting with the web app would look something like:
* Users should be able to submit an image or manually enter the ingredients.
* Users should be provided a list of expected ingredients based on the image if an image is provided by the user.
* Users should be able to modify the list of ingredients manually by adding or removing ingredients from the list.
* Users should recieve recipes based on their final ingredient list.

