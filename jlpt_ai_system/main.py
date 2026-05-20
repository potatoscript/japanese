import random
import json
from datetime import datetime, timedelta

from grammar_data import GRAMMAR_DATA
from vocab_data import VOCAB_DATA

SAVE_FILE = "progress.json"

# =========================
# SRS SETTINGS
# =========================

SRS_LEVELS = {

    1: 1,     # 1 day
    2: 3,     # 3 days
    3: 7,     # 1 week
    4: 14,    # 2 weeks
    5: 30     # 1 month
}

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
# UPDATE SRS
# =========================

def update_srs(

    progress,

    grammar,

    is_correct

):

    # =========================
    # CREATE SRS DATA
    # =========================

    if grammar not in progress["srs"]:

        progress["srs"][grammar] = {

            "level": 1,

            "next_review":
            datetime.now().strftime(
                "%Y-%m-%d"
            )
        }

    srs_data = progress["srs"][grammar]

    # =========================
    # CORRECT
    # =========================

    if is_correct:

        if srs_data["level"] < 5:

            srs_data["level"] += 1

    # =========================
    # WRONG
    # =========================

    else:

        srs_data["level"] = 1

    # =========================
    # NEXT REVIEW DATE
    # =========================

    days = SRS_LEVELS[
        srs_data["level"]
    ]

    next_date = (

        datetime.now()

        + timedelta(days=days)

    ).strftime("%Y-%m-%d")

    srs_data["next_review"] = next_date



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

    print("\n========== DIFFICULTY ==========")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. All")

    difficulty_choice = input(
        "\nSelect difficulty: "
    ).strip()

    if difficulty_choice == "1":
        selected_difficulty = "easy"

    elif difficulty_choice == "2":
        selected_difficulty = "medium"

    elif difficulty_choice == "3":
        selected_difficulty = "hard"

    else:
        selected_difficulty = "all"

    # =========================
    # FILTER QUESTIONS
    # =========================

    if selected_difficulty == "all":

        filtered_questions = GRAMMAR_DATA

    else:

        filtered_questions = [

            item for item in GRAMMAR_DATA

            if item["difficulty"]
            == selected_difficulty
        ]

    # =========================
    # CHECK EMPTY
    # =========================

    if len(filtered_questions) == 0:

        print(
            "\nNo grammar found "
            "for this difficulty."
        )

        return

    # =========================
    # RANDOM QUESTIONS
    # =========================

    questions = random.sample(
        filtered_questions,
        min(5, len(filtered_questions))
    )

    score = 0

    for index, item in enumerate(
        questions,
        start=1
    ):

        print(
            f"\n========== QUESTION {index} =========="
        )

        print(item["quiz"])

        correct_answer = item["answer"]

        all_wrong_answers = [

            item["answer"]

            for item in GRAMMAR_DATA

            if item["answer"] != correct_answer
        ]

        random.shuffle(all_wrong_answers)

        wrong_answers = all_wrong_answers[:3]

        choices = (
            wrong_answers
            + [correct_answer]
        )

        random.shuffle(choices)

        for i, choice in enumerate(
            choices,
            start=1
        ):

            print(f"{i}. {choice}")

        user_input = input(
            "\nSelect answer "
            "(q = menu): "
        ).strip()

        if check_exit(user_input):
            return

        if not user_input.isdigit():

            print("Invalid input.")

            continue

        user_index = int(user_input) - 1

        if (
            user_index < 0
            or user_index >= len(choices)
        ):

            print("Invalid choice.")

            continue

        selected_answer = choices[user_index]

        # =========================
        # CORRECT
        # =========================

        if selected_answer == correct_answer:

            print("✅ Correct!")

            score += 1

            progress["correct"] += 1

            update_srs(
                progress,
                item["grammar"],
                True
            )
                       
            result = "Correct"

        # =========================
        # WRONG
        # =========================

        else:

            print("❌ Wrong")

            print(
                "Correct Answer:",
                correct_answer
            )

            progress["wrong"] += 1

            update_srs(
                progress,
                item["grammar"],
                False
            )

            result = "Wrong"

        progress["history"].append({

            "date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "grammar": item["grammar"],

            "difficulty":
            item["difficulty"],

            "result": result
        })

    print("\n========== RESULT ==========")

    print(
        f"Score: "
        f"{score}/{len(questions)}"
    )

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

def weak_grammar_review():

    progress = load_progress()

    print(
        "\n========== "
        "WEAK GRAMMAR "
        "=========="
    )

    wrong_grammar = {}

    # =========================
    # COUNT WRONG ANSWERS
    # =========================

    for item in progress["history"]:

        if item["result"] == "Wrong":

            grammar = item["grammar"]

            if grammar not in wrong_grammar:

                wrong_grammar[grammar] = 0

            wrong_grammar[grammar] += 1

    # =========================
    # EMPTY
    # =========================

    if len(wrong_grammar) == 0:

        print(
            "\nExcellent!"
        )

        print(
            "No weak grammar yet."
        )

        return

    # =========================
    # SORT
    # =========================

    sorted_grammar = sorted(

        wrong_grammar.items(),

        key=lambda x: x[1],

        reverse=True
    )

    # =========================
    # DISPLAY
    # =========================

    for grammar, count in sorted_grammar:

        print(
            f"\n{grammar}"
        )

        print(
            f"Wrong Count: {count}"
        )

        for item in GRAMMAR_DATA:

            if item["grammar"] == grammar:

                print(
                    "Meaning:",
                    item["meaning"]
                )

                print(
                    "Example:",
                    item["example"]
                )

# =========================
# DAILY REVIEW
# =========================

def daily_review():

    progress = load_progress()

    print(
        "\n========== "
        "DAILY REVIEW "
        "=========="
    )

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )

    due_grammar = []

    # =========================
    # FIND DUE ITEMS
    # =========================

    for grammar, srs_data in (

        progress["srs"].items()

    ):

        if (
            srs_data["next_review"]
            <= today
        ):

            due_grammar.append(grammar)

    # =========================
    # NO REVIEWS
    # =========================

    if len(due_grammar) == 0:

        print(
            "\nNo reviews today!"
        )

        return

    print(
        f"\nYou have "
        f"{len(due_grammar)} "
        f"reviews today."
    )

    # =========================
    # QUIZ LOOP
    # =========================

    for grammar_name in due_grammar:

        item = None

        for data in GRAMMAR_DATA:

            if (
                data["grammar"]
                == grammar_name
            ):

                item = data

                break

        if item is None:
            continue

        print(
            "\n------------------"
        )

        print(item["quiz"])

        answer = input(
            "\nYour answer: "
        ).strip()

        if answer == item["answer"]:

            print("✅ Correct")

            update_srs(
                progress,
                grammar_name,
                True
            )

        else:

            print("❌ Wrong")

            print(
                "Correct:",
                item["answer"]
            )

            update_srs(
                progress,
                grammar_name,
                False
            )

    save_progress(progress)


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
        print("4. Daily Review")
        print("5. Weak Grammar Review")
        print("6. Statistics")
        print("7. Exit")

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
            daily_review()

        elif choice == "5":
            weak_grammar_review()

        elif choice == "6":
            statistics_mode()

        elif choice == "7":

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