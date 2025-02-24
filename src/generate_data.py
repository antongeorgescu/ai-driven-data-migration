import pandas as pd
import random
from faker import Faker

fake = Faker('en_CA')

# Define the provinces and cities
provinces_cities = {
    'ON': ['Toronto', 'Ottawa', 'Mississauga', 'Brampton', 'Hamilton'],
    'AB': ['Calgary', 'Edmonton', 'Red Deer', 'Lethbridge', 'St. Albert'],
    'NS': ['Halifax', 'Sydney', 'Truro', 'New Glasgow', 'Glace Bay'],
    'MB': ['Winnipeg', 'Brandon', 'Steinbach', 'Thompson', 'Portage la Prairie'],
    'PE': ['Charlottetown', 'Summerside', 'Stratford', 'Cornwall', 'Montague']
}

# Define the enrollment types
enrollment_types = ['NSL', 'CAL']

# Define the programs of study and their codes
programs_of_study = {
    'Biochemistry': 'BIOCHE',
    'Engineering': 'ENGRNG',
    'Computer Technology': 'COMTEC',
    'Social Studies': 'SOCSTD',
    'Political Science': 'POLSCI',
    'Climate Change': 'CLIMCH',
    'Physics': 'PHYSIC',
    'Philosophy': 'PHILOS'
}

# Define the colleges and their codes
colleges = {
    'University of Toronto': 'UOTON',
    'Queens University': 'QUEEN',
    'University of Alberta': 'UALBE',
    'Dalhousie University': 'DALHO',
    'University of Manitoba': 'UMANI',
    'Holland College': 'HOLCO'
}

# Define phone number formats
phone_formats = [
    '### ###-####',
    '(###) ###-####',
    '(###) ###-#### x####',
    '### ### ####'
]

# Generate the dataset
data = []
for _ in range(1500):  # Generate 1500 records
    name = fake.name()
    province = random.choice(list(provinces_cities.keys()))
    city = random.choice(provinces_cities[province])
    address = f"{fake.street_address()}, {city}, {province}, {fake.postalcode()}"
    phone_number = fake.numerify(random.choice(phone_formats))
    email = fake.email()
    enrollment_type = random.choice(enrollment_types)
    year_started = random.randint(2019, 2023)
    loan_amount = random.randint(10000, 28000)
    loan_balance = random.randint(int(loan_amount * 0.2), loan_amount)
    percentage_paid = f"{int(((loan_amount - loan_balance) / loan_amount) * 100)}%"
    program_of_study = random.choice(list(programs_of_study.keys()))
    program_code = programs_of_study[program_of_study]
    college = random.choice(list(colleges.keys()))
    college_code = colleges[college]
    
    data.append([name, address, phone_number, email, enrollment_type, loan_amount, year_started, loan_balance, percentage_paid, program_of_study, program_code, college, college_code, province])

# Create a DataFrame
columns = ['Name', 'Address', 'Phone Number', 'Email', 'Enrollment Type', 'Loan Amount', 'Year Started', 'Loan Balance', 'Percentage Paid', 'Program of Study', 'Program Code', 'College', 'College Code', 'Province']
df = pd.DataFrame(data, columns=columns)

# Save the dataset to a CSV file
file_path = 'data/synthetic_data.csv'
df.to_csv(file_path, index=False)

print(f"Data has been generated and saved to {file_path}")