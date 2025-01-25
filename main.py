from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def search_clip_cafe(transcribed_text):
    # Set up the browser (ensure you have the correct driver installed)
    driver = webdriver.Chrome()

    try:
        # Open Clip Cafe
        driver.get("https://clip.cafe")

        # Find the search bar and input the text
        search_bar = driver.find_element("name", "search")  # Update selector as per the website's HTML
        search_bar.send_keys(transcribed_text)
        search_bar.send_keys(Keys.RETURN)

        # Wait for results and scrape them (adjust wait and selectors)
        driver.implicitly_wait(5)
        results = driver.find_elements("css selector", ".result-class")  # Replace with actual class name

        # Extract and return the results
        for result in results:
            print(result.text)
    except NoSuchElementException as e:
        print(f"Error: Element not found. {e}")
    except TimeoutException as e:
        print(f"Error: Timeout while waiting for elements. {e}")
    finally:
        driver.quit()

# Example usage
transcribed_text = "May the Force be with you"
search_clip_cafe(transcribed_text)
