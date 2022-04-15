# Flipkart Mobile Revies scraper

This is a spider to scrap the Samsung mobile reviews from `Flipkart` site. Build using `scrapy` python package

## Features
It extracts the following:

  * Product Name
  * Product Price
  * Product title
  * Product review
  * Product rating
  * Product likes
  * Product dislikes

## Setup

Install required packages (scrapy)

```sh
pip install -r requirements.txt
```

## Execute Flipkart Scraper

### For Windows users
```sh
run.bat
```

### For Linux or Mac users
```sh
sh ./run.sh
```

### Or can run the following command
```bash
scrapy crawl flipkart_scraper -O ./data/data.json  # Overwrites the data.json file

scrapy crawl flipkart_scraper -o ./data/data.json  # Appends to the data.json file
```

It will create `data.json` file inside the `data` folder containing all the scraped data in `JSON` format

# Sample Data
Already fetched sample data is available in `data` folder


# Troubleshooting
If `data.json` file doesn't generate in proper format then just delete `data.json` file
