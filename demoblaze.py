import pytest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from credentials import username, password
import time


@pytest.fixture(scope="class")
def chrome_driver_init(request):
    chrome_driver = webdriver.Chrome()
    chrome_driver.maximize_window()
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()
    chrome_driver.quit()


@pytest.mark.usefixtures("chrome_driver_init")
class TestPriceAndTitle:

    def test_login(self):
        self.driver.get('https://www.demoblaze.com/')
        self.driver.find_element(By.ID, "login2").click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "loginusername"))).get_attribute("value")
        self.driver.find_element(By.ID, "loginusername").send_keys(username)
        self.driver.find_element(By.ID, "loginpassword").send_keys(password)
        self.driver.find_element(By.XPATH, '//*[@id="logInModal"]//button[2]').click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//a[@href='prod.html?idp_=3']")))
        time.sleep(2)
        assert self.driver.find_element(By.XPATH, "//a[@href='prod.html?idp_=3']").size['width'] != 0, "Nexus 6 is not exist"

    def test_add_item(self):
        self.driver.find_element(By.XPATH, "//a[@href='prod.html?idp_=3']").click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn.btn-success.btn-lg")))
        self.driver.find_element(By.CLASS_NAME, "btn.btn-success.btn-lg").click()
        time.sleep(2)
        alert = self.driver.switch_to.alert
        alert.accept()
        self.driver.find_element(By.ID, "cartur").click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@src= 'imgs/Nexus_6.jpg']")))
        assert self.driver.find_element(By.XPATH, "//*[@src= 'imgs/Nexus_6.jpg']").size['width'] != 0, "Nexus 6 is not exist on cart"

    def test_title_and_price(self):
        title_by_element = self.driver.find_element(By.XPATH, '//*[@id="tbodyid"]/tr/td[2]').text
        price_by_element = self.driver.find_element(By.XPATH, '//*[@id="tbodyid"]/tr/td[3]').text
        assert title_by_element == "Nexus 6", "Title is not Nexus 6"
        assert price_by_element == "650", "Price is not 650"
