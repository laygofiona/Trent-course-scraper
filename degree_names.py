from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

# Utility functions

# Close pop up window in main page
def close_pop_up(driver):
    # Wait until pop up window appears
    WebDriverWait(driver, 8).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[26]/div[1]/div/div/div/div"))) 

    # Check if close button is present before waiting for clickability
    close_button = driver.find_element(By.XPATH, "/html/body/div[26]/div[1]/div/button")
    if close_button is not None:
        WebDriverWait(driver, 14).until(EC.element_to_be_clickable(close_button))
        close_button.click()

    print("pop up closed")  

# Write program names to the file
def write_program_names(programs, f):
    # for each program
    for program in programs:
        program_name = program.text
        f.write(f"{program_name} \n")

def main():
    service = Service(executable_path="./chromedriver")
    driver = webdriver.Chrome(service=service)

    # Set up file to write course names to
    f = open("programs.txt", "a+")

    driver.get("https://www.trentu.ca/futurestudents/undergraduate/programs")

    close_pop_up(driver)


    # Wait until program links appear on page
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "program-link"))
    )


    # Find all program links with credential-degree class 
    degree_programs = driver.find_elements(By.CLASS_NAME, "credential-degree")

    # Write program names to the file
    write_program_names(degree_programs, f)
    
    f.close()
    driver.quit()

main()

