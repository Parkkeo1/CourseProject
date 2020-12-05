from bs4 import BeautifulSoup

# uses webdriver object to execute javascript code and get dynamically loaded webcontent
def scrape_url(url, driver):
    driver.get(url)
    res_html = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(res_html, "html.parser")
    return clean_soup(soup)

def clean_soup(soup):
    for scr in soup.find_all(['script', 'img', 'style']):
        scr.decompose()
    return soup
