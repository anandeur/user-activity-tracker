## User Activity Tracker

Inventory is an integral part of our POS system. We have items which in turn have multiple variants under it. For example it could be a blue T-Shirts which are available in multiple sizes (S, M, L) etc. A variant can have multiple such properties (Sizes, Cloth Type etc). The prices and the other properties are defined on a variant. We'd like to track every user action that changes the attributes of an item or its variants.
·  Item
o Attributes
§ Name
§ Brand
§ Category
§ Product Code (Barcode)
·         Variant
o    Attributes
§  Name
§  Selling Price
§  Cost Price
§  Properties - (Size:L, Cloth:Cotton)
§  Quantity
§  Think of them as filterable options on an ecommerce site.
o Eg:
§ Item  - Cotton Shirt
§ Variant - L (option - size : value - L)
§ Variant - XL (option - size : value - XL)
§ Variant - XXL (option - size : value - XXL)
·  A user can edit the attributes of an Item, its variants, and add new variant properties if needed.
·  The item is part of a branch which in turn is part to a store.
·  User Actions
o Edit Variant properties like variant name, selling price, cost price, quantity etc.
o Edit item properties like the name, brand, category etc.
o Add/Delete variants from an item.
 
User Actions to be logged on editing/modifiying/creating or deleting the attributes below.
·  Variant
o Cost Price
o Selling Price
o Variant Name
o Quantity
o Changing properties.
·  Item
o Name
o Brand
o Category
o Adding/Deleting Variant
 
The log will have to be surfaced as a notification feed like the one on facebook. Eg, John edited selling price, cost price of item X. John edited the selling price of items X,Y and Z. The user might make multiple edits on an item or edit the same attribute on multiple items. These actions will have to be grouped by user and by time whenever possible.
 
Build an API endpoint that takes the time range and  optionally the user id and outputs the user activity feed. If a user id is not passed it shows the activity log of all users. Actual screenshot are attached below. Only the fields mentioned above have to be implemented.


## Usage

- Clone the project and move to current working directory.
- Install the required packages using requirements.txt file by the command ```pip install -r requirements.txt```
- Run server by using ```python app.py```


## Requirements
- Python 3.x.x
- Flask
- Flask-SQLAlchemy