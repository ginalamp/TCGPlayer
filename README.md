# GET MTG
TCGPlayer is, in part, an online store for the resale of trading card game (TCG) cards. This project involved creating a beta store for TCGPlayer whereby sellers can upload cards to sell, and buyers can buy cards. We rebranded the store to "GET MTG", as the project uses data from the TCG brand "Magic: The Gathering" (MTG), and our founding members are Gina, Emma, and Tristan.

## Group members
* Gina Lamprecht (21773513)
* Emma Raaff (21861234)
* Tristan Luyt (21670897)

## Demo
Click [here](https://drive.google.com/file/d/1YcBK3_sBxkBAr26zCSs9GfymE5gvsq44/view?usp=sharing) to see a basic demo of the website.

## Usage
### Set up virtual environment & requirements

```
python3 -m virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```

### Set up database
Before completing the next steps, unzip the `all-cards-20211014091110-sample.zip` file in `src/`. This data was retrieved from [Scryfall](https://scryfall.com/docs/api/bulk-data) on the 14th of October 2021, and can be replaced with a newer version downloaded from the website (just remember to update the file path argument shown below if you do this).

Then migrate the models.
```
cd src
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell
```
Import the data to the database in your python shell.
```python
from tcgplaya import utils
utils.parse_bulk_data("all-cards-20211014091110-sample.json")
```

### Run server
Exit the shell and then run the server.

```
python3 manage.py runserver
```

This will direct you to the home page:

<img width="700" alt="image" src="https://user-images.githubusercontent.com/48590328/138441848-1113bfb4-df47-4c94-8531-1c53552f1bf4.png">

## Functionality

### Login & Registration (user authentication)
The user is directed to registration if they are not logged in and try to access functionality that is only available to logged in users (Cart, My Listings, Profile, Card - add card listing, Card Listing - add to cart)

### Cards (home page)
* view first ~100 cards from the database
* search for card names (searches entire database and displays any card that contains the searched word)
* view particular card
  - view card details (clicking on 'more information' shows additional information other than the oracle text, set, and rarity if available)
  - view card listings for that card (sorted in ascending order according to price to allow the buyer to pick the cheapest one to add to their cart). When the card listing is clicked, it directs the user to that particular card listing page.
  - add new card listing. The user can choose the card price (default suggested price is the usd price in the database if there is one).
   
### Marketplace
* view card listings from the database
* search for card listings (searches entire database and displays any card listing that contains the searched word)
* view particular card listing
  - view card listing details (seller information, price, some card information). Clicking on the card directs the user to that individual card page.
  - add/remove from cart (if the user is not the seller). This toggles based on whether the card listing is already in the user's cart or not. Clicking the button directs the user to their updated cart.
  - delete card listing (if the user is the seller). Clicking this button directs the user to the Marketplace
     
### Cart
* view card listings that have been added to the user's cart
* view particular card listing (directs them to the functionality described above)

### My Listings
* view card listings that the user has listed (i.e. for which they are the seller)
* view particular card listing (directs them to the functionality described above)
 
### Profile
* view username and email
* update username and email (updates when the 'Save Changes' button is clicked)
* change password (enter current and new password)
* logout (directs to login page)
 
### Admin
Admin (created through Django's `python3 manage.py createsuperuser`) has access to a platform where they have CRUD privileges for all of the above as well as seeing important metrics (such as how many users, cards, card listings, etc. there are). They can log in by going to `localhost:8000/admin`.

## Our Tech Stack

<img width="500" alt="image" src="https://user-images.githubusercontent.com/48590328/138437524-69e3e7d2-3e40-4457-a78c-7f9e965d843d.png">
