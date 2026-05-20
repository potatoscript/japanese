# STEP 1 — Create the Project Folder

Create this structure manually:

```text id="yrn1b8"
jlpt_ai_system/
│
├── main.py
├── grammar_data.py
├── vocab_data.py
├── progress.json
```

---

# STEP 2 — Create grammar_data.py

Create file:

```text id="nk6qch"
grammar_data.py
```

Paste this:

```python id="vlm7s9"
GRAMMAR_DATA = [
    {
        "grammar": "～まい",
        "meaning": "probably not / will not",
        "example": "彼は来るまい。",
        "reading": "かれ は くる まい。",
        "translation": "He probably won't come.",
        "quiz": "彼はもう戻る（　　　）。",
        "answer": "まい",
        "difficulty": "hard"
    },
    {
        "grammar": "～ばかりに",
        "meaning": "simply because",
        "example": "彼を信じたばかりに失敗した。",
        "reading": "かれ を しんじた ばかりに しっぱいした。",
        "translation": "I failed simply because I trusted him.",
        "quiz": "油断した（　　　）、負けてしまった。",
        "answer": "ばかりに",
        "difficulty": "medium"
    },
    {
        "grammar": "～つつも",
        "meaning": "although",
        "example": "悪いと知りつつも、やってしまった。",
        "reading": "わるい と しり つつも、やってしまった。",
        "translation": "Although I knew it was bad, I still did it.",
        "quiz": "危険だと知り（　　　）、挑戦した。",
        "answer": "つつも",
        "difficulty": "hard"
    }
]
```

Save.

---

# STEP 3 — Create vocab_data.py

Create:

```text id="r55caa"
vocab_data.py
```

Paste:

```python id="xvfxjg"
VOCAB_DATA = [
    {
        "word": "逆らう",
        "reading": "さからう",
        "meaning": "to oppose"
    },
    {
        "word": "重んじる",
        "reading": "おもんじる",
        "meaning": "to value"
    },
    {
        "word": "かさばる",
        "reading": "かさばる",
        "meaning": "to take up space"
    }
]
```

Save.

---

# STEP 4 — Create progress.json

Create:

```text id="t52p1s"
progress.json
```

Paste:

```json id="8x0dj7"
{
    "correct": 0,
    "wrong": 0,
    "history": []
}
```

Save.

---

# STEP 5 — Create main.py

Create:

```text id="i1x7j3"
main.py
```

Now paste THIS EXACT CODE.

```python id="c9ebp2"
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
```

Save.

---

# STEP 6 — RUN THE PROGRAM

Open terminal inside folder.

Run:

```bash id="d79np3"
python main.py
```

You should see:

```text id="o1dg6m"
==============================
 JLPT N1 AI TRAINER
==============================
1. Study Grammar
2. Grammar Quiz
3. Vocabulary Quiz
4. Statistics
5. Exit
```

---

# STEP 7 — TEST EVERYTHING

Test:

* Study mode
* Quiz mode
* Vocab mode
* Statistics
* q exit system

---

Next we add:

* Difficulty selector
* Weak grammar review
* Better vocabulary quiz
* Daily review system
* Spaced repetition (SRS)

---

# STEP 8 — ADD DIFFICULTY SELECTOR

Open:

```text id="gvl4c7"
main.py
```

---

# STEP 9 — REPLACE grammar_quiz()

Find:

```python id="o02yo1"
def grammar_quiz():
```

Delete the ENTIRE function.

Replace with this FULL upgraded version.

```python id="nsvh8q"
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

        wrong_answers = []

        while len(wrong_answers) < 3:

            random_item = random.choice(
                GRAMMAR_DATA
            )

            wrong = random_item["answer"]

            if (
                wrong != correct_answer
                and wrong not in wrong_answers
            ):
                wrong_answers.append(wrong)

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
```

Save.

---

# STEP 10 — TEST DIFFICULTY MODE

Run:

```bash id="59kvr0"
python main.py
```

Try:

* Easy
* Medium
* Hard
* All

---

# STEP 11 — ADD WEAK GRAMMAR REVIEW

Now add NEW function BELOW `statistics_mode()`

Paste this BELOW statistics.

```python id="6o9rqx"
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
```

Save.

---

# STEP 12 — ADD MENU OPTION

Inside:

```python id="3e9xmo"
def main():
```

Find:

```python id="yvmd4w"
print("4. Statistics")
print("5. Exit")
```

Replace with:

```python id="67eecx"
print("4. Weak Grammar Review")
print("5. Statistics")
print("6. Exit")
```

---

# STEP 13 — UPDATE MENU LOGIC

Find:

```python id="d7n2wd"
elif choice == "4":
    statistics_mode()

elif choice == "5":
```

Replace with:

```python id="j8y9x4"
elif choice == "4":
    weak_grammar_review()

elif choice == "5":
    statistics_mode()

elif choice == "6":
```

Save.

---

# STEP 14 — TEST WEAK GRAMMAR SYSTEM

Run:

```bash id="3pnw9w"
python main.py
```

Do some wrong answers intentionally.

Then open:

```text id="s0ovxu"
Weak Grammar Review
```

You should see:

* your weak grammar
* wrong counts
* examples
* meanings

---

# WHAT YOU JUST BUILT

You now have:

✅ Modular system
✅ Multiple quiz modes
✅ Difficulty system
✅ Statistics
✅ Weakness analysis
✅ Progress tracking
✅ Dynamic random questions

This is already similar to a real language learning app backend.

---

# NEXT STEP

Next we build:

# STEP 15 — REAL SRS SYSTEM

We will add:

* review dates
* daily review queue
* memory levels
* automatic scheduling

Like:

* Anki
* Bunpro
* WaniKani

This is where your app becomes truly powerful.
