from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, NoSuchElementException, ElementNotInteractableException
import argparse

# Utility functions

def get_subject_dropdown_values(driver):
    # wait until the subject drop down is visible
    # locate subject drop down
    # go through each option element in the select tag with the id of subjectSelect
    # get text and add it to subject_values array
    subjects = []
    try:
        # Create an xpath variable for the span tag which contains the degree program name
        select_id = "subjectSelect"
        
        # Wait until dropdown (select element) appears
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, select_id))) 
        # Find the corresponding element
        select_element = driver.find_element(By.ID, select_id)

        # Create a Select object
        select = Select(select_element)

        # Get all options
        all_options = select.options

        # Iterate through options and only append options that are not disabled and have a value to the subjects[]
        for option in all_options:
            if not option.get_attribute("disabled") and option.get_attribute("value"):
                subjects.append(str(option.text))
        

    except (StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error getting subject dropdown values: {e}")
    
    finally:
        return subjects


def set_dropdown(driver, value, id, selectByValue):
    # wait until the drop down is visible
    # locate drop down using id
    # Set the dropdown value to be the value

    try:
        select_id = id


        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, select_id))) 
        # Find the corresponding element
        select_element = driver.find_element(By.ID, select_id)

        # Create a Select object
        select = Select(select_element)

        # Set select object to be selected to the value or visible text
        if(selectByValue):
            select.select_by_value(value)
        else:
            select.select_by_visible_text(value)


    except (StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error setting dropdown value: {e}")



def press_search_button(driver):
    # wait until the search button is visible
    # locate search button
    # wait until the search button is clickable
    # Click the search button

    try:
        xpath_btn = f"//button[contains(text(), 'Search')]"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, xpath_btn)))
        # Check if search button is present before waiting for clickability
        search_button = driver.find_element(By.XPATH, xpath_btn)
        if search_button is not None:
            WebDriverWait(driver, 14).until(EC.element_to_be_clickable(search_button))
            # Alternative approach to click search_button
            driver.execute_script("arguments[0].click();", search_button)
    except (StaleElementReferenceException, TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error pressing search button: {e}")


def check_if_results_exist(driver, id):
    try:
        # Wait until element exists
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, id)))
        # Find div element with the resultsTable id
        results_table = driver.find_element(By.ID, id)
        if results_table is not None:
            return True

    except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
        print(f"Error with checking search results: No search results found")
        # Return false if it doesn't
        return False

