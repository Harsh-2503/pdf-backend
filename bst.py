import csv
from collections import defaultdict


def find_duplicate_questions(csv_file):
    temp = []
    duplicate_questions = defaultdict(list)

    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            question = row['question']
            id_ = row['id']
            duplicate_questions[question].append(id_)
            temp.append(int(id_))

    print(temp)
            

    for question, ids in duplicate_questions.items():
        if len(ids) > 1:
            print(f"Duplicate Question: {question}")
            print(f"IDs: {', '.join(ids)}")
            print()


if __name__ == "__main__":
    csv_file_path = "./aptitude_question.csv"  # Replace with the actual path to your CSV file
    find_duplicate_questions(csv_file_path)
