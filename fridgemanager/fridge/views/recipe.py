import json
import requests
from django.shortcuts import get_object_or_404, render, redirect
from ..models import Recipe, Product, Fridge
from ..api_key import api_key_value
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from ast import literal_eval


def get_recipes_from_api(products_names, number_of_recipes):
    # deployment
    base_url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {'apiKey': api_key_value,
              'number': number_of_recipes,
              'ingredients': str(products_names)
              }

    response = requests.get(base_url, params=params)
    recipes = literal_eval(response.content.decode('utf-8'))
    # print(recipes)
    # response_debugging_content = b'[{"id":633538,"title":"Baked Chicken with Cinnamon Apples","image":"https://spoonacular.com/recipeImages/633538-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":3,"missedIngredients ":[{"id":2010,"amount":4.0,"unit":"servings","unitLong":"servings","unitShort":"servings","aisle":"Spices and Seasonings","name":"powdered cinnamon","original":"Powdered Cinnamon, to taste","originalName":"Powdered Cinnamon, to tast e","meta":["to taste"],"image":"https://spoonacular.com/cdn/ingredients_100x100/cinnamon.jpg"},{"id":11282,"amount":0.5,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"onion","original":"1/2 Large Onion or 1 Small O nion, peeled & quartered","originalName":"Large Onion or 1 Small Onion, peeled & quartered","meta":["peeled","quartered"],"image":"https://spoonacular.com/cdn/ingredients_100x100/brown-onion.png"},{"id":14106,"amount":0.5,"unit":"cu p","unitLong":"cups","unitShort":"cup","aisle":"Alcoholic Beverages","name":"white wine","original":"1/2 cup White Wine","originalName":"White Wine","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/white-wine.jpg"} ],"usedIngredients":[{"id":9003,"amount":2.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"apples","original":"2 Apples (Granny Smith, McIntosh, Crispin, Jonagold, Fuji, Golden Delicious), washed, cored, & quarter ed","originalName":"Apples (Granny Smith, McIntosh, Crispin, Jonagold, Fuji, Golden Delicious), washed, cored, & quartered","meta":["washed","cored","quartered","(Granny Smith, McIntosh, Crispin, Jonagold, Fuji, Golden Delicious)"], "image":"https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"},{"id":5006,"amount":1.0,"unit":"","unitLong":"","unitShort":"","aisle":"Meat","name":"chicken","original":"1 Whole Chicken, washed and excess fat removed","origina lName":"Whole Chicken, washed and excess fat removed","meta":["whole","washed and excess fat removed"],"extendedName":"whole chicken","image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"}],"unusedIngredients": [{"id":9040,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"banana","original":"Banana+","originalName":"Banana","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/b ananas.jpg"},{"id":9200,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"orange","original":"orange+","originalName":"orange","meta":[],"image":"https://spoonacular.com/cdn/ingredien ts_100x100/orange.png"},{"id":9295,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"pomelo","original":"pomelo","originalName":"pomelo","meta":[],"image":"https://spoonacular.com/cdn /ingredients_100x100/pomelo-fruit.jpg"}],"likes":1},{"id":52530,"title":"Island Jam","image":"https://spoonacular.com/recipeImages/52530-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":4,"missedIngredi ents":[{"id":9181,"amount":4.0,"unit":"cups","unitLong":"cups","unitShort":"cup","aisle":"Produce","name":"cantaloupe","original":"4 cups cantaloupe, peeled and diced","originalName":"cantaloupe, peeled and diced","meta":["diced","p eeled"],"extendedName":"diced cantaloupe","image":"https://spoonacular.com/cdn/ingredients_100x100/cantaloupe.png"},{"id":9152,"amount":0.25,"unit":"cup","unitLong":"cups","unitShort":"cup","aisle":"Produce","name":"lemon juice","or iginal":"1/4 cup lemon juice","originalName":"lemon juice","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/lemon-juice.jpg"},{"id":9156,"amount":1.0,"unit":"tsp","unitLong":"teaspoon","unitShort":"tsp","aisle":"Pr oduce","name":"lemon rind","original":"1 tsp lemon rind","originalName":"lemon rind","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/zest-lemon.jpg"},{"id":9216,"amount":1.0,"unit":"tsp","unitLong":"teaspoon","uni tShort":"tsp","aisle":"Produce","name":"orange rind","original":"1 tsp orange rind","originalName":"orange rind","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/orange-zest.png"}],"usedIngredients":[{"id":9040,"am ount":3.0,"unit":"cups","unitLong":"cups","unitShort":"cup","aisle":"Produce","name":"bananas","original":"3 cups bananas","originalName":"bananas","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/bananas.jpg"},{"i d":9200,"amount":3.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"oranges","original":"3 oranges, peeled and diced","originalName":"oranges, peeled and diced","meta":["diced","peeled"],"extendedName":"diced orang es","image":"https://spoonacular.com/cdn/ingredients_100x100/orange.png"}],"unusedIngredients":[{"id":5006,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Meat","name":"chicken","original":"chicken+ ","originalName":"chicken","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"},{"id":9003,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"apples", "original":"apples+","originalName":"apples","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"},{"id":9295,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name" :"pomelo","original":"pomelo","originalName":"pomelo","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/pomelo-fruit.jpg"}],"likes":0},{"id":638604,"title":"Chilled Swiss Oatmeal","image":"https://spoonacular.com/re cipeImages/638604-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":5,"missedIngredients":[{"id":8121,"amount":0.5,"unit":"cup","unitLong":"cups","unitShort":"cup","aisle":"Cereal","name":"old-fashioned  oatmeal","original":"1/2 cup old-fashioned oatmeal (may use steel cut but not the instant kind)","originalName":"old-fashioned oatmeal (may use steel cut but not the instant kind)","meta":["instant","(may use steel cut but not the k ind)"],"image":"https://spoonacular.com/cdn/ingredients_100x100/porridge-or-cream-of-wheat.png"},{"id":1001119,"amount":6.0,"unit":"oz","unitLong":"ounces","unitShort":"oz","aisle":"Milk, Eggs, Other Dairy","name":"vanilla yogurt"," original":"6 oz low-fat vanilla yogurt (if using plain yogurt, add honey for sweetness)","originalName":"low-fat vanilla yogurt (if using plain yogurt, add honey for sweetness)","meta":["plain","low-fat","for sweetness","(if using y ogurt, add honey )"],"extendedName":"low fat plain vanilla yogurt","image":"https://spoonacular.com/cdn/ingredients_100x100/vanilla-yogurt.png"},{"id":1077,"amount":0.33333334,"unit":"cup","unitLong":"cups","unitShort":"cup","aisle" :"Milk, Eggs, Other Dairy","name":"milk","original":"1/3 cup milk","originalName":"milk","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/milk.png"},{"id":9078,"amount":2.0,"unit":"tablespoon","unitLong":"tablespoo ns","unitShort":"Tbsp","aisle":"Produce","name":"cranberry","original":"2-3 tablespoon dried cranberry or raisins","originalName":"dried cranberry or raisins","meta":["dried"],"extendedName":"dried cranberry","image":"https://spoona cular.com/cdn/ingredients_100x100/cranberries.jpg"},{"id":12155,"amount":1.0,"unit":"tablespoon","unitLong":"tablespoon","unitShort":"Tbsp","aisle":"Nuts;Baking","name":"walnuts","original":"1 tablespoon walnuts","originalName":"wal nuts","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/walnuts.jpg"}],"usedIngredients":[{"id":9003,"amount":1.0,"unit":"small","unitLong":"small","unitShort":"small","aisle":"Produce","name":"apple","original":"1  small apple, chopped","originalName":"apple, chopped","meta":["chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"},{"id":9040,"amount":1.0,"unit":"small","unitLong":"small","unitShort":"small","aisle":"Pro duce","name":"banana","original":"1 small banana, chopped","originalName":"banana, chopped","meta":["chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/bananas.jpg"}],"unusedIngredients":[{"id":5006,"amount":1.0,"uni t":"serving","unitLong":"serving","unitShort":"serving","aisle":"Meat","name":"chicken","original":"chicken+","originalName":"chicken","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"},{"id":9200 ,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"orange","original":"orange+","originalName":"orange","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/orange.png"} ,{"id":9295,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"pomelo","original":"pomelo","originalName":"pomelo","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/po melo-fruit.jpg"}],"likes":7},{"id":658737,"title":"Roja Sangria","image":"https://spoonacular.com/recipeImages/658737-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":5,"missedIngredients":[{"id":14097, "amount":2.0,"unit":"bottles","unitLong":"bottles","unitShort":"bottles","aisle":"Alcoholic Beverages","name":"dry\\" roja\\" wine","original":"2 bottles dry\\" roja\\" Spanish wine","originalName":"dry\\" roja\\" Spanish wine","met a":["spanish"],"extendedName":"spanish dry\\" roja\\" wine","image":"https://spoonacular.com/cdn/ingredients_100x100/red-wine.jpg"},{"id":10114037,"amount":1.0,"unit":"cup","unitLong":"cup","unitShort":"cup","aisle":"Alcoholic Bever ages","name":"brandy","original":"1 cup Brandy","originalName":"Brandy","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/brandy.png"},{"id":14144,"amount":12.0,"unit":"ounces","unitLong":"ounces","unitShort":"oz"," aisle":"Beverages","name":"sprite","original":"12 ounces cans of Sprite","originalName":"Sprite","meta":["canned"],"extendedName":"canned sprite","image":"https://spoonacular.com/cdn/ingredients_100x100/soda-can.jpg"},{"id":9302,"am ount":1.0,"unit":"small container","unitLong":"small container","unitShort":"small container","aisle":"Produce","name":"raspberries","original":"1 small container raspberries","originalName":"raspberries","meta":[],"image":"https:// spoonacular.com/cdn/ingredients_100x100/raspberries.jpg"},{"id":9159,"amount":2.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"limes","original":"2 limes","originalName":"limes","meta":[],"image":"https://spoonac ular.com/cdn/ingredients_100x100/lime.jpg"}],"usedIngredients":[{"id":1069003,"amount":2.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"apples","original":"2 green apples","originalName":"green apples","meta":["g reen"],"extendedName":"green apples","image":"https://spoonacular.com/cdn/ingredients_100x100/grannysmith-apple.png"},{"id":9200,"amount":2.0,"unit":"","unitLong":"","unitShort":"","aisle":"Produce","name":"oranges","original":"2 or anges","originalName":"oranges","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/orange.png"}],"unusedIngredients":[{"id":9040,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produ ce","name":"banana","original":"Banana+","originalName":"Banana","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/bananas.jpg"},{"id":5006,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","a isle":"Meat","name":"chicken","original":"chicken+","originalName":"chicken","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"},{"id":9295,"amount":1.0,"unit":"serving","unitLong":"serving","unitS hort":"serving","aisle":"Produce","name":"pomelo","original":"pomelo","originalName":"pomelo","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/pomelo-fruit.jpg"}],"likes":1},{"id":653810,"title":"Orange Banana Muff ins With Pistachios","image":"https://spoonacular.com/recipeImages/653810-312x231.jpg","imageType":"jpg","usedIngredientCount":2,"missedIngredientCount":5,"missedIngredients":[{"id":19912,"amount":0.5,"unit":"cup","unitLong":"cups", "unitShort":"cup","aisle":"Ethnic Foods;Health Foods","name":"agave syrup","original":"1/2 cup agave syrup","originalName":"agave syrup","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/agave.png"},{"id":18369,"amo unt":2.0,"unit":"tablespoons","unitLong":"tablespoons","unitShort":"Tbsp","aisle":"Baking","name":"baking powder","original":"2 tablespoons baking powder","originalName":"baking powder","meta":[],"image":"https://spoonacular.com/cdn /ingredients_100x100/white-powder.jpg"},{"id":1123,"amount":2.0,"unit":"","unitLong":"","unitShort":"","aisle":"Milk, Eggs, Other Dairy","name":"eggs","original":"2 eggs","originalName":"eggs","meta":[],"image":"https://spoonacular. com/cdn/ingredients_100x100/egg.png"},{"id":12151,"amount":0.25,"unit":"cup","unitLong":"cups","unitShort":"cup","aisle":"Nuts;Savory Snacks","name":"pistachios","original":"1/4 cup chopped pistachios","originalName":"chopped pistac hios","meta":["chopped"],"image":"https://spoonacular.com/cdn/ingredients_100x100/pistachios.jpg"},{"id":8402,"amount":2.0,"unit":"cups","unitLong":"cups","unitShort":"cup","aisle":"Cereal","name":"cooking oats","original":"2 cups q uick cooking oats","originalName":"quick cooking oats","meta":["quick"],"image":"https://spoonacular.com/cdn/ingredients_100x100/rolled-oats.jpg"}],"usedIngredients":[{"id":9040,"amount":3.0,"unit":"","unitLong":"","unitShort":"","a isle":"Produce","name":"bananas","original":"3 bananas, mashed","originalName":"bananas, mashed","meta":["mashed"],"image":"https://spoonacular.com/cdn/ingredients_100x100/bananas.jpg"},{"id":9200,"amount":2.0,"unit":"","unitLong":" ","unitShort":"","aisle":"Produce","name":"oranges","original":"2 oranges","originalName":"oranges","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/orange.png"}],"unusedIngredients":[{"id":5006,"amount":1.0,"unit" :"serving","unitLong":"serving","unitShort":"serving","aisle":"Meat","name":"chicken","original":"chicken+","originalName":"chicken","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/whole-chicken.jpg"},{"id":9003," amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"apples","original":"apples+","originalName":"apples","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/apple.jpg"},{" id":9295,"amount":1.0,"unit":"serving","unitLong":"serving","unitShort":"serving","aisle":"Produce","name":"pomelo","original":"pomelo","originalName":"pomelo","meta":[],"image":"https://spoonacular.com/cdn/ingredients_100x100/pomelo-fruit.jpg"}],"likes":1}]'
    # recipes = literal_eval(response_debugging_content.decode('utf-8'))

    return recipes


