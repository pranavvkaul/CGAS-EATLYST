from flask import Flask, request, jsonify
from flask_cors import CORS 
import google.generativeai as genai
import os 
import sys

API_KEY = "AIzaSyCQClSBITdW0LcdeXAYZZ-yo1TQmph9QNY"
genai.configure(api_key=API_KEY)

GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

SYSTEM_INSTRUCTION = (
    
    "You are Chef Bot, a master culinary expert and friendly sous chef. "
    "Your primary purpose is to provide detailed, step-by-step recipes, "
    "expert cooking techniques, and comprehensive food advice. "
    "Always maintain a warm and enthusiastic tone. "
    "When asked for a recipe, provide a brief, engaging introduction followed by clear, concise steps. "
    "Be concise, short and to the point in your responses. "
    '''
    if someone asks what eatlyst is please answer according to below content: Eatlyst will be a dynamic and interactive web application that helps users discover new recipes and explore foods based on their nutritional preferences. The platform will feature a “Recipe of the Day” that displays a randomly selected recipe each time the page is refreshed, making food discovery fun and effortless. It will also include a “Suggest a Food” option, where users can input their preferred nutritional ranges for carbohydrates, protein, fats, and calories to receive personalized food suggestions. The goal of the project is to make exploring healthy food options engaging, simple, and informative.
    remember if a question is somehow related to the below content, you must use the data to answer it.
    if some data is missing, you can refer to the internet and reform answers based on 
    Calorie_per_100g"
    "Carbohydrate_per_100g"
    "Protein_per_100g"
    "Fat_per_100g"
[
  {
    "Dish": "Papad",
    "Calorie_per_100g": 371,
    "Carbohydrate_per_100g": 59.87,
    "Protein_per_100g": 25.56,
    "Fat_per_100g": 3.25,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/papad?portionid=63356&portionamount=100.000"
  },
  {
    "Dish": "Vada",
    "Calorie_per_100g": 282,
    "Carbohydrate_per_100g": 40.97,
    "Protein_per_100g": 10.59,
    "Fat_per_100g": 8.64,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/vada"
  },
  {
    "Dish": "Samosa",
    "Calorie_per_100g": 308,
    "Carbohydrate_per_100g": 32.21,
    "Protein_per_100g": 4.67,
    "Fat_per_100g": 17.86,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/pastry-filled-with-potatoes-and-peas-(fried)?portionamount=100.000&portionid=53636&utm"
  },
  {
    "Dish": "Barfi",
    "Calorie_per_100g": 285,
    "Carbohydrate_per_100g": 38.82,
    "Protein_per_100g": 6.83,
    "Fat_per_100g": 12.1,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/barfi-or-burfi-indian-dessert-%28made-from-milk-or-cream-or-ricotta-cheese%29?portionamount=100.000&portionid=49913&utm"
  },
  {
    "Dish": "Fishcurry",
    "Calorie_per_100g": 100,
    "Carbohydrate_per_100g": 1.9,
    "Protein_per_100g": 12.4,
    "Fat_per_100g": 4.59,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/fish-curry?portionid=5406867&portionamount=100.000"
  },
  {
    "Dish": "Kachori",
    "Calorie_per_100g": 270,
    "Carbohydrate_per_100g": 35.69,
    "Protein_per_100g": 9.84,
    "Fat_per_100g": 10.01,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/kachori?portionid=5613275&portionamount=100.000"
  },
  {
    "Dish": "Vadapav",
    "Calorie_per_100g": 217,
    "Carbohydrate_per_100g": 28.69,
    "Protein_per_100g": 6.55,
    "Fat_per_100g": 8.51,
    "Source": "https://foods.fatsecret.com/calories-nutrition/generic/vada-pav?portionid=16763051&portionamount=100.000"
  },
  {
    "Dish": "Rasmalai",
    "Calorie_per_100g": 187,
    "Carbohydrate_per_100g": 18,
    "Protein_per_100g": 7.2,
    "Fat_per_100g": 9.6,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/amul/rasmalai/100g"
  },
  {
    "Dish": "Chicken Kabab",
    "Calorie_per_100g": 151,
    "Carbohydrate_per_100g": 19.83,
    "Protein_per_100g": 9.09,
    "Fat_per_100g": 3.67,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/chicken-kebab?portionamount=100.000&portionid=5164507&utm"
  },
  {
    "Dish": "Rasam",
    "Calorie_per_100g": 19,
    "Carbohydrate_per_100g": 2.82,
    "Protein_per_100g": 0.39,
    "Fat_per_100g": 0.88,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/rasam?portionid=7168139&portionamount=100.000"
  },
  {
    "Dish": "Gatte Ki Sabzi",
    "Calorie_per_100g": 110,
    "Carbohydrate_per_100g": 14.62,
    "Protein_per_100g": 8,
    "Fat_per_100g": 5.4,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/gatte-ki-sabzi?portionid=35472970&portionamount=100.000"
  },
  {
    "Dish": "Kadhi Pakora",
    "Calorie_per_100g": 230,
    "Carbohydrate_per_100g": 16.82,
    "Protein_per_100g": 6.45,
    "Fat_per_100g": 5.11,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/kadhi-pakora?portionid=53630958&portionamount=100.000"
  },
  {
    "Dish": "Ghewar",
    "Calorie_per_100g": 76,
    "Carbohydrate_per_100g": 13.24,
    "Protein_per_100g": 1.04,
    "Fat_per_100g": 2.09,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/ghewar"
  },
  {
    "Dish": "Aloomatter",
    "Calorie_per_100g": 98,
    "Carbohydrate_per_100g": 16.48,
    "Protein_per_100g": 3.29,
    "Fat_per_100g": 2.96,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/aloo-matar?portionid=8891398&portionamount=100.000"
  },
  {
    "Dish": "Prawns",
    "Calorie_per_100g": 105,
    "Carbohydrate_per_100g": 0.9,
    "Protein_per_100g": 20.14,
    "Fat_per_100g": 1.72,
    "Source": "https://foods.fatsecret.com/calories-nutrition/generic/prawns?portionid=320904&portionamount=100.000"
  },
  {
    "Dish": "Whole Wheat Sandwich Bread",
    "Calorie_per_100g": 245,
    "Carbohydrate_per_100g": 49,
    "Protein_per_100g": 9.5,
    "Fat_per_100g": 0.6,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/moreish/whole-wheat-sandwich-bread/100g"
  },
  {
    "Dish": "Dahipuri",
    "Calorie_per_100g": 204,
    "Carbohydrate_per_100g": 18.5,
    "Protein_per_100g": 3.4,
    "Fat_per_100g": 13.26,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/dahi-puri?portionid=61059711&portionamount=100.000"
  },
  {
    "Dish": "Haleem",
    "Calorie_per_100g": 157,
    "Carbohydrate_per_100g": 15.2,
    "Protein_per_100g": 9.77,
    "Fat_per_100g": 6.86,
    "Source": "https://foods.fatsecret.com/calories-nutrition/generic/haleem?portionid=21956918&portionamount=100.000"
  },
  {
    "Dish": "Aloogobi",
    "Calorie_per_100g": 86,
    "Carbohydrate_per_100g": 13.62,
    "Protein_per_100g": 2.29,
    "Fat_per_100g": 3.51,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/aloo-gobi?portionid=5772077&portionamount=100.000"
  },
  {
    "Dish": "Eggbhurji",
    "Calorie_per_100g": 82,
    "Carbohydrate_per_100g": 6.33,
    "Protein_per_100g": 3.75,
    "Fat_per_100g": 5.02,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/egg-bhurji?portionid=17042606&portionamount=100.000"
  },
  {
    "Dish": "Lemon rice",
    "Calorie_per_100g": 146,
    "Carbohydrate_per_100g": 31.48,
    "Protein_per_100g": 3,
    "Fat_per_100g": 0.55,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/lemon-rice"
  },
  {
    "Dish": "Bhindimasala",
    "Calorie_per_100g": 112,
    "Carbohydrate_per_100g": 13.51,
    "Protein_per_100g": 2.99,
    "Fat_per_100g": 6.4,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/bhindi-masala"
  },
  {
    "Dish": "Matar Mushroom",
    "Calorie_per_100g": 71,
    "Carbohydrate_per_100g": 10.35,
    "Protein_per_100g": 3.36,
    "Fat_per_100g": 2.67,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/matar-mushroom?portionid=62405181&portionamount=100.000"
  },
  {
    "Dish": "Gajar Halwa",
    "Calorie_per_100g": 175,
    "Carbohydrate_per_100g": 30.48,
    "Protein_per_100g": 4.07,
    "Fat_per_100g": 5,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/gajar-halwa?portionid=6724565&portionamount=100.000"
  },
  {
    "Dish": "Chicken Tikka",
    "Calorie_per_100g": 150,
    "Carbohydrate_per_100g": 7.62,
    "Protein_per_100g": 22.52,
    "Fat_per_100g": 3.02,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/chicken-tikka?portionid=5866731&portionamount=100.000"
  },
  {
    "Dish": "Tandoorichicken",
    "Calorie_per_100g": 103,
    "Carbohydrate_per_100g": 7.8,
    "Protein_per_100g": 11.71,
    "Fat_per_100g": 2.75,
    "Source": "https://www.fatsecret.co.za/calories-nutrition/generic/tandoori-chicken"
  },
  {
    "Dish": "Lauki Sabzi",
    "Calorie_per_100g": 61,
    "Carbohydrate_per_100g": 7.61,
    "Protein_per_100g": 1.68,
    "Fat_per_100g": 3.5,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/lauki-sabzi?portionid=35885349&portionamount=100.000"
  },
  {
    "Dish": "Baingan Bharta",
    "Calorie_per_100g": 97,
    "Carbohydrate_per_100g": 12.57,
    "Protein_per_100g": 1.69,
    "Fat_per_100g": 5.28,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/baingan-bharta?portionid=6009570&portionamount=100.000"
  },
  {
    "Dish": "boondi",
    "Calorie_per_100g": 584,
    "Carbohydrate_per_100g": 39.55,
    "Protein_per_100g": 13.75,
    "Fat_per_100g": 41.17,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/haldirams/boondi/100g"
  },
  {
    "Dish": "tilkut",
    "Calorie_per_100g": 238,
    "Carbohydrate_per_100g": 30.16,
    "Protein_per_100g": 4.43,
    "Fat_per_100g": 12.38,
    "Source": "https://www.fatsecret.com.sg/calories-nutrition/generic/tilkut"
  },
  {
    "Dish": "Basundi",
    "Calorie_per_100g": 192,
    "Carbohydrate_per_100g": 18,
    "Protein_per_100g": 5.3,
    "Fat_per_100g": 11,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/amul/basundi/100g"
  },
  {
    "Dish": "kothimbirvadi",
    "Calorie_per_100g": 90,
    "Carbohydrate_per_100g": 14.32,
    "Protein_per_100g": 4.11,
    "Fat_per_100g": 2.24,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/kothimbir-vadi?portionid=52275805&portionamount=100.000"
  },
  {
    "Dish": "sabudanakhichdi",
    "Calorie_per_100g": 199,
    "Carbohydrate_per_100g": 30.1,
    "Protein_per_100g": 2.72,
    "Fat_per_100g": 7.91,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/sabudana-khichdi"
  },
  {
    "Dish": "Chettinad chicken",
    "Calorie_per_100g": 180,
    "Carbohydrate_per_100g": 7.19,
    "Protein_per_100g": 16.22,
    "Fat_per_100g": 10,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/chicken-chettinad"
  },
  {
    "Dish": "Chikki",
    "Calorie_per_100g": 483,
    "Carbohydrate_per_100g": 53.56,
    "Protein_per_100g": 14,
    "Fat_per_100g": 26.8,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/chikki?portionid=7168197&portionamount=100.000"
  },
  {
    "Dish": "avial",
    "Calorie_per_100g": 108,
    "Carbohydrate_per_100g": 14.11,
    "Protein_per_100g": 1.83,
    "Fat_per_100g": 5.78,
    "Source": "https://www.fatsecret.co.in/calories-nutrition/generic/avial"
  },
  {
    "Dish": "patishapta",
    "Calorie_per_100g": 234,
    "Carbohydrate_per_100g": 42.56,
    "Protein_per_100g": 8.73,
    "Fat_per_100g": 4.26,
    "Source": "https://www.fatsecret.co.uk/calories-nutrition/generic/patishapta?portionid=57423198&portionamount=100.000"
  },
  {
    "Dish": "imarti",
    "Calorie_per_100g": 226,
    "Carbohydrate_per_100g": 31.71,
    "Protein_per_100g": 3.14,
    "Fat_per_100g": 10.6,
    "Source": "https://www.fatsecret.co.nz/calories-nutrition/generic/imarti?portionid=53557016&portionamount=100.000"
  },
  {
    "Dish": "Jalebi",
    "Calorie_per_100g": 300,
    "Carbohydrate_per_100g": 62.36,
    "Protein_per_100g": 4.19,
    "Fat_per_100g": 4.31,
    "Source": "https://foods.fatsecret.com/calories-nutrition/generic/jalebi?portionamount=100.000&portionid=16477981"
  }
]

[
  {
    "Recipe_Name": "Deep-Fried Peanuts",
    "Recipe_URL": "https://www.allrecipes.com/recipe/239295/deep-fried-peanuts/",
    "Detailed_Ingredients": "oil for frying as needed, 1 cup shelled raw peanuts, salt to taste",
    "Instructions": "Heat oil in a deep-fryer or large saucepan to 350 degrees F (175 degrees C). Cook peanuts in preheated oil until fragrant and hot, about 2 minutes. Transfer to paper towel-lined plates to drain. Season peanuts with salt",
    "Prep_Time": "10 mins",
    "Image_Link": "image/1.png"
  },
  {
    "Recipe_Name": "Oven-Fried Potatoes",
    "Recipe_URL": "https://www.allrecipes.com/recipe/18905/oven-fried-potatoes-i/",
    "Detailed_Ingredients": "½ cup unsalted butter, diced, more for the dish, 5 pounds red potatoes, thinly sliced, 1 onion, finely chopped, 6 strips bacon, chopped, salt and ground black pepper to taste",
    "Instructions": "Preheat the oven to 400 degrees F (200 degrees C). Grease a 9x13-inch casserole dish. Place potatoes in an even layer in the prepared dish. Sprinkle onion and bacon over potatoes; dot with diced butter. Cover the dish with aluminum foil. Bake in the preheated oven for 45 minutes. Remove foil; stir potatoes. Turn on the broiler and broil until until potatoes are brown and crisp, about 5 minutes. You may need to stir every minute or so for even browning. Serve immediately.",
    "Prep_Time": "1 hr 30 mins",
    "Image_Link": "image/2.png"
  },
  {
    "Recipe_Name": "Herbed Dumplings",
    "Recipe_URL": "https://www.allrecipes.com/recipe/87270/herbed-dumplings/",
    "Detailed_Ingredients": "1½ cups all-purpose flour, 2 teaspoons baking powder, 1 teaspoon salt, 1 teaspoon baking soda, 1 teaspoon dried thyme, 1 teaspoon dried parsley, 1 teaspoon dried oregano, 3 tablespoons unsalted butter, ¾ cup milk",
    "Instructions": "Combine flour, baking powder, salt, baking soda, thyme, parsley, and oregano in a bowl. Cut in butter until mixture resembles coarse crumbs. Gradually add milk, using just enough to form a thick batter. Drop by rounded tablespoons into simmering soup or stew, cover, and cook for 15 minutes.",
    "Prep_Time": "20 mins",
    "Image_Link": "image/3.png"
  },
  {
    "Recipe_Name": "Shrimply Delicious Shrimp Salad",
    "Recipe_URL": "https://www.allrecipes.com/recipe/87228/shrimply-delicious-shrimp-salad/",
    "Detailed_Ingredients": "1 pound large peeled and deveined cooked shrimp, 1 cup chopped celery, 1 large carrot, shredded, ½ cup chopped onion, 2 hard-cooked eggs, chopped, ¾ cup mayonnaise, salt and ground black pepper to taste",
    "Instructions": "Gently toss shrimp, celery, carrot, onion, eggs, and mayonnaise together in a large bowl; season with salt and black pepper. Chill until ready to serve.",
    "Prep_Time": "15 mins",
    "Image_Link": "image/4.png"
  },
  {
    "Recipe_Name": "Slow-Cooker Barbecue Ribs",
    "Recipe_URL": "https://www.allrecipes.com/recipe/22230/slow-cooker-barbecue-ribs/",
    "Detailed_Ingredients": "4 pounds pork baby back ribs, salt and ground black pepper to taste, 2 cups ketchup, 1 cup chili sauce, ½ cup packed brown sugar, 1/4 cup vinegar, 2 teaspoons dried oregano, 2 teaspoons Worcestershire sauce, 1 dash hot sauce",
    "Instructions": "Preheat the oven to 400 degrees F (200 degrees C), season ribs with salt and black pepper, place in a shallow baking pan, brown in the preheated oven for 15 minutes, flip, brown 15 minutes more, drain fat, transfer ribs to a slow cooker, combine ketchup, chili sauce, brown sugar, vinegar, oregano, Worcestershire sauce, hot sauce, salt, and black pepper in a medium bowl, pour sauce over ribs, flip to coat, cover slow cooker, cook on Low until ribs are tender, 6 to 8 hours.",
    "Prep_Time": "6 hrs 40 mins",
    "Image_Link": "image/5.png"
  },
  {
    "Recipe_Name": "Prize-Winning Baby Back Ribs",
    "Recipe_URL": "https://www.allrecipes.com/recipe/14539/prize-winning-baby-back-ribs/",
    "Detailed_Ingredients": "1 tablespoon ground cumin, 1 tablespoon chili powder, 1 tablespoon paprika, salt and pepper to taste, 3 pounds baby back pork ribs, 1 cup barbeque sauce",
    "Instructions": "Make the spice rub, trim the ribs then season with the spice mix, cook the ribs on the grill according to the detailed recipe below, brush the grilled baby back ribs with barbecue sauce, grill for five more minutes, this grilled baby back rib recipe calls for a savory homemade spice rub made with cumin, chili powder, paprika, salt, and pepper, it should take about an hour to perfectly cook these baby back ribs on the grill, you’ll know the ribs are done when an instant read thermometer inserted into the center reads 145 degrees F (63 degrees C).",
    "Prep_Time": "1 hr 35 mins",
    "Image_Link": "image/6.png"
  },
  {
    "Recipe_Name": "Prime Rib - It's Easier Than You Think",
    "Recipe_URL": "https://www.allrecipes.com/recipe/230368/prime-rib-its-easier-than-you-think/",
    "Detailed_Ingredients": "1 (5 pound) bone in beef prime rib roast, 1 tablespoon olive oil, 2 teaspoons Montreal style steak seasoning (such as McCormick), 1 teaspoon chopped garlic, 1 teaspoon Italian seasoning, 1 teaspoon mustard powder",
    "Instructions": "Gather all ingredients, Place roast, bone-side down, onto a rack set in a roasting pan, Whisk olive oil, steak seasoning, garlic, Italian seasoning, and mustard powder together in a small bowl, Spread over roast; set aside until roast comes to room temperature, about 45 minutes. Preheat the oven to 450 degrees F (230 degrees C), Bake in the preheated oven for 20 minutes. Insert a meat thermometer into the thickest part of the roast, not touching the bone. Reduce the oven temperature to 325 degrees F (165 degrees C), Continue cooking until reaches desired degree of doneness, or an internal temperature of 145 degrees F (65 degrees C) for medium is reached, about 1 1/2 to 2 hours. Remove from the oven, cover with a doubled sheet of aluminum foil, and set aside to rest in a warm area before slicing, 10 to 15 minutes.",
    "Prep_Time": "2 hrs 55 mins",
    "Image_Link": "image/7.png"
  },
  {
    "Recipe_Name": "Pittsburgh Ham Barbecues",
    "Recipe_URL": "https://www.allrecipes.com/recipe/170741/pittsburgh-ham-barbecues/",
    "Detailed_Ingredients": "½ cup unsalted butter, 1 small onion finely chopped, 2 cups ketchup, ½ cup water, ⅓ cup distilled white vinegar, 3 tablespoons brown sugar, 2 tablespoons Worcestershire sauce, 2 teaspoons prepared yellow mustard, 1 ½ pounds chipped chopped ham, 8 kaiser rolls split, 1 cup pickle relish (Optional)",
    "Instructions": "Preheat the oven to 275 degrees F (135 degrees C). Melt butter in a large skillet over medium-high heat. Add onion; cook and stir until translucent, about 5 minutes. Stir in ketchup, water, vinegar, brown sugar, Worcestershire sauce, and mustard; simmer about 10 minutes. Stir in ham; cook until sauce is bubbling and ham is heated through, 5 to 7 minutes. Meanwhile, heat kaiser rolls in the preheated oven until toasted, 5 to 7 minutes. Divide ham mixture among toasted rolls; top with pickle relish. Serve hot.",
    "Prep_Time": "30 mins",
    "Image_Link": "image/8.png"
  },
  {
    "Recipe_Name": "Mother's Potato Salad",
    "Recipe_URL": "https://www.allrecipes.com/recipe/214709/mothers-potato-salad/",
    "Detailed_Ingredients": "5 pounds whole russet potatoes, 5 large eggs, 1 ½ cups mayonnaise (such as Hellman's), 2 tablespoons prepared yellow mustard (such as French's), 25 pimento-stuffed green olives, sliced, 7 sweet gherkins, chopped, 3 stalks celery, chopped, 1 small onion, chopped, 1 pinch salt, or to taste, 1 green bell pepper, sliced (Optional)",
    "Instructions": "Place potatoes in a large pot and cover with salted water; bring to a boil over high heat. Reduce heat to medium-low, cover, and simmer until tender, about 20 minutes. Drain potatoes; steam dry 1 to 2 minutes. Cool, then peel and cut into cubes. Place eggs in a saucepan in a single layer; cover with water by 1 inch. Cover the saucepan; bring to a boil over high heat, then remove from heat, and let eggs stand in hot water for 15 minutes. Remove eggs from hot water, cool eggs under cold running water. Peel and slice. Reserve 1 attractive slice for garnish. Combine mayonnaise and mustard in a bowl. Combine potatoes, eggs, olives, gherkins, celery, and onion in a separate large bowl. Add mayonnaise dressing; gently toss until ingredients coated. Season with salt. Top salad with bell pepper slices and reserved egg slice in the center. Chill until ready to serve",
    "Prep_Time": "2 hrs 35 mins",
    "Image_Link": "image/9.png"
  },
  {
    "Recipe_Name": "Chef John's Shepherd's Pie",
    "Recipe_URL": "https://www.allrecipes.com/recipe/219919/chef-johns-shepherds-pie/",
    "Detailed_Ingredients": "1¼ pounds Yukon Gold potatoes peeled and cubed, 3 cloves garlic halved, 1 pound lean ground beef, 2 tablespoons all purpose flour, 4 cups frozen mixed vegetables, ¾ cup beef broth, 3 tablespoons ketchup, 1 teaspoon salt, ½ teaspoon ground black pepper, ¾ cup light sour cream, ½ cup shredded Cheddar cheese divided",
    "Instructions": "Place cubed potatoes and garlic in a large pot with enough water to cover. Bring to a boil over high heat. Reduce heat to medium-low, cover, and simmer until tender, about 20 minutes. Preheat the oven to 375 degrees F (190 degrees C). Meanwhile, cook ground beef over medium heat in a skillet. Stir in flour, mixing with beef drippings. Add beef broth, ketchup, vegetables, salt, and pepper. Stir to combine. Cook until thick, about 5 minutes. Transfer beef mixture to an oven-proof casserole dish. Drain potatoes and smash them a little bit before adding 1/4 cup grated cheese and sour cream. Mash together until smooth. Top meat mixture with potatoes. Spread potatoes from the center of casserole to the edges to form top layer. Sprinkle with remaining 1/4 cup grated cheese. Bake in the preheated oven until cheese melts and turns golden, 20 to 25 minutes. Let cool 15 minutes before serving",
    "Prep_Time": "1 hr 25 mins",
    "Image_Link": "image/10.png"
  },
  {
    "Recipe_Name": "Easiest Applesauce Cake",
    "Recipe_URL": "https://www.allrecipes.com/recipe/27709/easiest-applesauce-cake/",
    "Detailed_Ingredients": "1 (18.25 ounce) package yellow cake mix, 1 (3.4 ounce) package instant vanilla pudding mix, ½ teaspoon ground nutmeg, ½ teaspoon ground cinnamon, 1 cup applesauce, ¼ cup vegetable oil, 4 eggs, ½ cup water",
    "Instructions": "Preheat the oven to 350 degrees F (180 degrees C). Grease and flour three 8x4-inch loaf pans. In a large bowl, stir together cake mix, instant pudding mix, nutmeg, and cinnamon. Add applesauce, oil, eggs, and water. Blend for 3 to 4 minutes using an electric mixer. Divide the batter evenly between the prepared pans. Bake for 50 to 55 minutes in the preheated oven, or until a toothpick inserted in the center comes out clean.",
    "Prep_Time": "1 hr",
    "Image_Link": "image/11.png"
  },
  {
    "Recipe_Name": "Apple Pie Filling",
    "Recipe_URL": "https://www.allrecipes.com/recipe/12681/apple-pie-filling/",
    "Detailed_Ingredients": "18 cups thinly sliced apples, 3 tablespoons lemon juice, 10 cups water, 4 ½ cups white sugar, 1 cup cornstarch, 2 teaspoons ground cinnamon, 1 teaspoon salt, ¼ teaspoon ground nutmeg",
    "Instructions": "Gather the ingredients. Place apples in a bowl. Toss apples with lemon juice in a large bowl and set aside. Pour water into a Dutch oven over medium heat. Combine sugar, cornstarch, cinnamon, salt, and nutmeg in a bowl; add to water, stir well, and bring to a boil. Boil for 2 minutes, constantly stirring. Add apples and return to a boil. Reduce heat, cover, and simmer until apples are tender, 6 to 8 minutes. Cool for 30 minutes. Ladle into 5 freezer containers, leaving ½ inch of headspace. Cool at room temperature no longer than 1½ hours. Seal and freeze. Can be stored for up to 12 months.",
    "Prep_Time": "2 hrs 40 mins",
    "Image_Link": "image/12.png"
  },
  {
    "Recipe_Name": "Rompope (Mexican Eggnog)",
    "Recipe_URL": "https://www.allrecipes.com/recipe/260832/rompope-mexican-eggnog/",
    "Detailed_Ingredients": "3 pints whole milk, 2 ½ cups white sugar, 2 cinnamon sticks, 15 egg yolks, 1 cup rum",
    "Instructions": "Bring milk, sugar, and cinnamon sticks to a boil in a large saucepan over low heat. Continue to boil, stirring constantly, until milk has reduced by a little more than one-third, about 20 minutes. Remove from the heat. Leave in the saucepan and allow to cool slightly, about 10 minutes. Beat egg yolks with an electric mixer until thick and pale. Mix in a little of the warm milk mixture. Pour egg yolk mixture into the saucepan with the remaining milk mixture. Stir to combine and bring to a boil over low heat. Stir constantly, scraping the bottom and sides, until mixture is thick enough to coat the back of a spoon, 5 to 7 minutes. Remove from the heat, remove cinnamon sticks, and cool to lukewarm, 15 to 30 minutes. Stir in rum and cool completely, about 2 hours",
    "Prep_Time": "3 hrs 15 mins",
    "Image_Link": "image/13.png"
  },
  {
    "Recipe_Name": "Best Baconless Spinach Salad Dressing",
    "Recipe_URL": "https://www.allrecipes.com/recipe/241756/best-baconless-spinach-salad-dressing/",
    "Detailed_Ingredients": "½ cup olive oil, 2 tablespoons white wine vinegar, 2 teaspoons honey Dijon mustard, 2 teaspoons grated red onion, 1 teaspoon sea salt, ½ teaspoon ground black pepper, ¼ teaspoon lemon juice, ⅓ cup white sugar, or more to taste",
    "Instructions": "Whisk olive oil, white wine vinegar, Dijon mustard, red onion, sea salt, black pepper, and lemon juice together in a microwave-safe bowl. Cook oil mixture in the microwave until hot and almost boiling, 1½ to 2 minutes. Gradually whisk sugar into hot mixture until dressing is thick and creamy.",
    "Prep_Time": "15 mins",
    "Image_Link": "image/14.png"
  },
  {
    "Recipe_Name": "Best Baked Potato Soup",
    "Recipe_URL": "https://www.allrecipes.com/recipe/25665/baked-potato-soup-v/",
    "Detailed_Ingredients": "9 baking potatoes, ⅔ cup butter, ⅔ cup all-purpose flour, 6 cups whole milk, ½ tablespoon salt, 1 teaspoon ground black pepper, ½ cup bacon bits, divided, 4 green onions, chopped, 10 ounces shredded Cheddar cheese, 1 (8 ounce) container sour cream",
    "Instructions": "Prick potatoes with a fork and cook in the microwave, 3 or 4 at a time, until fork-tender, about 7 to 8 minutes. When cool enough to handle, scoop out the flesh. Melt butter in a large saucepan over medium heat; stir in flour and cook until well combined, about a minute. Whisk in milk, a little at a time, stirring constantly until thickened. Stir in cooked potatoes, salt, pepper, 1/3 cup bacon bits, 2 tablespoons green onions and most of the cheese. Cook until thoroughly heated. Stir in sour cream and heat through. Serve topped with remaining bacon, onions and cheese",
    "Prep_Time": "1 hr 15 mins",
    "Image_Link": "image/15.png"
  },
  {
    "Recipe_Name": "Quick and Easy Vegetable Soup",
    "Recipe_URL": "https://www.allrecipes.com/recipe/13338/quick-and-easy-vegetable-soup/",
    "Detailed_Ingredients": "1 (14.5 ounce) can diced tomatoes, 1 (14 ounce) can chicken broth, 1 (11.5 ounce) can tomato-vegetable juice cocktail, 2 carrots, sliced, 2 stalks celery, diced, 1 large potato, diced, 1 cup chopped fresh green beans, 1 cup fresh corn kernels, 1 cup water, salt and pepper to taste, 1 pinch Creole seasoning, or more to taste",
    "Instructions": "Gather all ingredients. Combine tomatoes, chicken broth, tomato juice, carrots, celery, potato, green beans, corn, and water in a large stockpot. Season with salt, pepper, and Creole seasoning. Bring to a boil over medium heat and simmer until vegetables are tender, about 30 minutes. Serve hot and enjoy",
    "Prep_Time": "50 mins",
    "Image_Link": "image/16.png"
  },
  {
    "Recipe_Name": "Hamburger Soup",
    "Recipe_URL": "https://www.allrecipes.com/recipe/12921/hamburger-soup-i/",
    "Detailed_Ingredients": "1 pound lean ground beef, 5 cups water, 1 (16 ounce) can diced tomatoes, 1 (10 ounce) package frozen corn kernels, 1 (8 ounce) can tomato sauce, 1 cup chopped carrots, 1 cup chopped celery, 1 cup chopped onion, 6 beef bouillon cubes, 3 tablespoons ketchup, 1 teaspoon dried basil, 1 teaspoon salt",
    "Instructions": "Gather all ingredients. Heat a large skillet over medium-high heat. Cook and stir ground beef in the hot skillet until browned and crumbly, 5 to 7 minutes. Drain and discard grease.Combine beef, water, tomatoes, corn, tomato sauce, carrots, celery, onion, bouillon, ketchup, basil, and salt in a large stockpot; bring to a boil. Reduce heat and simmer for at least 1 ½ hours.",
    "Prep_Time": "1 hr 50 mins",
    "Image_Link": "image/17.png"
  },
  {
    "Recipe_Name": "Breakfast Casserole",
    "Recipe_URL": "https://www.allrecipes.com/recipe/172671/breakfast-sausage-casserole/",
    "Detailed_Ingredients": "1 pound breakfast sausage, 6 eggs, 2½ cups milk, divided, ¾ teaspoon dry mustard powder, ½ teaspoon salt, 8 slices bread, cubed, 4 cups shredded Cheddar cheese, 1 (10.5 ounce) can condensed cream of mushroom soup",
    "Instructions": "Grease a 9x13-inch baking dish. Cook sausage in a large skillet over medium-high heat until evenly browned, crumbly, and no longer pink in the center, 7 to 9 minutes. Drain and discard any excess grease. While the sausage is cooking, whisk eggs in a mixing bowl until smooth. Whisk in 2 cups milk, mustard powder, and salt until evenly blended. Spread bread cubes into the prepared dish; sprinkle sausage over top, then Cheddar cheese. Pour egg mixture over the entire dish. Cover and refrigerate, 8 hours to overnight. When ready to bake, preheat the oven to 300 degrees F (150 degrees C). Remove casserole from the refrigerator and uncover. Whisk condensed soup and remaining ½ cup milk together in a bowl; pour mixture over casserole. Bake in the preheated oven until firm and golden brown, about 1½ hours",
    "Prep_Time": "10 hrs",
    "Image_Link": "image/18.png"
  },
  {
    "Recipe_Name": "Chili Soup",
    "Recipe_URL": "https://www.allrecipes.com/recipe/15914/chili-soup/",
    "Detailed_Ingredients": "3 pounds ground beef 1 ½ cups chopped onion 8 cups tomato juice 4 (15 ounce) cans kidney beans 4 (10.75 ounce) cans condensed tomato soup 2 large potatoes, cubed 3 teaspoons chili powder 8 cups water 1/8 teaspoon salt, or to taste",
    "Instructions": "Combine ground beef and onions in a large pot over medium heat; cook and stir until meat is browned and crumbly, about 5 minutes. Drain excess fat. Add tomato juice, beans, tomato soup, potatoes, and chili powder. Stir in water and salt. Bring to a boil, then reduce heat to low and simmer until potatoes are tender and soup has thickened, about 1 hour",
    "Prep_Time": "1 hr 15 mins",
    "Image_Link": "image/19.png"
  },
  {
    "Recipe_Name": "Dad's Basic Moist Pork Roast",
    "Recipe_URL": "https://www.allrecipes.com/recipe/233620/dads-basic-moist-pork-roast/",
    "Detailed_Ingredients": "2 tablespoons olive oil, 1 tablespoon ground black pepper, 1 teaspoon kosher salt, 1 (3 pound) boneless top loin pork roast",
    "Instructions": "Combine oil, pepper, and salt in a bowl; rub oil mixture over pork and refrigerate while the oven preheats. Preheat the oven to 475 degrees F (245 degrees C). Place pork on a roasting rack set in a large roasting pan. Roast in the preheated oven for 30 minutes. Remove pork from the oven and reduce the heat to 325 degrees F (165 degrees C). Insert an instant-read thermometer into the thickest part of the center. The temperature will range from 80 to 110 degrees F (27 to 43 degrees C). Allow pork to rest uncovered at room temperature until the internal temperature reaches between 115 and 140 degrees F (46 and 60 degrees C), about 30 minutes. Return to oven and continue to cook until internal temperature reaches 145 degrees F (63 degrees C), 15 to 30 minutes more. Let the roast stand uncovered at room temperature for 15 to 20 minutes before slicing and serving",
    "Prep_Time": "1 hr 40 mins",
    "Image_Link": "image/20.png"
  },
  {
    "Recipe_Name": "Quick and Easy Hamburger Stroganoff",
    "Recipe_URL": "https://www.allrecipes.com/recipe/240773/quick-and-easy-hamburger-stroganoff/",
    "Detailed_Ingredients": "1 (16 ounce) package egg noodles, 2 tablespoons butter, 1 onion, chopped, 1 pound ground beef, 1 tablespoon all-purpose flour, 1 (4.5 ounce) can sliced mushrooms, drained (Optional), 1 tablespoon garlic salt, or to taste, 1 (10.5 ounce) can cream of mushroom soup, 1 (10.5 ounce) can cream of chicken soup, 1 cup sour cream",
    "Instructions": "Gather all ingredients. Fill a large pot with lightly salted water and bring to a rapid boil. Cook egg noodles at a boil until tender yet firm to the bite, 7 to 9 minutes; drain. Meanwhile, melt butter in a large skillet over medium-high heat. Sauté onion in hot butter until tender and translucent, about 5 minutes. Add ground beef in small chunks; cook and stir beef until browned and crumbly, 5 to 7 minutes. Sprinkle flour over beef mixture; cook and stir for 1 minute. Stir in mushrooms and garlic salt. Pour in mushroom soup and chicken soup; cook and stir until heated through, about 5 minutes. Stir in sour cream until smooth and heated through, 2 to 3 minutes more. Serve beef mixture over cooked egg noodles",
    "Prep_Time": "30 mins",
    "Image_Link": "image/21.png"
  },
  {
    "Recipe_Name": "Simple Hamburger Stroganoff",
    "Recipe_URL": "https://www.allrecipes.com/recipe/23260/simple-hamburger-stroganoff/",
    "Detailed_Ingredients": "1 (16 ounce) package egg noodles, 1 pound lean ground beef, 1 (8 ounce) package cream cheese, cut into pieces, 1 (6 ounce) can chopped mushrooms, with liquid, 1 (.75 ounce) packet dry brown gravy mix, 2 (10.5 ounce) cans condensed cream of mushroom soup, 1 (8 ounce) container sour cream, ½ cup milk",
    "Instructions": "Fill a large pot with lightly salted water and bring to a rapid boil. Cook egg noodles at a boil until tender yet firm to the bite, 7 to 9 minutes. Drain. Meanwhile, cook ground beef in a large skillet over medium-high heat, stirring occasionally, until browned and crumbly, 5 to 7 minutes; drain and discard grease. Stir in cream cheese, mushrooms with liquid, and gravy mix; cook and stir over medium heat until cream cheese melts, 2 to 3 minutes. Add condensed soup, sour cream, and milk; cook, stirring occasionally, until smooth and creamy, 3 to 5 minutes. Drain egg noodles; stir into the beef mixture. Cook until heated through, 2 to 3 minutes",
    "Prep_Time": "20 mins",
    "Image_Link": "image/22.png"
  },
  {
    "Recipe_Name": "Chocolate Crinkle Cookies",
    "Recipe_URL": "https://www.allrecipes.com/recipe/9861/chocolate-crinkles-ii/",
    "Detailed_Ingredients": "2 cups white sugar, 1 cup unsweetened cocoa powder, ½ cup vegetable oil, 4 large eggs, 2 teaspoons vanilla extract, 2 cups all-purpose flour, 2 teaspoons baking powder, ½ teaspoon salt, ½ cup confectioners' sugar",
    "Instructions": "Gather ingredients. Mix sugar, cocoa, and oil together in a medium bowl. Beat in eggs, one at a time, until combined. Stir in vanilla. Combine flour, baking powder, and salt in another bowl. Gradually stir flour mixture into the cocoa mixture until thoroughly mixed. Cover dough and refrigerate for at least 4 hours. Preheat the oven to 350 degrees F (175 degrees C). Line two cookie sheets with parchment paper. Roll or scoop chilled dough into 1-inch balls. Coat each ball in confectioners' sugar and place 1 inch apart on the prepared cookie sheets. Bake in the preheated oven for 10 to 12 minutes. Let stand on the cookie sheet for a few minutes before transferring to wire racks to cool. Repeat Steps 4 and 5 to make remaining batches.",
    "Prep_Time": "5 hrs",
    "Image_Link": "image/23.png"
  },
  {
    "Recipe_Name": "Apple Dump Cake",
    "Recipe_URL": "https://www.allrecipes.com/recipe/244777/apple-pie-cake-mix-cake/",
    "Detailed_Ingredients": "2 (21 ounce) cans apple pie filling, 1 (15.25 ounce) package yellow cake mix, ½ cup butter, melted",
    "Instructions": "Gather the ingredients. Preheat the oven to 350 degrees F (175 degrees C). Pour pie filling into a 9x13-inch baking dish. Sprinkle cake mix evenly over apple pie filling and top with melted butter. Bake in the preheated oven until the top starts to turn brown, about 40 minutes. Cool cake 15 minutes before serving. Serve and enjoy",
    "Prep_Time": "1 hr",
    "Image_Link": "image/24.png"
  },
  {
    "Recipe_Name": "Easy Stuffed Pepper Soup",
    "Recipe_URL": "https://www.allrecipes.com/recipe/13182/stuffed-pepper-soup-i/",
    "Detailed_Ingredients": "2 pounds ground beef, 1 green bell pepper, chopped, 1 (29 ounce) can tomato sauce, 1 (29 ounce) can diced tomatoes, 2 cubes beef bouillon cube, ¼ cup packed brown sugar, 2 teaspoons salt, 1 teaspoon ground black pepper, 1 tablespoon soy sauce, 2 cups cooked white rice",
    "Instructions": "Brown beef in a Dutch oven over medium high heat until browned; drain off any fat. Add green pepper and saute for 3 minutes. Stir in tomato sauce, diced tomatoes with juice, bouillon cubes, brown sugar, salt, black pepper, and soy sauce. Reduce heat to low, cover and simmer for 30 to 45 minutes. Stir in rice and heat through",
    "Prep_Time": "40 mins",
    "Image_Link": "image/25.png"
  },
  {
    "Recipe_Name": "Stuffed Pepper Soup",
    "Recipe_URL": "https://www.allrecipes.com/recipe/13378/stuffed-pepper-soup-iv/",
    "Detailed_Ingredients": "1 pound ground sirloin, 1 green bell pepper, chopped, 1 cup finely diced onion, 1 (29 ounce) can diced tomatoes, 1 (15 ounce) can tomato sauce, 1 (14 ounce) can chicken broth, ¼ teaspoon dried thyme, ¼ teaspoon dried sage, salt and pepper to taste, 2 cups water, 1 cup white rice",
    "Instructions": "Gather all ingredients. Heat a large skillet over medium-high heat. Cook and stir ground beef in the hot skillet until browned and crumbly, 5 to 7 minutes. Drain and discard grease. Add green pepper and onion; cook and stir until onion has softened and turned translucent, about 5 minutes. Add tomatoes, tomato sauce, broth, thyme, and sage; season with salt and pepper. Cover and simmer until peppers are tender, about 30 to 45 minutes. Meanwhile, bring water and rice to a boil in a saucepan. Reduce heat to medium-low, cover, and simmer until rice is tender and water has been absorbed, 20 to 25 minutes. Stir cooked rice into soup; heat through and serve",
    "Prep_Time": "1 hr",
    "Image_Link": "image/26.png"
  },
  {
    "Recipe_Name": "Cream of Mushroom Soup",
    "Recipe_URL": "https://www.allrecipes.com/recipe/13096/cream-of-mushroom-soup-i/",
    "Detailed_Ingredients": "5 cups sliced fresh mushrooms, 1½ cups chicken stock, ½ cup chopped onion, ⅛ teaspoon dried thyme, 3 tablespoons butter, 3 tablespoons all-purpose flour, ¼ teaspoon salt, ¼ teaspoon ground black pepper, 1 cup half-and-half or heavy cream, 1 tablespoon sherry",
    "Instructions": "Gather all ingredients. Simmer mushrooms, stock, onion, and thyme in a large heavy saucepan until vegetables are tender, 10 to 15 minutes. Carefully transfer the hot mixture to a blender or food processor. Cover and hold lid down with a potholder; pulse until creamy but still with some chunks of vegetable. Melt butter in the same saucepan. Whisk in flour until smooth. Whisk in salt and pepper. Slowly whisk in half-and-half and mushroom mixture. Bring soup to a boil and cook, stirring constantly, until thickened. Stir in sherry. Taste and season with more salt and pepper if needed.",
    "Prep_Time": "50 mins",
    "Image_Link": "image/27.png"
  }
]

'''
)
#Initialize the model
MODEL = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config=GENERATION_CONFIG,
    system_instruction=SYSTEM_INSTRUCTION,
)
GLOBAL_CHAT_SESSION = MODEL.start_chat(history=[])

app = Flask(__name__)
CORS(app) 

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Handles POST requests from the web front-end."""
    try:
        data = request.get_json()
        user_input = data.get('message')

        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        response = GLOBAL_CHAT_SESSION.send_message(user_input)
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"Server-side Error: {e}") 
        return jsonify({"error": "Internal server error - check API key and server log."}), 500

def start_cli_chat():
    """Starts the chat interface directly in the terminal (for debugging)."""
    cli_chat_session = MODEL.start_chat(history=[]) 

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Chef Bot: Bon Appétit! See you later! 👋")
            break
        if not user_input.strip():
            continue

        try:
            print("Chef is thinking...", end="\r")
            response = cli_chat_session.send_message(user_input)
            print(f"Chef Bot: {response.text}")
        except Exception as e:
            print(f"\n Error: {e}")
            print("Check your API Key or internet connection.")

if __name__ == '__main__':
    
    if "--cli" in sys.argv:
        start_cli_chat()
    else:
        print("Starting Flask web server...")
        app.run(debug=True, port=5000)