import csv
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime
import os

# Функція для визначення вікової категорії
def get_age_category(age):
    if age < 20:
        return "до 20"
    elif 20 <= age < 30:
        return "20-29"
    elif 30 <= age < 40:
        return "30-39"
    elif 40 <= age < 50:
        return "40-49"
    elif 50 <= age < 60:
        return "50-59"
    else:
        return "60 і більше"

# Функція для читання CSV-файлу
def read_csv_file(filename):
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не існує.")
        return None
    try:
        with open(filename, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            header = next(reader)  # Пропускаємо заголовок
            data = [row for row in reader]
            print("Файл відкрито: Ok")
            return data
    except Exception as e:
        print(f"Помилка при відкритті файлу: {e}")
        return None

# Функція для підрахунку співробітників за статтю
def count_by_gender(data):
    genders = [row[3] for row in data]
    gender_count = Counter(genders)

    print(f"Кількість чоловіків: {gender_count['male']}")
    print(f"Кількість жінок: {gender_count['female']}")

    labels = ['Чоловіки', 'Жінки']
    sizes = [gender_count['male'], gender_count['female']]

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['blue', 'pink'])
    plt.title('Співробітники за статтю')
    plt.show()

# Функція для підрахунку співробітників за віковими категоріями
def count_by_age_category(data):
    current_year = datetime.now().year
    age_categories = [
        get_age_category(current_year - datetime.strptime(row[4], '%Y-%m-%d').year)
        for row in data
    ]
    age_category_count = Counter(age_categories)

    print("Кількість співробітників за віковими категоріями:")
    for category, count in age_category_count.items():
        print(f"{category}: {count}")

    labels = age_category_count.keys()
    sizes = age_category_count.values()

    plt.figure(figsize=(8, 6))
    plt.bar(labels, sizes, color='green')
    plt.title('Кількість співробітників за віковими категоріями')
    plt.xlabel('Вікові категорії')
    plt.ylabel('Кількість')
    plt.show()

# Функція для підрахунку співробітників кожної статі у кожній віковій категорії
def count_gender_by_age_category(data):
    current_year = datetime.now().year
    gender_age_category_count = {'male': Counter(), 'female': Counter()}

    for row in data:
        gender = row[3]
        birth_year = datetime.strptime(row[4], '%Y-%m-%d').year
        age_category = get_age_category(current_year - birth_year)
        gender_age_category_count[gender][age_category] += 1

    print("Кількість співробітників кожної статі у кожній віковій категорії:")
    for gender, age_data in gender_age_category_count.items():
        print(f"\nСтать: {gender}")
        for category, count in age_data.items():
            print(f"{category}: {count}")

        # Візуалізація даних
        labels = age_data.keys()
        sizes = age_data.values()

        plt.figure(figsize=(8, 6))
        plt.bar(labels, sizes, color='blue' if gender == 'male' else 'pink')
        plt.title(f'Кількість {gender} за віковими категоріями')
        plt.xlabel('Вікові категорії')
        plt.ylabel('Кількість')
        plt.show()

# Основна функція
def main():
    filename = 'personal_data.csv'
    data = read_csv_file(filename)

    if data:
        count_by_gender(data)
        count_by_age_category(data)
        count_gender_by_age_category(data)

# Запуск програми
if __name__ == '__main__':
    main()
