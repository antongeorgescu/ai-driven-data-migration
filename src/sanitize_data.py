import pandas as pd
import re

# Load the CSV file
file_path_source = 'data/synthetic_data.csv'
df = pd.read_csv(file_path_source)

# Strip leading/trailing whitespace from all string fields
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Luhn algorithm for masking
def luhn_mask(value):
    def luhn_checksum(num):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(num)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    masked_value = ''.join(['*' if c.isdigit() else c for c in value])
    if luhn_checksum(re.sub(r'\D', '', value)) == 0:
        return masked_value
    return value

# Mask PII fields
def mask_name(name):
    parts = name.split()
    masked_parts = [p[0] + '*' * (len(p) - 2) + p[-1] if len(p) > 1 else p for p in parts]
    return ' '.join(masked_parts)

def mask_address(address):
    return re.sub(r'^\d+', lambda x: '*' * len(x.group()), address)

def mask_phone(phone):
    # Remove round brackets
    phone = phone.replace('(', '').replace(')', '')
    
    # Regular expression to match phone numbers with optional extensions
    phone_pattern = re.compile(r'(\d{3})([-.\s]?\d{3}[-.\s]?\d{4})( x\d+)?')
    match = phone_pattern.match(phone)
    if match:
        first_part = match.group(1)
        masked_part = '*' * len(match.group(2))
        extension = match.group(3) if match.group(3) else ''
        return first_part + masked_part + extension
    return phone

def mask_email(email):
    local, domain = email.split('@')
    domain_parts = domain.split('.')
    return local[:2] + '*' * (len(local) - 2) + '@' + domain_parts[0] + '.' + domain_parts[1]

df['Name'] = df['Name'].apply(mask_name)
df['Address'] = df['Address'].apply(mask_address)
df['Phone Number'] = df['Phone Number'].apply(mask_phone)
df['Email'] = df['Email'].apply(mask_email)

# Apply Luhn algorithm wherever applicable
df['Phone Number'] = df['Phone Number'].apply(luhn_mask)

# Save the sanitized data to a new CSV file
file_path_sanitized = 'data/sanitized_synthetic_data.csv'
df.to_csv(file_path_sanitized, index=False)

print("Data has been sanitized and saved to", file_path_sanitized)