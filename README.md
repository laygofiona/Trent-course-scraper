# Trent Course Scraper

This repo contains two Python scripts that scrape Trent University's Academic timetable (https://my.trentu.ca/portal/applications/timetable/public/landing.php) and undergraduate programs webpage (https://www.trentu.ca/futurestudents/undergraduate/programs). The scripts are made with Selenium WebDriver. Running each script outputs a .txt file that contains the respective information. 

### Installing Selenium
#### In the terminal run one of the following:
```pip install selenium```

``` pip3 install selenium```

``` python3 -m pip install selenium```

### Running degree_names.py

#### In the terminal
```python3 degree_names.py```

This script creates a programs.txt file containing an updated list of all degree programs offered at Trent.

### Running main.py

#### In the terminal
```python3 main.py currentYear ```

example:

```python3 main.py 2024 ```

This script creates two .txt files: courses.txt and faculty.txt. courses.txt contains a list of all courses offered throughout the current academic year in each department. faculty.txt contains a list of all the professors in each department. 


