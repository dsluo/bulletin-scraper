# Bulletin Scraper

Scrape's UGA's [Bulletin website](http://bulletin.uga.edu/CoursesHome.aspx) for all course info and puts it into a nice JSON formatted file.

## To Run

* Install dependencies (preferably in a virtual environment).
    ```
    pip install -r requirements.txt
    ```
* Change directory into the Bulletin directory (the one with `scrapy.cfg`, not the project directory).
    ```
    cd bulletin
    ```
* Run
    ```
    scrapy crawl bulletin -o courses.json
    ```