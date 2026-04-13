# ITparser

Asynchronous web parser for collecting structured data from IT‑related websites.  
The parser reads a list of page URLs from the configuration, extracts item links, scrapes each item page, and stores the results in an SQLite database.

## Features

- **Asynchronous** crawling using `asyncio` for high performance
- Configurable **log levels**, output file, and format
- SQLite storage with automatic table creation
- Graceful error handling and fatal error logging

## Installation

1. Clone the repository:
   git clone https://github.com/RusBoh/ITparser.git
   cd ITparser
2. Install dependencies:
   pip install -r requirements.txt

## Usage

Run the parser from the project root:
   python src/main.py

## What happens during execution

1. Logger initialisation – logs to console and file.
2. Database connection – creates db file if it doesn’t exist.
3. Table setup – drops the items table (if exists) and recreates it with columns url and title.
4. Page scraping – asynchronously fetches all pages listed in config.PAGES_LIST.
5. Link extraction – collects all item links from the pages and removes duplicates.
6. Item scraping – asynchronously fetches each item page and extracts (url, title).
7. Database insertion – saves each item to the items table.
8. Cleanup – commits changes and closes the database connection.