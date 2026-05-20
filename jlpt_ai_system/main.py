import random
import json
from datetime import datetime

from grammar_data import GRAMMAR_DATA
from vocab_data import VOCAB_DATA

SAVE_FILE = "progress.json"


# =========================
# LOAD / SAVE
# =========================

def load_progress():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        return {
            "correct": 0,
            "wrong": 0,
            "history": []
        }


def save_progress(progress):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=4)


# =========================
# EXIT CHECK
# =========================

def check_exit(user_input):
    return user_input.lower() in ["q", "exit", "menu"]


# =========================
# STUDY MODE
# =========================

def study_mode():

    print("\n========== STUDY MODE ==========")

    for item in GRAMMAR_DATA:

        print("\n----------------------")
        print("Grammar      :", item["grammar"])
        print("Meaning      :", item["meaning"])
        print("Example      :", item["example"])
        print("Reading      :", item["reading"])
        print("Translation  :", item["translation"])

        user_input = input(
            "\nPress Enter for next grammar (q = menu): "
        )

        if check_exit(user_input):
            return


# =========================
# GRAMMAR QUIZ
# =========================

def grammar_quiz():

    progress = load_progress()

    questions = random.sample(
        GRAMMAR_DATA,
        min(5, len(GRAMMAR_DATA))
    )

    score = 0

    for index, item in enumerate(questions, start=1):

        print(f"\n========== QUESTION {index} ==========")

        print(item["quiz"])

        correct_answer = item["answer"]

        wrong_answers = []

        while len(wrong_answers) < 3:

            random_item = random.choice(GRAMMAR_DATA)

            wrong = random_item["answer"]

            if (
                wrong != correct_answer
                and wrong not in wrong_answers
            ):
                wrong_answers.append(wrong)

        choices = wrong_answers + [correct_answer]

        random.shuffle(choices)

        for i, choice in enumerate(choices, start=1):
            print(f"{i}. {choice}")

        user_input = input(
            "\nSelect answer number (q = menu): "
        )

        if check_exit(user_input):
            return

        if not user_input.isdigit():
            print("Invalid input.")
            continue

        user_index = int(user_input) - 1

        if user_index < 0 or user_index >= len(choices):
            print("Invalid choice.")
            continue

        selected_answer = choices[user_index]

        if selected_answer == correct_answer:

            print("✅ Correct!")

            score += 1

            progress["correct"] += 1

            result = "Correct"

        else:

            print("❌ Wrong")
            print("Correct Answer:", correct_answer)

            progress["wrong"] += 1

            result = "Wrong"

        progress["history"].append({
            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "grammar": item["grammar"],
            "result": result
        })

    print("\n========== RESULT ==========")
    print(f"Score: {score}/{len(questions)}")

    save_progress(progress)


# =========================
# VOCAB QUIZ
# =========================

def vocab_quiz():

    print("\n========== VOCAB QUIZ ==========")

    question = random.choice(VOCAB_DATA)

    print("\nWord:", question["word"])

    answer = input(
        "Meaning (q = menu): "
    ).strip()

    if check_exit(answer):
        return

    if answer.lower() == question["meaning"]:

        print("✅ Correct!")

    else:

        print("❌ Wrong")
        print(
            "Correct Meaning:",
            question["meaning"]
        )


# =========================
# STATISTICS
# =========================

def statistics_mode():

    progress = load_progress()

    total = (
        progress["correct"]
        + progress["wrong"]
    )

    print("\n========== STATISTICS ==========")

    print("Correct :", progress["correct"])
    print("Wrong   :", progress["wrong"])

    if total > 0:

        accuracy = (
            progress["correct"] / total
        ) * 100

        print(
            f"Accuracy : {accuracy:.2f}%"
        )

    else:

        print("No statistics yet.")


# =========================
# MAIN MENU
# =========================

def main():

    while True:

        print("\n==============================")
        print(" JLPT N1 AI TRAINER ")
        print("==============================")
        print("1. Study Grammar")
        print("2. Grammar Quiz")
        print("3. Vocabulary Quiz")
        print("4. Statistics")
        print("5. Exit")

        choice = input(
            "\nSelect option: "
        ).strip()

        if choice == "1":
            study_mode()

        elif choice == "2":
            grammar_quiz()

        elif choice == "3":
            vocab_quiz()

        elif choice == "4":
            statistics_mode()

        elif choice == "5":

            print(
                "\nGood luck with JLPT N1!"
            )

            break

        else:

            print("Invalid option.")


# =========================
# START PROGRAM
# =========================

if __name__ == "__main__":
    main()