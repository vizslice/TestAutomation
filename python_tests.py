"""
Sample Selenium test using Python's built-in unittest framework.
 
Run with:
    python -m unittest seleniumtest.py -v
or simply:
    python seleniumtest.py
"""
 
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
 
 
class SeleniumSampleTest(unittest.TestCase):
 
    def setUp(self):
        # Selenium Manager auto-downloads the correct chromedriver for you.
        options = webdriver.ChromeOptions()
        # Uncomment the next line to run without opening a visible browser window:
        # options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(5)
        self.addCleanup(self.driver.quit)  # ensures browser closes even if test fails
 
    def test_page_title(self):
        """Verify the Selenium homepage loads and has the expected title."""
        self.driver.get("https://www.selenium.dev")
        self.assertIn("Selenium", self.driver.title)
 
    def test_search_on_duckduckgo(self):
        """Perform a simple search and verify results appear."""
        self.driver.get("https://duckduckgo.com")
        search_box = self.driver.find_element(By.NAME, "q")
        search_box.send_keys("Selenium Python")
        search_box.send_keys(Keys.RETURN)
 
        # Wait until at least one result link is present
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='result-title-a']"))
        )
        results = self.driver.find_elements(By.CSS_SELECTOR, "a[data-testid='result-title-a']")
        self.assertGreater(len(results), 0, "Expected at least one search result")
 
 
if __name__ == "__main__":
    unittest.main()