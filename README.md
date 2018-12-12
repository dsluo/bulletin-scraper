# Bulletin Scraper

Scrape's UGA's [Bulletin website](http://bulletin.uga.edu/CoursesHome.aspx) for all course info and puts it into a nice 
JSON formatted file.

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

## Note about the data

Courses are listed multiple times if they are transdisciplinary (once for each discipline). E.g. for `Introduction to 
Quantum Computation`, listed as `CSCI(MATH)(PHYS) 4612/6612`, it will be listed once under `CSCI`, once under `MATH`, 
and once under `PHYS`.