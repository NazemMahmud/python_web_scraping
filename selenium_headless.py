from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time

website = "https://www.audible.com/search"
path = "C:\\nmpiash\\Software\\chromedriver-win64\\chromedriver.exe"
service = Service(executable_path=path)  # selenium 4
options = Options()
# options.headless = True # old mood
# options.add_argument('window-size=1920x1080')
# options.add_argument('--headless=new')

driver = webdriver.Chrome(options=options, service=service)
driver.get(website)
driver.maximize_window() # in headless false mood

# Locating the box that contains all the audiobooks listed in the page
container = driver.find_element(By.CLASS_NAME,  'adbl-impression-container ')
# Getting all the audiobooks listed (the "/" gives immediate child nodes)
products = container.find_elements( By.XPATH, './/li[contains(@class, "productListItem")]')
# products = container.find_elements_by_xpath('./li')

# Pagination 1
pagination = driver.find_element(By.XPATH,'//ul[contains(@class, "pagingElements")]')  # locating pagination bar
pages = pagination.find_elements(By.TAG_NAME,'li')  # locating each page displayed in the pagination bar
last_page = 5 # int(pages[-2].text)  # getting the last page with negative indexing (starts from where the array ends)


# Initializing storage
book_title = []
book_author = []
book_length = []

# Pagination 2
current_page = 1   # this is the page the bot starts scraping


# The while loop below will work until the bot reaches the last page of the website, then it will break
while current_page <= last_page:
    time.sleep(10)  # let the page render correctly
    container = driver.find_element(By.CLASS_NAME,'adbl-impression-container ')
    products = container.find_elements(By.XPATH,'.//li[contains(@class, "productListItem")]')
    # products = container.find_elements_by_xpath('./li')

    for product in products:
        # We use "contains" to search for web elements that contain a particular text, so we avoid building long XPATH
        title = product.find_element( By.XPATH,'.//h3[contains(@class, "bc-heading")]').text
        book_title.append(title)  # Storing data in list
        print(title)
        book_author.append(product.find_element( By.XPATH,'.//li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element( By.XPATH,'.//li[contains(@class, "runtimeLabel")]').text)

    current_page = current_page + 1  # increment the current_page by 1 after the data is extracted
    # Locating the next_page button and clicking on it. If the element isn't on the website, pass to the next iteration

    try:
        next_page = driver.find_element(By.XPATH, './/span[contains(@class , "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()
# Storing the data into a DataFrame and exporting to a csv file
df_books = pd.DataFrame({'title': book_title, 'author': book_author, 'length': book_length})
df_books.to_csv('books.csv', index=False)