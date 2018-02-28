import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Product:

    # sets product name
    def set_product_name(self):
        # grabs preview page url and gets text from it
        page = requests.get(self.initial_url)
        page_data = page.text

        soup = BeautifulSoup(page_data, 'html.parser')

        #sets the product name equal to the information from preview page
        return str(soup.find('div', class_='description').div.h2.text)

    # sets product category for use in the product url
    def set_product_category(self):
        # splits string by 5th slash which will always output correct category
        return str(self.initial_url.split('/')[5])

    # sets produt url
    def set_product_url(self):
        category_url = 'http://www.supremenewyork.com/shop/all/' + str(self.category)

        page = requests.get(category_url)
        page_data = page.text

        soup = BeautifulSoup(page_data, 'html.parser')

        # gets array of a tags with the product name and an array of a tags with product color
        items_of_same_name = soup.find_all('a', string=self.name)
        items_of_same_color = soup.find_all('a', string=self.color)

        # runs all hrefs together to get a matching pair
        for product in items_of_same_name:
            for color in items_of_same_color:
                if product['href'] == color['href']:
                    return 'http://www.supremenewyork.com' + product['href']

        # if not returns first product with the name
        return 'http://www.supremenewyork.com' + items_of_same_name[0]['href']

    # inits all values of the product
    def __init__(self, initial_url, color):
        self.initial_url = initial_url
        self.color = color
        self.name = self.set_product_name()
        self.category = self.set_product_category()
        self.url = self.set_product_url()

class SupremeBot:

    def main():
        initial_url = 'http://www.supremenewyork.com/previews/springsummer2018/bags/backpack'
        color = 'Black'

        # inits current product object
        product = Product(initial_url, color)

        print(product.url)

        # inits selenium chrome web driver
        driver = webdriver.Chrome()

        driver.get(product.url)
        # makes assertion that driver opened right page
        assert product.name in driver.title

        # finds and clicks add ot cart button
        add_to_cart_btn = driver.find_element_by_xpath("//input[@value='add to cart']")
        add_to_cart_btn.click()

        # waits until checkout is visible then clicks
        try:
            checkout_ready = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, 'checkout'))
            )
        finally:
            check_out_btn = driver.find_element_by_xpath("//a[@class='button checkout']")
            check_out_btn.click()

        time.sleep(5000)

    if __name__ == '__main__':
        main()
