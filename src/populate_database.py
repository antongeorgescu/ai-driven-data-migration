import pandas as pd
import pyodbc
import argparse
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
server = os.getenv('DB_SERVER')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')

# Connection string
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Load the CSV file
file_path = 'data/sanitized_synthetic_data.csv'
df = pd.read_csv(file_path)

# Strip leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Establish a database connection
try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Empty the whole database
    cursor.execute("DELETE dbo.Student")
    cursor.execute("DELETE dbo.Communication")
    cursor.execute("DELETE dbo.EducationInstitution")
    cursor.execute("DELETE dbo.Province")
    cursor.execute("DELETE dbo.LoanInfo")
    cursor.execute("DELETE dbo.StudyInfo")   
    conn.commit()

    # Insert data into the Province table
    provinces = df['Province'].unique()
    for province in provinces:
        cursor.execute("INSERT INTO Province (Province) VALUES (?)", province)
    conn.commit()

    # Insert data into the EducationInstitution table
    education_institutions = df[['College', 'College Code', 'Province']].drop_duplicates()
    for index, row in education_institutions.iterrows():
        cursor.execute("""
            INSERT INTO EducationInstitution (College, CollegeCode, ProvinceID)
            VALUES (?, ?, (SELECT ProvinceID FROM Province WHERE Province = ?))
        """, row['College'], row['College Code'], row['Province'])
    conn.commit()

    # Insert data into the Communication table
    communications = df[['Phone Number', 'Email']].drop_duplicates()
    for index, row in communications.iterrows():
        cursor.execute("INSERT INTO Communication (PhoneNumber, Email) VALUES (?, ?)", row['Phone Number'], row['Email'])
    conn.commit()

    # Insert data into the LoanInfo table
    loan_infos = df[['Enrollment Type', 'Loan Amount', 'Year Started', 'Loan Balance', 'Percentage Paid']].drop_duplicates()
    for index, row in loan_infos.iterrows():
        cursor.execute("""
            INSERT INTO LoanInfo (EnrollmentType, LoanAmount, YearStarted, LoanBalance, PercentagePaid)
            VALUES (?, ?, ?, ?, ?)
        """, row['Enrollment Type'], row['Loan Amount'], row['Year Started'], row['Loan Balance'], row['Percentage Paid'])
    conn.commit()

    # Insert data into the StudyInfo table
    study_infos = df[['Program of Study', 'Program Code', 'College Code']].drop_duplicates()
    for index, row in study_infos.iterrows():
        cursor.execute("INSERT INTO StudyInfo (ProgramOfStudy, ProgramCode, CollegeCode) VALUES (?, ?, ?)", row['Program of Study'], row['Program Code'], row['College Code'])
    conn.commit()

    # Insert data into the Student table
    students = df[['Name', 'Address', 'Phone Number', 'Email', 'Enrollment Type', 'Loan Amount', 'Year Started', 'Loan Balance', 'Percentage Paid', 'Program of Study', 'Program Code', 'College', 'College Code', 'Province']]
    for index, row in students.iterrows():
        first_name, last_name = row['Name'].split(' ', 1)
        cursor.execute("""
            INSERT INTO Student (FirstName, LastName, Address, LoanInfoID, CommunicationID, StudyInfoID, EducationInstitutionID)
            VALUES (?, ?, ?, 
            (SELECT LoanInfoID FROM LoanInfo WHERE EnrollmentType = ? AND LoanAmount = ? AND YearStarted = ? AND LoanBalance = ? AND PercentagePaid = ?),
            (SELECT CommunicationID FROM Communication WHERE PhoneNumber = ? AND Email = ?),
            (SELECT StudyInfoID FROM StudyInfo WHERE ProgramOfStudy = ? AND ProgramCode = ? AND CollegeCode = ?),
            (SELECT EducationInstitutionID FROM EducationInstitution WHERE College = ? AND CollegeCode = ? AND ProvinceID = (SELECT ProvinceID FROM Province WHERE Province = ?))
            )
        """, first_name, last_name, row['Address'], row['Enrollment Type'], row['Loan Amount'], row['Year Started'], row['Loan Balance'], row['Percentage Paid'], row['Phone Number'], row['Email'], row['Program of Study'], row['Program Code'], row['College Code'], row['College'], row['College Code'], row['Province'])
    conn.commit()
    print("Database has been populated with sanitized data.")
except pyodbc.Error as e:
    print(f"Error: {e}")
    with open('error_log.txt', 'a') as f:
        f.write(f"Error: {e}\n")
    print(f"Error in populating the database:{e}")
finally:
    # Close the database connection
    if 'cursor' in locals() and cursor:
        cursor.close()
    if 'conn' in locals() and conn:
        conn.close()
