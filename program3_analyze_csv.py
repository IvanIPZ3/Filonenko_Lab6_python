from datetime import datetime, date

import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = "employees.csv"

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
        return -1

    today = date.today()
    years = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        years -= 1
    return years


def main():
    # 1. Read CSV file
    try:
        df = pd.read_csv(CSV_FILE, delimiter=";", encoding="utf-8")
    except FileNotFoundError:
        print(f"Cannot open CSV file: '{CSV_FILE}' not found.")
        return
    except Exception as exc:
        print("Error while reading CSV file:", exc)
        return

    print("Ok. CSV file loaded successfully.")

    # 2. Add age column
    df["Вік"] = df["Дата народження"].apply(calculate_age)

    # ---------- 2.1 Count by gender ----------
    gender_counts = df["Стать"].value_counts().sort_index()
    print("\nКількість співробітників за статтю:")
    for gender, count in gender_counts.items():
        print(f"{gender}: {count}")

    # Plot gender diagram
    plt.figure()
    gender_counts.plot(kind="bar")
    plt.title("Кількість співробітників за статтю")
    plt.xlabel("Стать")
    plt.ylabel("Кількість")
    plt.tight_layout()
    plt.show()

    # ---------- 2.2 Count by age category ----------
    def get_age_category(age: int) -> str:
        """Return name of age category for given age."""
        for category_name, cond in AGE_SHEETS.items():
            if cond(age):
                return category_name
        return "unknown"

    df["Вікова_категорія"] = df["Вік"].apply(get_age_category)

    age_counts = df["Вікова_категорія"].value_counts().reindex(
        ["younger_18", "18-45", "45-70", "older_70", "unknown"]
    ).fillna(0).astype(int)

    print("\nКількість співробітників за віковими категоріями:")
    for category, count in age_counts.items():
        print(f"{category}: {count}")

    # Plot age category diagram
    plt.figure()
    age_counts.plot(kind="bar")
    plt.title("Кількість співробітників за віковими категоріями")
    plt.xlabel("Вікова категорія")
    plt.ylabel("Кількість")
    plt.tight_layout()
    plt.show()

    # ---------- 2.3 Count by gender + age category ----------
    crosstab = pd.crosstab(df["Вікова_категорія"], df["Стать"])

    print("\nКількість співробітників за віком і статтю:")
    print(crosstab)

    # build grouped bar chart: one figure, one axis
    fig, ax = plt.subplots()  # create single figure window

    crosstab.loc[["younger_18", "18-45", "45-70", "older_70"]].plot(
        kind="bar",
        ax=ax  # draw on this axis, not creating new figure
    )

    ax.set_title("Кількість співробітників за віком і статтю")
    ax.set_xlabel("Вікова категорія")
    ax.set_ylabel("Кількість")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
