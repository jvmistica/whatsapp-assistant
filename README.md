# WhatsApp Assistant

A WhatsApp contact that assists you in taking down notes, recipes, and managing inventory items. This was initially created to minimize food waste by asking it, "What can I make?" It will return a list of recipes for food that you can make based on the items you currently have.

## Getting Started

Install the required modules:
```
pip install -r requirements.txt
```
\
Setup the database:
1. **Create an SQL instance** by logging into Google Cloud Platform and navigating to Storage > SQL.
2. Click "Create Instance" > "Choose MySQL" and fill up the details for the instance.
3. **Create a database** by clicking "Databases" > "Create database" under your SQL instance.
4. Fill up the details and click "Create"
5. Change the details in the modules/config.py file:
```
DB_USER="db_user"
DB_PASS="db_pass"
DB_NAME="db_name"
CLOUD_SQL_CONNECTION_NAME="sql_conn_name"
```
\
Deploy to Google App Engine:
```
gcloud app deploy
```

## Commands

### Show a list of records
Show notes.\
Show items.\
Show recipes.

### Show a specific record
Show note: \<Note title>\
Show item: \<Item name>\
Show recipe: \<Recipe name>

### Notes
New note: \<Message>\
Delete note: \<Note title>\
Edit note: \<Note title> -> \<New content>

### Items
New item: \<Item name>\
Delete item: \<Item name>\
Edit item: \<Item name> -> \<New item name>

### Recipes
New recipe: \<Recipe name>; <Recipe Ingredients>\
Delete recipe: \<Recipe name>\
Edit recipe: \<Recipe name> -> \<New recipe ingredients>
