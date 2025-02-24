import pandas as pd
import pyodbc
import argparse

# Parse command line arguments for username and password
# parser = argparse.ArgumentParser(description='Populate database with sanitized data.')
# parser.add_argument('--username', required=True, help='Database username')
# parser.add_argument('--password', required=True, help='Database password')
# args = parser.parse_args()

# Database connection parameters
server = 'STDLJHXX0T3\SQLEXPRESS'
database = 'StudentLoanDB'
# username = args.username
# password = args.password
username = 'sparxuser'
password = 'dana2606'

# Connection string
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Load the CSV file
file_path = 'data/sanitized_synthetic_data.csv'
df = pd.read_csv(file_path)

# Strip leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Establish a database connection
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()

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
students = df[['FirstName', 'LastName', 'Address', 'Phone Number', 'Email', 'Enrollment Type', 'Loan Amount', 'Year Started', 'Loan Balance', 'Percentage Paid', 'Program of Study', 'Program Code', 'College', 'College Code', 'Province']]
for index, row in students.iterrows():
    cursor.execute("""
        INSERT INTO Student (FirstName, LastName, Address, LoanInfoID, CommunicationID, StudyInfoID, EducationInstitutionID)
        VALUES (?, ?, ?, 
            (SELECT LoanInfoID FROM LoanInfo WHERE EnrollmentType = ? AND LoanAmount = ? AND YearStarted = ? AND LoanBalance = ? AND PercentagePaid = ?),
            (SELECT CommunicationID FROM Communication WHERE PhoneNumber = ? AND Email = ?),
            (SELECT StudyInfoID FROM StudyInfo WHERE ProgramOfStudy = ? AND ProgramCode = ? AND CollegeCode = ?),
            (SELECT EducationInstitutionID FROM EducationInstitution WHERE College = ? AND CollegeCode = ? AND ProvinceID = (SELECT ProvinceID FROM Province WHERE Province = ?))
        )
    """, row['FirstName'], row['LastName'], row['Address'], row['Enrollment Type'], row['Loan Amount'], row['Year Started'], row['Loan Balance'], row['Percentage Paid'], row['Phone Number'], row['Email'], row['Program of Study'], row['Program Code'], row['College Code'], row['College'], row['College Code'], row['Province'])
conn.commit()

# Close the database connection
cursor.close()
conn.close()

print("Database has been populated with sanitized data.")