import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

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

    def set_item_cookie(self):
        page = requests.get(self.url)
        page_data = page.text
        
        soup = BeautifulSoup(page_data, 'html.parser')

        cookie_val = soup.find('input', {'id': 'st'})['value']
        return cookie_val

    def set_size_cookie(self):
        pass

    # inits all values of the product
    def __init__(self, initial_url, color, size):
        self.initial_url = initial_url
        self.color = color
        self.size = size
        self.name = self.set_product_name()
        self.category = self.set_product_category()
        self.url = self.set_product_url()
        self.item_cookie = self.set_item_cookie()
        self.size_cookie = self.set_size_cookie()

class CheckoutBot:

    def __init__(self):
        pass

    # adds product to cart using selenium webdriver
    def add_product_to_cart_using_driver(self, driver, product):
        if product.color == '':
            time.sleep(5)

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

    # addsproduct to cart by injecting cookies
    def add_product_to_cart_using_cookies(self, driver, product):
        #cookie = {'cart' : '1+item--' + }
        print(product.item_cookie)

    # locate each input and fill accordingly
    def fill_checkout_info(self, driver):
        name_input = driver.find_element_by_id('order_billing_name')
        name_input.clear()
        name_input.send_keys('John Doe')

        email_input = driver.find_element_by_id('order_email')
        email_input.clear()
        email_input.send_keys('john@doe.com')

        phone_number_input = driver.find_element_by_id('order_tel')
        phone_number_input.clear()
        phone_number_input.send_keys('206 444 4444')

        address_input = driver.find_element_by_id('bo')
        address_input.clear()
        address_input.send_keys('400 Broad St')

        zip_code_input = driver.find_element_by_id('order_billing_zip')
        zip_code_input.clear()
        zip_code_input.send_keys('98101')

        city_input = driver.find_element_by_id('order_billing_city')
        city_input.clear()
        city_input.send_keys('Seattle')

        state_input = Select(driver.find_element_by_id('order_billing_state'))
        state_input.select_by_value('WA')

        country_input = Select(driver.find_element_by_id('order_billing_country'))
        country_input.select_by_value('USA')

        card_input = driver.find_element_by_id('nnaerb')
        card_input.clear()
        card_input.send_keys('1234 5678 1234 5678')

        cvv_input = driver.find_element_by_id('orcer')
        cvv_input.clear()
        cvv_input.send_keys('123')

        card_month_input = Select(driver.find_element_by_id('credit_card_month'))
        card_month_input.select_by_value('01')

        card_year_input = Select(driver.find_element_by_id('credit_card_year'))
        card_year_input.select_by_value('2020')

        order_terms_input = driver.find_element_by_class_name('terms').find_element_by_class_name('iCheck-helper')
        order_terms_input.click()
        
    def click_payment_btn(self, driver):
        submit_payment_btn = driver.find_element_by_id('pay').find_element_by_name('commit')
        submit_payment_btn.click()

class User:

    def __init__(self):
        # initial testing values
        # URL - http://www.supremenewyork.com/previews/springsummer2018/jackets/tiger-stripe-track-jacket-4
        # Color - White

        # initial user input values
        self.initial_url = input('Enter preview URL: ')

        print('Is the Item an accessory?')
        if input('y/n: ') == 'y':
            self.is_accessory = True
        else:
            self.is_accessory = False

        if not self.is_accessory:
            print('If you don\'t know the color leave blank, the bot will pause for 5 seconds to let you choose while it is running, if you want it to select the first possible color input any color')
            self.color = input('Enter color: ')
            self.size = input('Enter size: ')

        print('Do you want to use cookies or a webdriver to add the item to your cart')
        self.add_to_cart_method = input('cookies/webdriver: ')

        print('Do you want process payment to automatically be selected (can mess with captcha if automatic)')
        if input('y/n: ') == 'y':
            self.auto_click_payment_btn = True
        else:
            self.auto_click_payment_btn = False

def main():
    quit = False

    while not quit:
        # inits new user object
        user = User()

        # inits selenium chrome web driver
        driver = webdriver.Chrome()
        driver.get('http://www.supremenewyork.com')

        # inits product object
        product = Product(user.initial_url, user.color, user.size)
        # init a supreme bot object
        checkout_bot = CheckoutBot()

        # gets product url and opens it
        driver.get(product.url)
        assert product.name in driver.title

        if user.add_to_cart_method == 'cookies':
            checkout_bot.add_product_to_cart_using_cookies(driver, product)
            driver.get('https://www.supremenewyork.com/checkout')
        elif user.add_to_cart_method == 'webdriver':
            checkout_bot.add_product_to_cart_using_driver(driver, product)
        else:
            print('No add to cart method was found')
            quit = True

        assert 'Supreme' in driver.title
        # fills out checkout information
        checkout_bot.fill_checkout_info(driver)

        #clicks checkout button
        if user.auto_click_payment_btn:
            checkout_bot.click_payment_btn(driver)

        # gives user time to do captcha and finish checkout
        time.sleep(5000)

if __name__ == '__main__':
    main()