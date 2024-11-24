# Custom exception for when a student is not found
class StudentNotFoundError(Exception):
    pass


# Custom exception for invalid grade inputs
class InvalidGradeError(Exception):
    pass


# Define the Student class to handle individual student records
class Student:
    def __init__(self, name):
        self.name = name
        self.grades = {}

    # Method to add or update a grade for a specific subject
    def add_grade(self, subject, grade):
        if 0 <= grade <= 100:
            self.grades[subject] = grade
        else:
            raise InvalidGradeError("Grade must be between 0 and 100.")

    # Calculate the average grade for the student
    def calculate_average(self):
        if self.grades:
            return sum(self.grades.values()) / len(self.grades)
        else:
            return 0

    # Print student details
    def display(self):
        average = self.calculate_average()
        print(f"{self.name.capitalize()}: Grades: {self.grades}, Average: {average:.2f}")


# Define the Gradebook class to manage multiple students and provide gradebook operations
class Gradebook:
    def __init__(self, subjects):
        self.subjects = subjects
        self.students = {}
        self.highest_grades = {subject: -1 for subject in subjects}
        self.lowest_grades = {subject: 101 for subject in subjects}
        self.subject_totals = {subject: 0.0 for subject in subjects}
        self.total_grade = 0.0

    # Method to add a new student
    def add_student(self, name):
        if name not in self.students:
            self.students[name] = Student(name)
        else:
            print("Student already exists!")

    # Method to add or update a grade for a student
    def add_grade(self, name, subject, grade):
        if name in self.students:
            student = self.students[name]
            try:
                student.add_grade(subject, grade)
                self.subject_totals[subject] += grade
                self.total_grade += grade
                self.update_highest_lowest(subject, grade)
            except InvalidGradeError as e:
                print(e)
        else:
            raise StudentNotFoundError(f"Student '{name}' not found.")

    # Update highest and lowest grades
    def update_highest_lowest(self, subject, grade):
        if grade > self.highest_grades[subject]:
            self.highest_grades[subject] = grade
        if grade < self.lowest_grades[subject]:
            self.lowest_grades[subject] = grade

    # Calculate and display the average grade for the class
    def calculate_class_average(self):
        num_grades = len(self.students) * len(self.subjects)
        return self.total_grade / num_grades if num_grades > 0 else 0

    # Display details of all students
    def display_all_students(self):
        for student in self.students.values():
            student.display()

    # Display grades for a specific student
    def display_student(self, name):
        if name in self.students:
            self.students[name].display()
        else:
            raise StudentNotFoundError(f"Student '{name}' not found.")

    # Remove a student
    def remove_student(self, name):
        if name in self.students:
            del self.students[name]
            print(f"{name.capitalize()} has been removed from the class.")
        else:
            raise StudentNotFoundError(f"Student '{name}' not found.")

    # Search for a student by name
    def search_student(self, name):
        try:
            self.display_student(name)
        except StudentNotFoundError as e:
            print(e)

    # Sort students by a specified criteria (name or average)
    def sort_students(self, by='name'):
        sorted_students = list(self.students.values())
        if by == 'name':
            sorted_students.sort(key=lambda student: student.name)
        elif by == 'average':
            sorted_students.sort(key=lambda student: student.calculate_average(), reverse=True)
        print(f"\nStudents sorted by {by.capitalize()}:")
        for student in sorted_students:
            student.display()

    # Display the average grades per subject
    def display_subject_averages(self):
        print("\nAverage grades per Subject:")
        for subject in self.subjects:
            subject_avg = self.subject_totals[subject] / len(self.students) if len(self.students) > 0 else 0
            print(f"{subject} average: {subject_avg:.2f}")

        print("\nHighest and Lowest Grades:")
        for subject in self.subjects:
            print(f"{subject} - Highest: {self.highest_grades[subject]}, Lowest: {self.lowest_grades[subject]}")


# Main program logic to interact with the Gradebook
def main():
    subjects = ['Math', 'English', 'Science']
    gradebook = Gradebook(subjects)

    # Initial input for class size and students
    num_students = int(input("Enter the number of students in the class: "))
    for _ in range(num_students):
        while True:
            name = input("Enter the name of the student: ").strip().lower()
            if not name.isdigit():
                gradebook.add_student(name)
                for subject in subjects:
                    while True:
                        try:
                            grade = float(input(f"Enter {name.capitalize()}'s grade for {subject}: "))
                            gradebook.add_grade(name, subject, grade)
                            break
                        except ValueError:
                            print("Invalid input. Please enter a numeric value between 0 and 100.")
                        except InvalidGradeError as e:
                            print(e)
                break
            else:
                print("Invalid name. Student names cannot be numbers.")

    # Interactive menu for managing students and grades
    while True:
        print("\nOptions:")
        print("1. Add a new student.")
        print("2. Update a student's grades.")
        print("3. Remove a student.")
        print("4. Search for a student.")
        print("5. Display subject averages and class average.")
        print("6. Sort students by name or average.")
        print("7. Exit")

        option = input("Choose an option: ")


        if option == '1':
            name = input("Enter the name of the new student: ").strip().lower()
            if name not in gradebook.students:
                gradebook.add_student(name)
                for subject in subjects:
                    while True:
                        try:
                            grade = float(input(f"Enter {name.capitalize()}'s grade for {subject}: "))
                            gradebook.add_grade(name, subject, grade)
                            break
                        except ValueError:
                            print("Invalid input. Please enter a numeric value.")
                        except InvalidGradeError as e:
                            print(e)
            else:
                print("Student already exists.")
        elif option == '2':
            name = input("Enter the name of the student to update: ").strip().lower()
            if name in gradebook.students:
                for subject in subjects:
                    while True:
                        try:
                            grade = float(input(f"Enter {name.capitalize()}'s new grade for {subject}: "))
                            gradebook.add_grade(name, subject, grade)
                            break
                        except ValueError:
                            print("Invalid input. Please enter a numeric value.")
                        except InvalidGradeError as e:
                            print(e)
            else:
                print("Student not found.")
        elif option == '3':
            name = input("Enter the name of the student to remove: ").strip().lower()
            try:
                gradebook.remove_student(name)
            except StudentNotFoundError as e:
                print(e)
        elif option == '4':
            name = input("Search student: ").strip().lower()
            gradebook.search_student(name)
        elif option == '5':
            gradebook.display_subject_averages()
            class_avg = gradebook.calculate_class_average()
            print(f"\nOverall class average grade: {class_avg:.2f}")
        elif option == '6':
            sort_criteria = input("Sort by 'name' or 'average': ").strip().lower()
            if sort_criteria in ['name', 'average']:
                gradebook.sort_students(by=sort_criteria)
            else:
                print("Invalid sort criteria.")
        elif option == '7':
            break
        else:
            print("Invalid option. Please try again.")


# Run the program
main()
