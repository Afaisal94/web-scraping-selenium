from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome()

all_urls = []
data_products = []

def scraping_url_product():
    driver = webdriver.Chrome()
    driver.get("https://www.amazon.com")

    # input text & submit
    input = driver.find_element(By.ID, 'twotabsearchtextbox')
    input.send_keys("Headset")
    input.send_keys(Keys.ENTER)
    total_pages = driver.find_element(By.XPATH, "//span[@class='s-pagination-item s-pagination-disabled']")
    total_pages = int(total_pages.text)
    # total_pages = 5

    # Looping by total pages
    for x in range(total_pages):
        # Get Url
        current_url = driver.current_url
        driver.get(current_url)
        # Scraping Process
        urls = driver.find_elements(By.XPATH, "//a[@class='a-link-normal s-link-style a-text-normal']")
        count = len(urls)
        for n in range(count):
            url = urls[n].get_attribute('href')
            all_urls.append(url)
        print(f'Scraping ke-{x+1} : {current_url}')

        # Click Next
        btn_next = driver.find_elements(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
        next = len(btn_next)
        if (next == 1):
            btn_next = driver.find_element(By.XPATH, "//a[@class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator']")
            btn_next.click()
        else:
            pass

    print('Scraping URL has been successful !')


def scraping_data_product():
    driver = webdriver.Chrome()
    count = len(all_urls)
    for x in range(count):
        url = all_urls[x]
        driver.get(url)

        title = driver.find_element(By.ID, 'productTitle').text
        img = driver.find_element(By.XPATH, "//div[@id='imgTagWrapperId']/img").get_attribute('src')
        link = driver.current_url

        try:
            price = driver.find_element(By.XPATH, "//span[@id='price_inside_buybox']").text
        except:
            price = 'No Data'

        content = [title, price, img, link]
        data_products.append(content)

    print('Scraping Data Products has been successful !')

def save_data_csv():
    with open('data.csv', mode='w', newline='') as csv_file:
        # Create object
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # Write
        writer.writerow(["TITLE", "PRICE", "IMAGE URL", "PRODUCT URL"])
        for d in data_products:
            writer.writerow(d)
    print("Writing to CSV has been successful !")



scraping_url_product()
scraping_data_product()
save_data_csv()


print('Done')


# close browser
driver.quit()