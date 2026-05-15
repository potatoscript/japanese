import random
import json
from datetime import datetime

# =========================
# JLPT N1 Grammar Database
# =========================

GRAMMAR_DATA = [
    {
        "grammar": "ただ～のみ",
        "meaning": "nothing but / all one can do is",
        "example": "結果を待つのみです。",
        "reading": "けっか を まつ のみ です。",
        "translation": "All we can do is wait for the result.",
        "quiz": "彼の成功をただ祈る（　　　）だ。",
        "answer": "のみ"
    },
    {
        "grammar": "～っぱなし",
        "meaning": "leave something as it is / continuously",
        "example": "電気をつけっぱなしで寝た。",
        "reading": "でんき を つけっぱなし で ねた。",
        "translation": "I slept with the light left on.",
        "quiz": "テレビをつけ（　　　）で出かけた。",
        "answer": "っぱなし"
    },
    {
        "grammar": "～てからというもの",
        "meaning": "ever since",
        "example": "日本へ来てからというもの、毎日忙しい。",
        "reading": "にほん へ きて からというもの、まいにち いそがしい。",
        "translation": "Ever since coming to Japan, every day has been busy.",
        "quiz": "転職してからというもの、（　　　）。",
        "answer": "毎日忙しい"
    },
    {
        "grammar": "～といったら",
        "meaning": "speaking of / when it comes to",
        "example": "昨日の暑さといったら、本当に大変だった。",
        "reading": "きのう の あつさ といったら、ほんとう に たいへん だった。",
        "translation": "Yesterday's heat was unbelievable.",
        "quiz": "今日の寒さ（　　　）、耐えられない。",
        "answer": "といったら"
    },
    {
        "grammar": "～としたところで",
        "meaning": "even if",
        "example": "今から急いだとしたところで、間に合わない。",
        "reading": "いま から いそいだ としたところで、まにあわない。",
        "translation": "Even if we hurry now, we won't make it.",
        "quiz": "今さら謝った（　　　）、遅い。",
        "answer": "としたところで"
    },
    {
        "grammar": "～にあたらない",
        "meaning": "not worth / no need to",
        "example": "驚くにあたらない。",
        "reading": "おどろく に あたらない。",
        "translation": "It's not surprising.",
        "quiz": "そんなことは驚く（　　　）。",
        "answer": "にあたらない"
    },
    {
        "grammar": "～んばかりだ",
        "meaning": "as if almost",
        "example": "彼は泣かんばかりに喜んだ。",
        "reading": "かれ は なかんばかり に よろこんだ。",
        "translation": "He was so happy he almost cried.",
        "quiz": "彼女は飛び上がらん（　　　）喜んだ。",
        "answer": "ばかりに"
    },
    {
        "grammar": "～つつも",
        "meaning": "although",
        "example": "悪いと知りつつも、やってしまった。",
        "reading": "わるい と しり つつも、やってしまった。",
        "translation": "Although I knew it was bad, I still did it.",
        "quiz": "危険だと知り（　　　）、挑戦した。",
        "answer": "つつも"
    },
    {
        "grammar": "～ないことには",
        "meaning": "unless",
        "example": "やってみないことには分からない。",
        "reading": "やってみない ことには わからない。",
        "translation": "You won't know unless you try.",
        "quiz": "食べてみない（　　　）、味は分からない。",
        "answer": "ことには"
    },
    {
        "grammar": "～にかけては",
        "meaning": "when it comes to",
        "example": "料理にかけては彼女が一番だ。",
        "reading": "りょうり に かけては かのじょ が いちばん だ。",
        "translation": "She is the best when it comes to cooking.",
        "quiz": "日本語（　　　）彼はクラスで一番だ。",
        "answer": "にかけては"
    },
    {
        "grammar": "～のみならず",
        "meaning": "not only but also",
        "example": "彼は英語のみならず、中国語も話せる。",
        "reading": "かれ は えいご のみならず、ちゅうごくご も はなせる。",
        "translation": "He can speak not only English but also Chinese.",
        "quiz": "彼女は歌（　　　）、ダンスも上手だ。",
        "answer": "のみならず"
    },
    {
        "grammar": "～ばかりに",
        "meaning": "simply because",
        "example": "彼を信じたばかりに失敗した。",
        "reading": "かれ を しんじた ばかりに しっぱい した。",
        "translation": "I failed simply because I trusted him.",
        "quiz": "油断した（　　　）、負けてしまった。",
        "answer": "ばかりに"
    },
    {
        "grammar": "～ようがない",
        "meaning": "there is no way to",
        "example": "証拠がなく、判断しようがない。",
        "reading": "しょうこ が なく、はんだん しよう が ない。",
        "translation": "There is no way to judge without evidence.",
        "quiz": "情報が少なく、確認しよう（　　　）。",
        "answer": "がない"
    },
    {
        "grammar": "～わりに",
        "meaning": "despite / for",
        "example": "彼は若いわりにしっかりしている。",
        "reading": "かれ は わかい わりに しっかり している。",
        "translation": "He is reliable for someone young.",
        "quiz": "この店は高い（　　　）、味は普通だ。",
        "answer": "わりに"
    },
    {
        "grammar": "～を通じて",
        "meaning": "throughout / through",
        "example": "一年を通じて暖かい。",
        "reading": "いちねん を つうじて あたたかい。",
        "translation": "It is warm throughout the year.",
        "quiz": "彼とは友人を（　　　）知り合った。",
        "answer": "通じて"
    },
]

