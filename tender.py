import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

location = os.getcwd()

preference = {"download.default_directory": location}

# Making an instance of Chrome options
ops = webdriver.ChromeOptions()
ops.add_experimental_option("prefs", preference)

driver = webdriver.Chrome(options=ops)

try:
    driver.get("https://etender.up.nic.in/nicgep/app")

    tenders_by_org = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@id='PageLink_0']"))
    )

    time.sleep(2)
    tenders_by_org.click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("https://etender.up.nic.in/nicgep/app?page=FrontEndTendersByOrganisation&service=page")
    )

    # Find all rows in table1
    table1 = driver.find_elements(By.XPATH, "//*[@id='table']//tr[1]/following-sibling::tr")

    for row in table1:
        print(row.text)

    # Find all tender links in table1
    tenders_table1 = driver.find_elements(By.XPATH, "//*[@id='table']//tr[1]/following-sibling::tr/td[3]/a")

    list_of_tenders_table1 = []

    for organisation_link in tenders_table1:
        organisation_link_href = organisation_link.get_attribute('href')
        list_of_tenders_table1.append(organisation_link_href)

    for tender in list_of_tenders_table1:
        driver.get(tender)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='table']/tbody/tr[1]/td[5]"))
        )

        # Find all tender links in table2
        tender_link_table2 = driver.find_elements(By.XPATH, "//*[@id='table']//tr[1]/following-sibling::tr/td[5]/a")

        list_of_tenders_table2 = []

        for link in tender_link_table2:
            link_href = link.get_attribute('href')
            list_of_tenders_table2.append(link_href)

        for link in list_of_tenders_table2:
            print("Tender Link:", link)

            driver.get(link)
            time.sleep(2)
            tenderID = driver.find_element(By.XPATH, "//*[@id='content']/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/b").text
            print("Tender ID:", tenderID)

finally:
    driver.quit()
