# ------------------------------------------------------------------------------------------ #
# Title: Assignment06
# Desc: This assignment demonstrates using functions
# with structured error handling
# Change Log: (Who, When, What)
#   RRoot,1/1/2030,Created Script
#   LBatista, 11.18.2023, Mod06 Homework
# ------------------------------------------------------------------------------------------ #
import json
import io as _io  # Needed to try closing in the "finally" block

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
# Define the Data Constants
# FILE_NAME: str = "Enrollments.csv"
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables and constants
student_first_name: str = ''  # Holds the first name of a student entered by the user.
student_last_name: str = ''  # Holds the last name of a student entered by the user.
course_name: str = ''  # Holds the name of a course entered by the user.
student_data: dict = {}  # one row of student data
students: list = []  # a table of student data
csv_data: str = ''  # Holds combined string data separated by a comma.
json_data: str = ''  # Holds combined string data in a json format.
file = _io.TextIOWrapper  # This is the actual type of the file handler.
menu_choice: str  # Hold the choice made by the user.


class FileProcessor:
    """
    A collection of processing Layer functions that work with JSON files

    Changelog: (who,when, what)
    LBatista, 11.19.2023, created class
    """
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        This function reads the file and raises an error if the json file doesn't exist.
        :param file_name: Enrollments.json
        :param student_data: student first name, student last name, course
        :return: student data
        """
        try:
            file = open(file_name, "r")
            student_data = json.load(file)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages("Text file must exist before running this script!\n Creating it...")
            with open(FILE_NAME, "w") as file:
                json.dump(students, file)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!\n")
        finally:
            if file.closed == False:
                file.close()
        return student_data

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        This function writes the data to our JSON file

        Changelog: (who, when, what)
        LBatista, 11.19.2023, created function

        :return: None
        """
        try:
            file = open(file_name, "w")
            json.dump(student_data, file)
            print("The data was saved to the file! ")
            file.close()
        except TypeError as e:
            IO.output_error_messages("Please check that the data is a valid JSON format", e)

        except Exception as e:
            IO.output_error_messages("There was a non-specific error", e)

        finally:
            if file.closed == False:
                file.close()


class IO:
    """
    A collection of presentation layer functions that manage user input and output

    Changelog: (who, when, what)
    LBatista, 11.19.2023, created class
    """
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """ This function displays the custom error messages to the user

        Changelog: (who, when, what)
        LBatista, 11.18.2023, created the function

        :return: None
        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
        This function displays the menu of choices to the user

        Changelog: (who, when, what)
        LBatista, 11.18.2023, created function
        :return: None
        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """
        This function gets a menu choice from the user
        :return: string with user's choice
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please select option 1-4 ")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message
        return choice

    @staticmethod
    def input_student_data(student_data:list):
        """ This function allows the user to input data for new students

        Changelog: (who, when, what
        LBatista, 11.19.2023, created function
        :return: str
        """
        try:
            student_first_name = input("Enter the student's first name: ")
            if any(char.isdigit() for char in student_first_name):
                raise ValueError("The first name should only contain letters. ")
            student_last_name = input("Enter the student's last name: ")
            if any(char.isdigit() for char in student_last_name):
                raise ValueError("The last name should only contain letters. ")
            course_name = input("Please enter the name of the course: ")
            student_data = {"FirstName": student_first_name,
                                "LastName": student_last_name,
                                "CourseName": course_name}
            students.append(student_data)

            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            IO.output_error_messages("That value is not the correct type of data!", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error!", e)
        return student_data

    @staticmethod
    def output_student_courses(student_data: list):
        """ This function displays the current data in the file to the user

        Changelog (who, when, what)
        LBatista, 11.19.2023, created function

        return: None
        """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student["FirstName"]} 'f'{student["LastName"]} is enrolled in {student["CourseName"]}')
        print("-" * 50)
        print()


# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file

students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":
        IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_courses(student_data=students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
