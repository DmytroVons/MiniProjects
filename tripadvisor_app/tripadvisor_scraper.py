import json
import os.path
import time
from typing import List

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy as AppiumBy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class TripAdvisorScraper:
    """
    A class to scrape hotel information and prices from TripAdvisor using Appium and Selenium.

    Attributes:
        driver (webdriver.Remote): The Appium WebDriver instance for interacting with the app.
        selected_dates (List[List[str]]): A list of date ranges to search for hotel deals.
    """

    def __init__(self, driver: webdriver.Remote, selected_dates: tuple[List[str]]) -> None:
        """
                Initialize the TripAdvisorScraper with the Appium WebDriver instance and selected date ranges.

                Args:
                    driver (webdriver.Remote): The Appium WebDriver instance.
                    selected_dates (tuple[List[str]]): A list of date ranges in the format [['from', 'to'], ...].
                """
        self.driver = driver
        self.actions = ActionChains(driver)
        self.wait = WebDriverWait(driver, 20)
        self.selected_dates = selected_dates
        self.hotels_info = []

    def scroll_down_action(self):
        """
        Perform a scroll down action using touch gestures.
        """
        self.actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        self.actions.w3c_actions.pointer_action.move_to_location(814, 1639)
        self.actions.w3c_actions.pointer_action.pointer_down()
        self.actions.w3c_actions.pointer_action.move_to_location(828, 608)
        self.actions.w3c_actions.pointer_action.release()
        self.actions.perform()

    def scroll_up_action(self):
        """
        Perform a scroll up action using touch gestures.
        """
        self.actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        self.actions.w3c_actions.pointer_action.move_to_location(881, 1656)
        self.actions.w3c_actions.pointer_action.pointer_down()
        self.actions.w3c_actions.pointer_action.move_to_location(900, 1101)
        self.actions.w3c_actions.pointer_action.release()
        self.actions.perform()

    def perform_search(self, search_query: str):
        """
        Perform a search for the provided query on TripAdvisor app.

        Args:
            search_query (str): The search query for hotels.
        """
        self.scroll_down_action()
        el1 = self.wait.until(EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Tripadvisor")))
        el1.click()
        self.driver.implicitly_wait(500)
        el2 = self.wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, "//android.widget.FrameLayout[@content-desc=\"Search\"]/android.widget.ImageView")))
        el2.click()
        el3 = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")))
        el3.click()
        el4 = self.wait.until(
            EC.presence_of_element_located((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/edtSearchString")))
        el4.click()
        el4.send_keys(search_query)
        self.driver.implicitly_wait(3)
        el5 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,
                                                              "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[1]")))
        el5.click()

    def scrape_and_save(self, search_query: str):
        """
        Scrape hotel information and prices for the selected date ranges and save to hotels_info list.

        Args:
            search_query (str): The search query for hotels.
        """
        self.perform_search(search_query)
        first_loop = True
        for date in self.selected_dates:
            el1 = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/txtDate")))
            el1.click()
            el2 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,
                                                                  f"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.GridView/android.widget.FrameLayout[{date[0]}]/android.widget.TextView")))
            from_date = el2.text
            el2.click()
            el3 = self.wait.until(EC.presence_of_element_located((AppiumBy.XPATH,
                                                                  f"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.GridView/android.widget.FrameLayout[{date[1]}]/android.widget.TextView")))
            to_date = el3.text
            el3.click()
            el4 = self.wait.until(
                EC.presence_of_element_located((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/btnPrimary")))
            el4.click()
            if first_loop:
                self.driver.implicitly_wait(30)
                self.scroll_up_action()
                el5 = self.wait.until(
                    EC.presence_of_element_located((AppiumBy.ID, "com.tripadvisor.tripadvisor:id/btnAllDeals")))
                el5.click()
                first_loop = False
            self.form_hotel_info(from_date=from_date, to_date=to_date)

    def form_hotel_info(self, from_date: str, to_date: str) -> List:
        """
        Extract hotel information from the UI elements and save to hotels_info list.

        Args:
            from_date (str): The start date of the hotel deal.
            to_date (str): The end date of the hotel deal.

        Returns:
            List: A list of dictionaries containing hotel information.
        """
        time.sleep(5)
        screenshot_filename = f"screenshot_{from_date}-{to_date}.png"
        self.driver.save_screenshot(os.path.join("files", screenshot_filename))
        # Find the parent element
        parent_element = driver.find_element(AppiumBy.XPATH,
                                             "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView")

        # Find all the smaller elements (hotel elements) within the parent element
        hotel_elements = parent_element.find_elements(AppiumBy.XPATH,
                                                      "//androidx.cardview.widget.CardView/android.view.ViewGroup")
        # Iterate through each hotel element
        for hotel_element in hotel_elements:
            try:
                # Find the hotel name element within the current hotel element
                hotel_name_element = hotel_element.find_element(AppiumBy.ID,
                                                                "com.tripadvisor.tripadvisor:id/txtProviderName")
                hotel_name = hotel_name_element.text

                # Find the price element within the current hotel element
                price_element = hotel_element.find_element(AppiumBy.ID,
                                                           "com.tripadvisor.tripadvisor:id/txtPriceTopDeal")
                hotel_price = price_element.text

                self.hotels_info.append({hotel_name: {"provider": hotel_price, "screenshot": screenshot_filename}})
            except NoSuchElementException:
                # Handle the case where the elements were not found
                print("Hotel information not found for an element.")
        return self.hotels_info

    def save_result_to_file(self, filename):
        """
        Save the scraped hotel information to a JSON file.

        Args:
            filename (str): The filename for the JSON file.
        """
        with open(filename, "w") as json_file:
            json.dump(self.hotels_info, json_file, indent=4)


if __name__ == '__main__':
    desired_caps = {
        "platformName": "Android",
        "deviceName": "emulator-5554",
        "platformVersion": "11.0",
        "automationName": "UiAutomator2",
        "noReset": "false",
        "fullReset": "false"
    }
    driver = webdriver.Remote("http://172.28.144.1:4723/wd/hub", desired_caps)
    selected_dates = (["20", "21"], ["21", "22"], ["24", "25"], ["25", "26"], ["30", "31"])
    scraper = TripAdvisorScraper(
        driver=driver,
        selected_dates=selected_dates
    )

    scraper.scrape_and_save("The Grosvenor Hotel")
    scraper.save_result_to_file(os.path.join("files", "prices.json"))

    driver.quit()