def iterate_results_table(driver, courses_file, faculty_file, courses):
    tbody_id = "resultsBody"
    try:
        # wait until a <tbody> element with an id of resultsBody is visible
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, tbody_id)))
        # Find results table and assign it to results_body
        results_body = driver.find_element(By.ID, tbody_id)
        # Get the rows within results_body
        rows = results_body.find_elements(By.TAG_NAME, "tr")
        # Set up faculty array to keep track of staff members
        faculty = []

        
        # Iterate through each <tr> or row element
        for row in rows:
            try:
                # Scroll to the row
                driver.execute_script("arguments[0].scrollIntoView();", row)
                # Wait until row is visible
                #WebDriverWait(driver, 10).until(EC.visibility_of(row))

                # Find <td> elements in each row
                cells = row.find_elements(By.TAG_NAME, "td")

                # Add info to faculty.txt
                # professor(s) for each course will always be the last cell in each row
                faculty_cell = cells[len(cells) - 1].text
                # check if the last cell is not empty and not "To be Announced" and its text is not in faculty[]
                if(faculty_cell != "" and faculty_cell != "To be Announced" and faculty_cell not in faculty):
                    # Convert string to array where , separates elements
                    faculty_arr = faculty_cell.split(',')
                    # Write contents of faculty_arr to file by listing faculty names on one line separated by a space
                    faculty_string = " ".join(faculty_arr)
                    faculty_file.write(f"{faculty_string}  ")

                    # append the professor(s) to the faculty array
                    for member in faculty_arr:
                        faculty.append(member)


                # Add info to courses.txt
                # check if course name (cell[2]) in row is present in courses[]
                # if it isn't present and not empty, then iterate over td elements
                if(cells[2].text != "" and cells[2].text not in courses):

                    # Iterate over td elements
                    for index, cell in enumerate(cells):
                        # Ensure that cell is not empty
                        if(cell.text != ""):
                            # Find the course name/title
                            # course name is always in the third <td>
                            if(index == 2):
                                # Write the course name text to the f on a new line
                                courses_file.write(f"{cell.text}\n")
                                # Append cell.text (course name) to courses to prevent duplicate courses
                                courses.append(str(cell.text))

                            # Find cross-listed courses
                            # cross-listed courses are always in the fourth <td>
                            if(index == 3):          
                                # check if the fourth <td> isn't empty
                                # Iterate through each cross-listed course
                                # cross-listed courses are contained within <ul>
                                # Find <ul> within cell
                                ul = cell.find_element(By.TAG_NAME, "ul")

                                # Write all cross-listed courses texts on one line with spaces in between
                                # Find <li> within <ul>
                                lis = ul.find_elements(By.TAG_NAME, "li")
                                for li in lis:
                                    # get each cross_listed course and write it to the file
                                    # Remove any last two characters from the text
                                    courses_file.write(f"{li.text[:-2]} ")

                    # Find the course code
                    # course code is in the <th> element with a class of text-nowrap
                    head = row.find_element(By.CSS_SELECTOR, "th.text-nowrap")
                    # Write the course code text on the same line as the cross-listed courses line, separated by a space, if it isn't empty
                    # Remove any last two characters from the text
                    courses_file.write(f"{head.text[:-2]}\n")
        

            except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
                print("row isn't visible")
    


    except (StaleElementReferenceException, TimeoutException, NoSuchElementException) as e:
        print(f"Error iterating through results table")

    finally:
        faculty_file.write(f"\n")

# Main function
def main():
    # Setting up service and driver
    service = Service(executable_path="./chromedriver")
    driver = webdriver.Chrome(service=service)

    # Parse year argument
    parser = argparse.ArgumentParser(description = "Process year")
    parser.add_argument('year', type=int, help="Obtain course and faculty listing within that year")
    args = parser.parse_args()

    # Set up file to write course names and codes to
    f = open("courses.txt", "w")
    # Set up file to write faculty names 
    s = open("faculty.txt", "w")

    # Go to academic timetable website
    driver.get("https://my.trentu.ca/portal/applications/timetable/public/landing.php")

    # Get subject drop down text values
    subject_values = get_subject_dropdown_values(driver)
    

    # Location will always be set to all locations
    location = {
        "value": "ALL", 
        "id": "locationSelect"
    }

    # Term will always be set to the 2024-2025 academic year
    term = {
        "value": f"{args.year}AY", 
        "id": "termSelect"
    }

    # Setting subject id
    subject_id = "subjectSelect"

    # Setting results table id
    results_table_id = "resultsTable"

    # Set up courses array to keep track of courses
    courses = []
    
    
    # iterate over subject_values array
    # For each subject
    for subject in subject_values:
        # Set the location value in location dropdown
        set_dropdown(driver, location["value"], location["id"], True)
        # Set the subject dropdown to point to the subject
        set_dropdown(driver, subject, subject_id, False)
        # Set the term value in term dropdown
        set_dropdown(driver, term["value"], term["id"], True)
        # Press the search button
        press_search_button(driver)

        # Check if results table exists
        results_exists = check_if_results_exist(driver, results_table_id)

        # if results exist
        if(results_exists):
            # write subject name to courses.txt 
            f.write(f"\n{subject}\n")
            # write subject name to faculty.txt
            s.write(f"\n{subject}\n")
            f.write(f"=====\n")
            iterate_results_table(driver, f, s, courses)
            f.write(f"=====\n")
            
            
    s.close()
    f.close()
    driver.quit()



main()