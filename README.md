# supreme-bot

Fully functioning start to end supreme bot built with python using the BS4 and Selenium packages.

## Getting Started

Follow these steps to get the project up and running on your local computer.

### Prerequisites

You will need Python 3 installed on your computer, dependencies include BS4, selenium, time, and requests.

The web driver that is currently being used is for chrome, but this can be easily swapped out.

### Installing

First install Beautiful Soup 4

```
pip install beautifulsoup4
```

Next install selenium

```
pip install -U selenium
```

Follow installation and setup steps for tthe chrome web driver here http://chromedriver.chromium.org/getting-started

Naviagate to the folder location run the script

```
python supreme_bot_script.py
```

This will prompt you to enter the preview url ( which can be found at https://www.supremenewyork.com ) the size and color of the product.

Finally it will open up a chrome page and will output all info up to the captcha at that point the user must fill out the captcha manually, after that the order will be placed, there may be one more confirmation that the user must manually do depending on the season / site updates.
