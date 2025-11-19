import sys
from datetime import datetime, date

import pandas as pd

CSV_FILE = "employees.csv"
XLSX_FILE = "employees.xlsx"

AGE_SHEETS = {
    "younger_18": lambda age: age < 18,
    "18-45":      lambda age: 18 <= age < 45,
    "45-70":      lambda age: 45 <= age < 70,
    "older_70":   lambda age: age >= 70,
}


def calculate_age(birthdate_str: str) -> int:
    """Calculate age in full years from 'YYYY-MM-DD' string."""
    try:
        birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d").date()
    except ValueError:
        # If date format is wrong, return -1 (invalid age)
        return -1

    today = date.today()
    years = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        years -= 1
    return years


def main():
    # 1. Read CSV
    try:
        df = pd.read_csv(CSV_FILE, delimiter=";", encoding="utf-8")
    except FileNotFoundError:
        print(f"Cannot open CSV file: '{CSV_FILE}' not found.")
        return
    except Exception as exc:
        print("Error while reading CSV file:", exc)
        return

    # 2. Add 'Вік' column
    df["Вік"] = df["Дата народження"].apply(calculate_age)

    # 3. Prepare DataFrame for Excel sheets (only necessary columns)
    base_columns = ["Прізвище", "Ім’я", "По батькові", "Дата народження", "Вік"]
    df_base = df[base_columns].copy()

    # 4. Write XLSX with multiple sheets
    try:
        with pd.ExcelWriter(XLSX_FILE, engine="openpyxl") as writer:
            # Sheet "all" – all employees
            df_base.to_excel(writer, sheet_name="all", index=False)

            # Other sheets – age categories
            for sheet_name, condition in AGE_SHEETS.items():
                mask = df_base["Вік"].apply(condition)
                df_category = df_base[mask].copy()
                df_category.to_excel(writer, sheet_name=sheet_name, index=False)

        print("Ok. XLSX file created successfully.")

    except Exception as exc:
        print("Cannot create XLSX file:", exc)


if __name__ == "__main__":
    main()
