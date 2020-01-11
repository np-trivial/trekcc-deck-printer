# trekcc-deck-printer
Python script to download all the images for a deck from trekcc.org for use on DriveThruCards.com (or other card printing sites)

## Usage:
`python.exe .\trekcc-deck-printer.py <decklist URL>`

For example:

`python.exe .\trekcc-deck-printer.py "https://www.trekcc.org/decklists/index.php?mode=view&deckID=12525"`

_trekcc-deck-printer_ will create a directory based on the title of that deck, and put all the necessary images in that directory. If a deck requires multiple copies of a card, it will create that many copies. This simplifies the upload to a card printing site, so that you need not manually change the quantity of any cards.