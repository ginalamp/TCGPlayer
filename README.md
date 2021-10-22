# GET MTG
TCGPlayer is, in part, an online store for the resale of trading card game (TCG) cards. This project involved creating a beta store for TCGPlayer whereby sellers can upload cards to sell, and buyers can buy cards. We rebranded the store to "GET MTG", as the project uses data from the TCG brand "Magic: The Gathering" (MTG), and our founding members are Gina, Emma, and Tristan.

## Group members
* Gina Lamprecht (21773513)
* Emma Raaff (21861234)
* Tristan Luyt (21670897)
## Usage
### Set up virtual environment & requirements

```
python3 -m virtualenv env
source env/bin/activate
pip3 install -r requirements.txt
```

### Set up database
Before completing the next steps, unzip the `all-cards-20211014091110-sample.zip` file in `src/`.

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


## Our Tech Stack
* Django
* Python
* HTML
* JavaScript
* CSS (particularly Bootstrap)
## Functionality
A user can register a profile with a username, email and password. From here, they can browse the "Card" page, which provides an extensive collection of MTG cards. From this page, users can select a card to view information about that card. This information includes particularly:
* Price
* Brand
* Rarity
Additional information includes:
* Release date
* Type
* Popularity ranking
* Mana cost
* Converted mana cost (CMC)
* Power
* Toughness

A user can upload cards for sale. This is done by clicking on a specific card and adding a listing for that card. The seller sets their desired price, and this price is linked to the rest of the relevant information about that card stored in the database via the administrative system.

If a seller wishes to purchase a particular card, they can navigate to the listings page and contact the seller of the card they would like to purchase. The seller and buyer then communicate off of the GET MTG site to discuss payment arrangements.

In order to provide buyers with the best price, card listings for a particular card are sorted from least expensive to most expensive. Users can also purchase multiple cards in one session by adding the cards to a cart.

A basic Business Intelligencec report is also available to users with Administrator privileges, allowing them to access data reporting on important metrics.
