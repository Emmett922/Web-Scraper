# eCommerce Web Scraper (v.1.0)

This project is a web scraping application intended to strengthen my development skills by practicing on websites specifically built for web scraping. More specifically, this program is designed to scrape the 20 pages worth of laptop data from the [*webscraper.io*](https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops) test site.

## Project Structure

The main components of this application are:

- **Frontend UI**: Built with React, the main logic is found in the [`App.js`](https://github.com/Emmett922/eCommerce-Web-Scraper/blob/main/frontend/src/App.js) file.
- **Backend**: Handled by Python, with two key files:
  - [`server.py`](https://github.com/Emmett922/eCommerce-Web-Scraper/blob/main/backend/server.py): Manages the Flask server and the API endpoints.
  - [`web_scraper_io_scraper.py`](https://github.com/Emmett922/eCommerce-Web-Scraper/blob/main/backend/web_scraper_io_scraper.py): Contains the web scraping logic using Playwright and Selectolax.

## Current Functionality

In this version (v.1.0), the web application features:
- A single button to initiate the scraping process.
- A display section for the laptop data that is gathered from the test site.

## Future Plans

In version 2 (v.2.0), I plan to:
- Develop a more polished UI with an improved visual structure.
- Enhance status messages for better user feedback.
- Implement functionality to download the scraped data as a `.csv` file or send it to a Google Sheets document.
- Introduce a database for storing scraped data, despite the current static nature of the test site, to demonstrate a fully functioning and connected application.

Stay tuned for more updates as I continue to develop and refine this project!
