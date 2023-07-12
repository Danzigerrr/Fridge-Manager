import json

from django.shortcuts import get_object_or_404, render, redirect
from ..models import Recipe, Product, Fridge
from ..api_key import api_key_value
from django.core.paginator import Paginator
from django.contrib import messages
import requests
from django.db.models import Count


def get_recipes(products_names):
    base_url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {'apiKey': api_key_value,
              'number_of_recipes': 1,
              'ingredients': str(products_names)
              }

    # response = requests.get(base_url, params=params)
    # return response.content

    # debugging
    json_data = """[{"id":641110,"title":"Curry and Sage Roast Chicken","image":"https://spoonacular.com/recipeImages/641110-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":6,"missedIngredients":[{"id":99226,"amount":1.0,"unit":"small bunch","unitLong":"small bunch","unitShort":"small bunch","aisle":"Produce","name":"sage","original":"small bunch of fresh sage – chopped","originalName":"fresh sage – chopped","meta":["fresh","chopped"],"extendedName":"fresh sage","image":"https://spoonacular.com/cdn/ingredients_100x100/fresh-sage.png"},{"id":11215,"amount":3.0,"unit":"cloves","unitLong":"cloves","unitShort":"cloves","aisle":"Produce","name":"garlic - &","original":"3 cloves garlic – crushed & chopped","originalName":"garlic – crushed & chopped","meta":["crushed","chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/garlic.png"},{"id":19296,"amount":3.0,"unit":"tablespoons","unitLong":"tablespoons","unitShort":"Tbsp","aisle":"Nut butters, Jams, and Honey","name":"honey","original":"3 tablespoons of honey","originalName":"honey","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/honey.png"},{"id":9152,"amount":0.5,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"juice of lemon","original":"juice of 1/2 lemon","originalName":"juice lemon","meta":[],"extendedName":"lemon (juice)","image":"https://spoonacular.com/cdn/ingredients_100x100/lemon-juice.jpg"},{"id":9206,"amount":0.5,"unit":"","unitLong":"","unitShort":"","aisle":"Beverages","name":"juice of orange","original":"juice of 1/2 orange","originalName":"juice orange","meta":[],"extendedName":"orange (juice)","image":"https://spoonacular.com/cdn/ingredients_100x100/orange-juice.jpg"},{"id":2043,"amount":1.0,"unit":"dashes","unitLong":"dashe","unitShort":"dashes","aisle":"Spices and Seasonings","name":"turmeric","original":"dashes of turmeric","originalName":"turmeric","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/turmeric.jpg"}],"usedIngredients":[{"id":2015,"amount":1.0,"unit":"teaspoon","unitLong":"teaspoon","unitShort":"tsp","aisle":"Spices and Seasonings","name":"curry","original":"teaspoon of curry","originalName":"curry","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/curry-powder.jpg"},{"id":5006,"amount":1.0,"unit":"","unitLong":"","unitShort":"","aisle":"Meat","name":"chicken","original":"1 whole chicken","originalName":"whole chicken","meta":["whole"],"extendedName":"whole chicken","image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"}],"unusedIngredients":[{"id":11206,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"cucumber","original":"cucumber","originalName":"cucumber","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/cucumber.jpg"}],"likes":2},{"id":650378,"title":"Curry Chicken Salad","image":"https://spoonacular.com/recipeImages/650378-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":7,"missedIngredients":[{"id":5311,"amount":2.0,"unit":"cans","unitLong":"cans","unitShort":"cans","aisle":"Canned and Jarred","name":"chicken","original":"2 cans canned chicken","originalName":"canned chicken","meta":["canned"],"extendedName":"canned chicken","image":"https://spoonacular.com/cdn/ingredients_100x100/canned-food.png"},{"id":11124,"amount":1.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"carrot","original":"1 Carrot, diced","originalName":"Carrot, diced","meta":["diced"],"extendedName":"diced carrot","image":"https://spoonacular.com/cdn/ingredients_100x100/sliced-carrot.png"},{"id":11143,"amount":1.0,"unit":"Stalk","unitLong":"Stalk","unitShort":"Stalk","aisle":"Produce","name":"celery","original":"1 Stalk Celery, diced","originalName":"Celery, diced","meta":["diced"],"extendedName":"diced celery","image":"https://spoonacular.com/cdn/ingredients_100x100/celery.jpg"},{"id":4025,"amount":0.5,"unit":"cup","unitLong":"cups","unitShort":"cup","aisle":"Condiments","name":"mayonnaise","original":"1/2 cup mayonnaise","originalName":"mayonnaise","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/mayonnaise.png"},{"id":9132,"amount":1.0,"unit":"handful","unitLong":"handful","unitShort":"handful","aisle":"Produce","name":"grapes","original":"1 handful red grapes, quartered","originalName":"red grapes, quartered","meta":["red","quartered"],"extendedName":"red grapes","image":"https://spoonacular.com/cdn/ingredients_100x100/red-grapes.jpg"},{"id":21052,"amount":2.0,"unit":"servings","unitLong":"servings","unitShort":"servings","aisle":"Produce","name":"salad greens","original":"Salad greens","originalName":"Salad greens","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/mixed-greens-or-mesclun.jpg"},{"id":2043,"amount":1.0,"unit":"teaspoon","unitLong":"teaspoon","unitShort":"tsp","aisle":"Spices and Seasonings","name":"turmeric powder","original":"1 teaspoon turmeric powder (to taste)","originalName":"turmeric powder (to taste)","meta":["to taste","()"],"image":"https://spoonacular.com/cdn/ingredients_100x100/turmeric.jpg"}],"usedIngredients":[{"id":11206,"amount":0.5,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"cucumber","original":"1/2 Cucumber, peeled and sliced","originalName":"Cucumber, peeled and sliced","meta":["peeled","sliced"],"image":"https://spoonacular.com/cdn/ingredients_100x100/cucumber.jpg"},{"id":2015,"amount":2.0,"unit":"teaspoons","unitLong":"teaspoons","unitShort":"tsp","aisle":"Spices and Seasonings","name":"madras curry powder","original":"2 teaspoons madras Curry powder","originalName":"madras Curry powder","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/curry-powder.jpg"}],"unusedIngredients":[{"id":5006,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Meat","name":"chicken","original":"Chicken","originalName":"Chicken","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"}],"likes":1},{"id":716268,"title":"African Chicken Peanut Stew","image":"https://spoonacular.com/recipeImages/716268-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":9,"missedIngredients":[{"id":10211821,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"bell peppers","original":"Bell Peppers for garnishing","originalName":"Bell Peppers for garnishing","meta":["for garnishing"],"image":"https://spoonacular.com/cdn/ingredients_100x100/bell-pepper-orange.png"},{"id":10211215,"amount":2.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"garlic cloves","original":"2 garlic cloves","originalName":"garlic cloves","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/garlic.jpg"},{"id":11216,"amount":1.0,"unit":"piece","unitLong":"","unitShort":"","aisle":"Produce;Ethnic Foods;Spices and Seasonings","name":"of ginger","original":"Small piece of Chopped ginger","originalName":"Small of Chopped ginger","meta":["chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/ginger.png"},{"id":16098,"amount":1.0,"unit":"cup","unitLong":"cup","unitShort":"cup","aisle":"Nut butters, Jams, and Honey","name":"groundnut","original":"1 cup of groundnut (Blended) or 1 Cooking spoon of peanut Butter","originalName":"groundnut (Blended) or 1 Cooking spoon of peanut Butter","meta":["(Blended)"],"image":"https://spoonacular.com/cdn/ingredients_100x100/peanut-butter.png"},{"id":11282,"amount":2.0,"unit":"handfuls","unitLong":"handfuls","unitShort":"handfuls","aisle":"Produce","name":"onions","original":"2 handfuls of Chopped onions","originalName":"Chopped onions","meta":["chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/brown-onion.png"},{"id":1042027,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":null,"name":"seasoning","original":"Seasoning","originalName":"Seasoning","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/seasoning.png"},{"id":11507,"amount":0.5,"unit":"small","unitLong":"smalls","unitShort":"small","aisle":"Produce","name":"sweet potato","original":"1/2 small sweet potato (Chopped)","originalName":"sweet potato (Chopped)","meta":["chopped","()"],"image":"https://spoonacular.com/cdn/ingredients_100x100/sweet-potato.png"},{"id":2049,"amount":1.0,"unit":"pinch","unitLong":"pinch","unitShort":"pinch","aisle":"Produce;Spices and Seasonings","name":"thyme","original":"Pinch of thyme","originalName":"Pinch of thyme","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/thyme.jpg"},{"id":11529,"amount":1.0,"unit":"small","unitLong":"small","unitShort":"small","aisle":"Produce","name":"tomato","original":"1 Chopped small tomato","originalName":"Chopped small tomato","meta":["chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/tomato.png"}],"usedIngredients":[{"id":5006,"amount":1.5,"unit":"cups","unitLong":"cups","unitShort":"cup","aisle":"Meat","name":"chicken","original":"1.5 cups of Chopped Chicken","originalName":"Chopped Chicken","meta":["chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"},{"id":2015,"amount":1.0,"unit":"teaspoon","unitLong":"teaspoon","unitShort":"tsp","aisle":"Spices and Seasonings","name":"curry","original":"1 teaspoon of Curry","originalName":"Curry","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/curry-powder.jpg"}],"unusedIngredients":[{"id":11206,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"cucumber","original":"cucumber","originalName":"cucumber","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/cucumber.jpg"}],"likes":124}]"""
    response_content = json.loads(json_data)
    return response_content


