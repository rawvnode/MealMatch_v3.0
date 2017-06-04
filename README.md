# MealMatch_v3.0

Welcome to MealMatch by Endless!

This repo consists of three folders that need to be addressed; “JSON”, “Scrapy crawler” and “MealMatch”.
 
The JSON folder contains all the information that the team gathered with the use of the web crawlers developed. There are two files, one that contains ingredients, and one that contains recipes. 
 
As said these JSON files were created through crawling the web for ingredients and recipes. This was done with the use of the python framework Scrapy. Within Scrapy, you can create a project. This project is in the Scrapy crawler folder and has the name “tutorial”. Inside this folder are the so called spiders. These are the ones that goes through the predetermined websites for information specified by its creator/s. 
 
Both of these previously mentioned folders are separated from the actual project in the sense that they are deployed entirely on their own, and then manually integrated with the databases. The main folder for the project however is the one called MealMatch. When opening this folder you see a number of subfolders. In the subfolder with the same name, MealMatch, you will find the root views and urls as well as the settings.py file where the Django settings can be changed. 
When going back one step to the root folder MealMatch you find several other important subfolders. First there is MapReduce, which contains the code for mapping recipes against ingredients, and storing them in the Mongo database. Then you have two applications within Django; recipes and account_functions. recipes contains the code that has to do with every page that are associated with the recipes, that is the startpage, result page etc. Here you have the views, urls and models that are the foundation of this application, as well as the Django forms that are used within. The account_functions applications has the same structure, but contains code that are related to all pages that handles account functions, as the name says. 
 
In the static folder you find all the JavaScript and CSS code as well as all media including images and a video. 
 
The last important folder here is the Templates folder. This contains all the HTML code that the system are built upon. In the root you have all the pages related to the recipe application. You then have a subfolder for the templates involved in the account_funtions application. Other than this you have the registration folder inside Templates. This is a application itself, but its models, view and such are built in in Django, and only extends it. These templates are all related to the pages where you create your user, handles passwords and login in and out of the system.

