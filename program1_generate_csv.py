import csv
import random
from datetime import datetime, date, timedelta

from faker import Faker

# Create Faker with Ukrainian locale
fake = Faker(locale="uk_UA")

# Constants
CSV_FILE = "employees.csv"
RECORDS_COUNT = 500
FEMALE_RATIO = 0.4  # 40% female, 60% male
START_YEAR = 1938
END_YEAR = 2008

# Patronymics dictionary: at least 20 male and 20 female
MALE_PATRONYMICS = [
    "Іванович", "Петрович", "Олексійович", "Андрійович", "Олегович",
    "Сергійович", "Миколайович", "Володимирович", "Анатолійович", "Юрійович",
    "Вікторович", "Богданович", "Романович", "Тарасович", "Ігорович",
    "Степанович", "Олександрович", "Григорович", "Дмитрович", "Михайлович"
]

FEMALE_PATRONYMICS = [
    "Іванівна", "Петрівна", "Олексіївна", "Андріївна", "Олегівна",
    "Сергіївна", "Миколаївна", "Володимирівна", "Анатоліївна", "Юріївна",
    "Вікторівна", "Богданівна", "Романівна", "Тарасівна", "Ігорівна",
    "Степанівна", "Олександрівна", "Григорівна", "Дмитрівна", "Михайлівна"
]


def random_birthdate(start_year: int, end_year: int) -> date:
    """Return a random date between 1 Jan start_year and 31 Dec end_year."""
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    days_range = (end_date - start_date).days
    random_days = random.randint(0, days_range)
    return start_date + timedelta(days=random_days)


def get_patronymic(gender: str) -> str:
    """Return patronymic according to gender ('Чоловіча' or 'Жіноча')."""
    if gender == "Жіноча":
        return random.choice(FEMALE_PATRONYMICS)
    return random.choice(MALE_PATRONYMICS)


def generate_gender_list(total: int, female_ratio: float):
    """
    Create a shuffled list of genders with given female ratio.
    Example: 40% female, 60% male.
    """
    females = int(total * female_ratio)
    males = total - females
    genders = ["Жіноча"] * females + ["Чоловіча"] * males
    random.shuffle(genders)
    return genders


def main():
    # Prepare header with Ukrainian column names
    header = [
        "Прізвище",
        "Ім’я",
        "По батькові",
        "Стать",
        "Дата народження",
        "Посада",
        "Місто проживання",
        "Адреса проживання",
        "Телефон",
        "Email",
    ]

    genders = generate_gender_list(RECORDS_COUNT, FEMALE_RATIO)

    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            writer.writerow(header)

            for gender in genders:
                # Generate names according to gender
                if gender == "Жіноча":
                    last_name = fake.last_name_female()
                    first_name = fake.first_name_female()
                else:
                    last_name = fake.last_name_male()
                    first_name = fake.first_name_male()

                patronymic = get_patronymic(gender)
                birthdate = random_birthdate(START_YEAR, END_YEAR)

                job_title = fake.job()
                city = fake.city()
                address = fake.street_address()
                phone = fake.phone_number()
                email = fake.email()

                # Save date as ISO format YYYY-MM-DD for easier parsing later
                row = [
                    last_name,
                    first_name,
                    patronymic,
                    gender,
                    birthdate.strftime("%Y-%m-%d"),
                    job_title,
                    city,
                    address,
                    phone,
                    email,
                ]
                writer.writerow(row)

        print(f"Ok. File '{CSV_FILE}' created with {RECORDS_COUNT} records.")

    except Exception as exc:
        print("Error while creating CSV file:", exc)


if __name__ == "__main__":
    main()
