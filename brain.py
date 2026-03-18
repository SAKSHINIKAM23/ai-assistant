def get_reply(text):
    text = text.lower()

    # Energy / mood
    if any(w in text for w in ["tired", "exhausted", "burnout"]):
        return "Rest is productive too 😌 Take a 20 min break then reassess."
    if any(w in text for w in ["stressed", "overwhelmed", "anxious"]):
        return "Breathe. Pick ONE thing to focus on right now. What is it? 🎯"
    if any(w in text for w in ["bored", "unmotivated", "lazy"]):
        return "Start with just 5 minutes. Momentum beats motivation 💪"
    if any(w in text for w in ["happy", "great", "amazing", "productive"]):
        return "Love that energy! Keep riding it 🔥 What's next on your list?"

    # Tasks
    if any(w in text for w in ["remind", "task", "todo", "add"]):
        return "Got it! Send me the task and I'll save it ✅"
    if any(w in text for w in ["what are my tasks", "show tasks", "my list"]):
        return "FETCH_TASKS"  # handled in bot.py

    # WPI / Study
    if any(w in text for w in ["study", "homework", "assignment", "exam", "quiz"]):
        return "Study mode ON 📚 Want me to set a focus reminder in 25 min?"
    if any(w in text for w in ["ml", "deep learning", "research", "medvault"]):
        return "MedVault grind! 🧠 Break it into small steps — what's the first one?"

    # Content creation
    if any(w in text for w in ["instagram", "content", "reel", "post"]):
        return "Content brain activated 🎥 Captured anything interesting today?"

    # Greetings
    if any(w in text for w in ["hi", "hello", "hey"]):
        return "Hey Sakshi! 👋 What are we tackling today?"
    if any(w in text for w in ["bye", "good night", "cya"]):
        return "Rest well! 🌙 You did good today. Tomorrow we go again 💪"

    # Default
    return "Interesting... tell me more, or type 'tasks' to see your list 🤔"