# Fridge Manager - web application using Django framework

Author: **Krzysztof Nazar**

## [Live demo](https://fridgemanagerbykn.pythonanywhere.com/) 
Use [**this link**](https://fridgemanagerbykn.pythonanywhere.com/) to check the demo of this application hosted by [Pythonanywhere.com](https://pythonanywhere.com).

## The goal of the project
**The goal of this project is to deploy a Django web application allowing the users to manage their fridges and reduce the food waste.**
The key functionality of the app is to search for recipes using the products stored currently in the fridge.


## Main functionalities of the application

The application provides an interface and tools designed for managing products stored in a fridge.

The key functionalities in the app include:
- **Register as a new user** - Register to the system.
- **Add your fridge** - Create your fridge and define its details
- **Share your fridge with another users** - Use an invitation link, send it to another user, and manage one fridge together
- **Add products to your fridge** - Add new products by defining their name, expiration date, amount, etc.
- **Search for recipes** - Check out the meal which can be made using the products in your fridge
- **User dashboard** - See statistics of your account in one place

## Why did I create this?

By creating this app I would like to have an impact on the global food waste problem.
According to [Greenly Institute](https://greenly.earth/en-us/blog/ecology-news/global-food-waste-in-2022):

"Over a third of all food produced (~2.5 billion tons) is lost or wasted each year.
One third of this occurs in the food production stage.
Boston Consulting Group (BCG) estimates this wasted food is worth $230 billion.

👉 Researchers estimate the lost food calories from food waste amount to roughly 24% of the total available food calories."

Users of my app can **#ActLocallyAndThinkGlobally** by reducing their own food waste.


## What I've learnt during this project?
During this project I learnt how to:
- setup user authorisation in Django ([docs](https://docs.djangoproject.com/en/4.2/topics/auth/))
- use Bootstrap for styling ([docs](https://getbootstrap.com/docs/4.0/content/images/))
- create custom error pages ([tutorial](https://dev.to/riyanagueco/creating-a-custom-error-page-on-django-3nnd))
- manage relationships between Django models ([docs](https://docs.djangoproject.com/en/4.2/topics/db/models/))
- improved my skills in creating Django forms ([docs](https://docs.djangoproject.com/en/4.2/topics/forms/))
- use spoonacular API ([docs](https://spoonacular.com/food-api/docs))

## Used libraries
 - Django
 - requests
 - secrets
 
## Possible future improvements

- **Add an option to define the priority of products used as ingredients** - the user can define what products he/she wants to use today

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)