def create_recipe_link(recipe):
    title = recipe['title'].replace(' ', '-')
    recipe_id = recipe['id']
    link = f"https://spoonacular.com/{title}-{recipe_id}"
    return link


def get_recipe_from_product_list(request):
    # Retrieve fridges connected to the logged-in user
    fridges_of_user = Fridge.objects.filter(owners=request.user)

    # Retrieve products from the fridges of the user
    products = Product.objects.filter(fridge__in=fridges_of_user)

    if len(products) == 0:
        return render(request, 'recipe/recipe_list.html',
                      {'products': products})
    else:
        products_names = []
        for product in products:
            products_names.append(product.name)

        products_names = ','.join([name + '+' for name in products_names])[:-1]

        # get recipes from api
        recipes = get_recipes(products_names)

        for recipe in recipes:
            # print(recipe)
            recipe['recipe_link'] = create_recipe_link(recipe)

        p = Paginator(products, 2)  # 2nd arg --> objects per page
        page = request.GET.get('page')
        products_to_show = p.get_page(page)
        return render(request, 'recipe/recipe_list.html',
                      {'products': products_to_show, 'recipes': recipes})


def recipe_saved_list(request):
    recipes = Recipe.objects.filter(saved_by=request.user).annotate(num_saved_users=Count('saved_by'))
    context = {'recipes': recipes}
    return render(request, 'recipe/recipe_saved.html',
                  context)


def recipe_save(request):
    if request.method == 'POST':
        recipe_title = request.POST.get('recipe_title')
        recipe_image_link = request.POST.get('recipe_image_link')
        recipe_link = request.POST.get('recipe_link')
        recipe_id = request.POST.get('recipe_id')
        recipe_api_likes = request.POST.get('recipe_api_likes')

        recipe = Recipe(id=recipe_id,
                        title=recipe_title,
                        link=recipe_link,
                        image_link=recipe_image_link,
                        api_likes=recipe_api_likes)
        recipe.save()

        recipe.saved_by.add(request.user)

        messages.success(request, 'Recipe saved successfully!')
        return redirect('recipe_list')


def recipe_unsave(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.saved_by.remove(request.user)  # remove the connection to this user

        # if no users saved this recipe, delete it from database
        counter = recipe.saved_by.count()
        if counter == 0:
            recipe.delete()

        messages.success(request, 'Recipe unsaved successfully!')
        return redirect('recipe_list')

