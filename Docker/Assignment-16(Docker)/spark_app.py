from pyspark import SparkContext
import os


def remove_header(row):
    return row != header


def split_row(row):
    fields = row.split(",")

    employee_id = int(fields[0])
    name = fields[1]
    department = fields[2]
    salary = int(fields[3])

    return (employee_id, name, department, salary)


def get_salary(employee):
    return employee[3]


def department_salary_pair(employee):
    return (employee[2], employee[3])


def add_salaries(salary1, salary2):
    return salary1 + salary2


def format_employee(employee):
    return (
        "ID: "
        + str(employee[0])
        + ", Name: "
        + employee[1]
        + ", Department: "
        + employee[2]
        + ", Salary: "
        + str(employee[3])
    )


spark = SparkContext(appName="EmployeeRDDProcessing")

rdd = spark.textFile("employees.csv")  # Read CSV file

header = rdd.first()
data = rdd.filter(remove_header)  # Removing header

# Convert rows into tuples
employees = data.map(split_row)

# 1. Sort employees by salary in descending order
print("\nEmployees sorted by salary (descending):")

sorted_employees = employees.sortBy(keyfunc=get_salary, ascending=False)

for employee in sorted_employees.collect():
    print(format_employee(employee))

# 2. Total salary by department
print("\nDepartment-wise Total Salaries:")

department_totals = employees.map(department_salary_pair).reduceByKey(add_salaries)

for department, total in department_totals.collect():
    print(department + ": " + str(total))

# 3. Top 3 highest-paid employees
top_three = sorted_employees.take(3)

print("\nTop 3 Highest-Paid Employees:")

for employee in top_three:
    print(format_employee(employee))

# Save output to file
os.makedirs("output", exist_ok=True)

with open("output/top_3_employees.csv", "w") as file:
    for employee in top_three:
        file.write(format_employee(employee) + "\n")

spark.stop()