SAVE_FILE = "jlpt_n1_progress.json"

def check_exit(user_input):
    return user_input.lower() in ["q", "exit", "menu"]


# =========================
# Save / Load Progress
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
# Study Mode
# =========================

def study_mode():
    print("\n========== STUDY MODE ==========")

    for item in GRAMMAR_DATA:
        print(f"\nGrammar: {item['grammar']}")
        print(f"Meaning: {item['meaning']}")
        print(f"Example: {item['example']}")
        print(f"Reading: {item['reading']}")
        print(f"Translation: {item['translation']}")
        #input("\nPress Enter for next grammar...")
        user_input = input("\nPress Enter for next grammar (q = menu): ")

        if check_exit(user_input):
            return


# =========================
# Quiz Mode
# =========================

def quiz_mode():
    progress = load_progress()

    print("\n========== QUIZ MODE ==========")

    questions = random.sample(GRAMMAR_DATA, min(10, len(GRAMMAR_DATA)))

    score = 0

    for index, item in enumerate(questions, start=1):
        print(f"\nQuestion {index}")
        print(item["quiz"])

        #user_answer = input("Your answer: ").strip()
        user_answer = input("Your answer (q = menu): ").strip()

        if check_exit(user_answer):
            return

        if user_answer == item["answer"]:
            print("✅ Correct!")
            score += 1
            progress["correct"] += 1
            result = "Correct"
        else:
            print("❌ Wrong")
            print(f"Correct answer: {item['answer']}")
            progress["wrong"] += 1
            result = "Wrong"

        progress["history"].append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "grammar": item["grammar"],
            "result": result
        })

    print("\n========== RESULT ==========")
    print(f"Your Score: {score}/{len(questions)}")

    save_progress(progress)


# =========================
# Review Weak Points
# =========================

def review_mode():
    progress = load_progress()

    print("\n========== REVIEW MODE ==========")

    wrong_grammar = []

    for history in progress["history"]:
        if history["result"] == "Wrong":
            wrong_grammar.append(history["grammar"])

    wrong_grammar = list(set(wrong_grammar))

    if not wrong_grammar:
        print("Excellent! No weak grammar recorded.")
        return

    for grammar in wrong_grammar:
        for item in GRAMMAR_DATA:
            if item["grammar"] == grammar:
                print(f"\nGrammar: {item['grammar']}")
                print(f"Meaning: {item['meaning']}")
                print(f"Example: {item['example']}")
                print(f"Translation: {item['translation']}")


# =========================
# Statistics
# =========================

def statistics_mode():
    progress = load_progress()

    total = progress["correct"] + progress["wrong"]

    print("\n========== STATISTICS ==========")
    print(f"Correct Answers : {progress['correct']}")
    print(f"Wrong Answers   : {progress['wrong']}")

    if total > 0:
        accuracy = (progress["correct"] / total) * 100
        print(f"Accuracy         : {accuracy:.2f}%")
    else:
        print("Accuracy         : No data yet")


# =========================
# Main Menu
# =========================

def main():
    while True:
        print("\n==============================")
        print(" JLPT N1 Grammar Trainer ")
        print("==============================")
        print("1. Study Mode")
        print("2. Quiz Mode")
        print("3. Review Weak Grammar")
        print("4. Statistics")
        print("5. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            study_mode()
        elif choice == "2":
            quiz_mode()
        elif choice == "3":
            review_mode()
        elif choice == "4":
            statistics_mode()
        elif choice == "5":
            print("Good luck with JLPT N1! 頑張って！")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
