
# 🧠 WikiGuess – Interactive Wikipedia Quiz Game

**WikiGuess** is a Python-based interactive quiz game where players guess terms based on real Wikipedia content. The game is designed to enhance engagement, boost learning, and make acquiring knowledge fun through input-based guessing logic.

---

## 🎮 Features

- 🔍 Clues generated dynamically from Wikipedia article summaries
- 🎯 User guesses the correct term or concept
- ✅ Feedback on correct/incorrect guesses
- 🔄 Replayable with random topics
- 📚 Educational and engaging

---

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Internet connection (for Wikipedia API access)

### Install Dependencies

```bash
pip install wikipedia
````

### Run the Game

```bash
python wiki_quiz.py
```

---

## 🧩 How It Works

1. The game fetches a summary from a random or predefined Wikipedia article.
2. The title of the article is hidden.
3. The user reads the summary and tries to guess the term.
4. The game tells the user if the guess is correct and optionally gives hints or allows retries.

---

## ✏️ Example Gameplay

```
Clue: This is a type of programming language used widely in data science and web development. It emphasizes readability.

Your guess: python

✅ Correct! The term was: Python (programming language)
```

---

## 📦 File Structure

```
wiki_guess/
├── wiki_quiz.py       # Main game logic
├── requirements.txt   # Dependencies (optional)
└── README.md          # Project info
```

---

## 🧠 Why This Game?

This project blends **educational content** with **gamification** to support:

* Active recall learning
* Exposure to new topics
* Vocabulary reinforcement

Ideal for students, trivia fans, and lifelong learners!

---

## 🙌 Contributions

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## 📄 License

MIT License

---

## 🔗 Credits

* Uses the [`wikipedia`](https://pypi.org/project/wikipedia/) Python package
* Content sourced from [Wikipedia](https://wikipedia.org)

```
