import requests
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


def main():

    preview_url = input('Enter preview URL: ')

    print('Leave blank if none')
    size = input('Enter size: ')

    print('Leave blank for no color')
    color = input('Enter color: ')

    # inits selenium chrome web driver
    driver = webdriver.Chrome()
    driver.get('http://www.supremenewyork.com')

    # gets all info for product
    product_name = get_product_name(preview_url)
    product_category = get_product_category(preview_url)
    product_url = get_product_url(product_category, product_name, color)
    if not size == '':
        size_cookie = get_size_cookie(product_url, size)

    # opens product page
    driver.get(product_url)

    assert product_name in driver.title

    # fills out all entered product and billing info
    if not size == '':
        select_product_size(driver, size_cookie)
    add_product_to_cart(driver, color)
    fill_checkout_info(driver)
    click_payment_btn(driver)

    # gives user time to do captcha and finish checkout
    time.sleep(5000)


def get_product_name(initial_url):
    # grabs preview page url and gets text from it
    page = requests.get(initial_url)
    page_data = page.text

    soup = BeautifulSoup(page_data, 'html.parser')

    # gets the product name equal to the information from preview page
    return str(soup.find('div', class_='description').div.h2.text)


def get_product_category(initial_url):
    # splits string by 5th slash which will always output correct category
    return str(initial_url.split('/')[5]).replace('-', '_')


def get_product_url(category, name, color):
    category_url = 'http://www.supremenewyork.com/shop/all/' + \
        str(category)

    page = requests.get(category_url)
    page_data = page.text

    soup = BeautifulSoup(page_data, 'html.parser')

    # gets array of a tags with the product name and an array of a tags with product color
    items_of_same_name = soup.find_all('a', string=name)
    # some products have an extra space at end of name
    items_of_same_name += soup.find_all('a', string=name + ' ')
    items_of_same_color = soup.find_all('a', string=color)

    # runs all hrefs together to get a matching pair
    for product in items_of_same_name:
        for color in items_of_same_color:
            if product['href'] == color['href']:
                return 'http://www.supremenewyork.com' + product['href']

    # if not returns first product with the name
    return 'http://www.supremenewyork.com' + items_of_same_name[0]['href']


def get_size_cookie(url, size):
    page = requests.get(url)
    page_data = page.text

    soup = BeautifulSoup(page_data, 'html.parser')

    cookie_val = soup.find('select', {'id': 's'}).find(
        'option', text=size)['value']
    return cookie_val


def select_product_size(driver, size_cookie):
    size_input = Select(driver.find_element_by_id('s'))
    size_input.select_by_value(size_cookie)


def add_product_to_cart(driver, color):
    if color == '':
        time.sleep(5)

    # finds and clicks add ot cart button
    add_to_cart_btn = driver.find_element_by_xpath(
        "//input[@value='add to cart']")
    add_to_cart_btn.click()

    # waits until checkout is visible then clicks
    try:
        checkout_ready = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'checkout'))
        )
    finally:
        check_out_btn = driver.find_element_by_xpath(
            "//a[@class='button checkout']")
        check_out_btn.click()


def fill_checkout_info(driver):
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

    country_input = Select(
        driver.find_element_by_id('order_billing_country'))
    country_input.select_by_value('USA')

    card_input = driver.find_element_by_id('nnaerb')
    card_input.clear()
    card_input.send_keys('1234 5678 1234 5678')

    cvv_input = driver.find_element_by_id('orcer')
    cvv_input.clear()
    cvv_input.send_keys('123')

    card_month_input = Select(
        driver.find_element_by_id('credit_card_month'))
    card_month_input.select_by_value('01')

    card_year_input = Select(driver.find_element_by_id('credit_card_year'))
    card_year_input.select_by_value('2020')

    order_terms_input = driver.find_element_by_class_name(
        'terms').find_element_by_class_name('iCheck-helper')
    order_terms_input.click()


def click_payment_btn(driver):
    submit_payment_btn = driver.find_element_by_id(
        'pay').find_element_by_name('commit')
    submit_payment_btn.click()


if __name__ == '__main__':
    main()