def create_recipe_link(recipe_title, recipe_id):
    title = recipe_title.replace(' ', '-')
    link = f"https://spoonacular.com/{title}-{recipe_id}"
    return link


def get_recipe_from_product_list(request):
    # check if user has any products and fridges
    fridges_of_user = Fridge.objects.filter(owners=request.user)
    products_in_fridges = Product.objects.filter(fridge__in=fridges_of_user)
    if fridges_of_user.count() > 0:
        if products_in_fridges.count() > 0:

            number_of_recipes = 5
            # if the user has enough daily points, search for new recipes
            if request.user.userprofile.daily_points >= number_of_recipes:
                # retrieve fridges connected to the logged-in user
                fridges_of_user = Fridge.objects.filter(owners=request.user)

                # retrieve products from the fridges of the user
                products = Product.objects.filter(fridge__in=fridges_of_user).order_by('created_date')

                if len(products) == 0:
                    return render(request, 'recipe/recipe_list.html',
                                  {'products': products})
                else:
                    products_names = []
                    for product in products:
                        products_names.append(product.name)

                    products_names = ','.join([name + '+' for name in products_names])[:-1]

                    recipes = get_recipes_from_api(products_names, number_of_recipes)

                    for recipe in recipes:
                        # if the recipe already exists, does not save it
                        try:
                            matching_recipe = Recipe.objects.get(id=recipe['id'])
                            matching_recipe.visible_as_daily_recipe.add(request.user)
                            matching_recipe.save()
                        except Recipe.DoesNotExist:
                            new_recipe = Recipe.objects.create(
                                id=recipe['id'],
                                title=recipe['title'],
                                image_link=recipe['image'],
                                api_likes=recipe['likes'],
                                link=create_recipe_link(recipe['title'], recipe['id'])
                            )
                            new_recipe.save()
                            new_recipe.visible_as_daily_recipe.add(request.user)


                    # update user points after using API:
                    request.user.userprofile.daily_points -= number_of_recipes
                    request.user.userprofile.save()

                    return render(request, 'recipe/recipe_list.html',
                                  {'recipes': recipes, 'fridges_of_user': fridges_of_user, 'products_in_fridges': products_in_fridges})
            else:
                current_user = request.user
                # Filter recipes that are visible to the current user
                visible_recipes = Recipe.objects.filter(visible_as_daily_recipe=current_user)

                context = {'visible_recipes': visible_recipes, 'fridges_of_user': fridges_of_user, 'products_in_fridges': products_in_fridges}

                return render(request, 'recipe/recipe_list.html', context)
        else:
            return render(request, 'recipe/recipe_list.html')
    else:
        return render(request, 'recipe/recipe_list.html')


def get_recipe_favourite_list(request):
    recipes = Recipe.objects.filter(favourite_by=request.user).annotate(num_saved_users=Count('favourite_by'))
    context = {'recipes': recipes}
    return render(request, 'recipe/recipe_saved.html',
                  context)


def recipe_make_favourite(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        recipe.favourite_by.add(request.user)

        messages.success(request, 'Recipe saved successfully!')
        return redirect('recipe_list')


def recipe_unmake_favourite(request):
    if request.method == 'POST':
        recipe_id = request.POST.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.favourite_by.remove(request.user)  # remove the connection to this user

        # if no users saved this recipe, delete it from database
        counter = recipe.favourite_by.count()
        counter += recipe.visible_as_daily_recipe.count()
        if counter == 0:
            recipe.delete()

        messages.success(request, 'Recipe unsaved successfully!')
        return redirect('recipe_list')
