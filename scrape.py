# Write the function to take input of the url
# & return all the content of the html page

import selenium.webdriver as webdrive
from selenium.webdriver.chrome.service import Service
import time

def scrape_website(website):
    print("Launching the chrome browser...")
    
    chrome_driver_path = "./chromedriver.exe"
    # Option: Configure how Chrome should run, with options Like
    # - Use headless mode for non-GUI execution.
    # - Optionally disable loading images to save bandwidth.
    options = webdrive.ChromeOptions()
    # Now select the browser, like chrome or any other
    driver = webdrive.Chrome(service=Service(chrome_driver_path), options=options)    
    
    try:
        driver.get(website)
        print("Page Loaded... ")
        html = driver.page_source
        time.sleep(10)
        
        return html
    finally:
        driver.quit()
        
# For some website, this will not run due to captcha like amazon.ca
# To overcome these problem use online servie like brightData


# ------------------------------------------------

# Now we need to clear the data, just like the textual content and that to the LLM and allow it to parse it,
# And also reduce the amount of characters or batches that we need to sun,it to out LLM to get a valueable response
        
from bs4 import BeautifulSoup

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return "" #to erdicate error's if no body is found

def clear_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")
    
    # Now remove all the Javascript and CSS
    for script_or_style in soup(["script","style"]):
        script_or_style.extract
        
    # This tell to get all the text and seperate them with the new line charaxter
    cleaned_content = soup.get_text(separator="\n")
    
    # Remove all the \n in-between the text
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content

# Passing the content with-in the limit of token for LLM
# Returns nest array, which each element is token of 6000
# For loop(0 to total lenth of dom_content, step size = 6000 i.e. token limit we sepeified)
# dom_content[i : i +max_length]-> from 0 to 5999
def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i +max_length] for i in range(0,len(dom_content), max_length)
    ]
    