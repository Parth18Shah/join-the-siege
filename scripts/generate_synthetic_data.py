import pandas as pd
import random
from faker import Faker
fake = Faker()

LABELS = ['bank_statement', 'invoice', 'drivers_license', 'unknown file']
TEXT_TEMPLATES = {
    'bank_statement': lambda: f"Bank Statement Account Number: {fake.random_number(digits=10)} Balance: ${fake.random_int(min=1000, max=10000)} Transaction: {fake.sentence(nb_words=6)} Description: {fake.paragraph()}",
    'invoice': lambda: f"Invoice Item: {fake.word()} Quantity: {fake.random_int(min=1, max=20)} Amount: ${fake.random_number(digits=4)} Notes: {fake.sentence(nb_words=10)}",
    'drivers_license': lambda: f"Driver's License Name: {fake.name()} License Number: {fake.random_number(digits=9)} DOB: {fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=80)} Address: {fake.address()}",
    'unknown file': lambda: fake.text(max_nb_chars=300)
}

def generate_synthetic_row(label):
    # Generate text content based on label
    text_content = TEXT_TEMPLATES[label]()
    return {
        'text_content': text_content,
        'label': label,
    }

def generate_synthetic_data(num_samples=1000):
    data = []
    for _ in range(num_samples):
        label = random.choice(LABELS)
        data.append(generate_synthetic_row(label))

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv('./files/synthetic_data.csv', index=False)
    print("Synthetic data saved to synthetic_data.csv")
