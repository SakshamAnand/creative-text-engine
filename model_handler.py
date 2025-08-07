def generate_response(message, mode):
    """
    Placeholder response generator.
    Replace this with actual LLM logic later.
    """
    if mode == "Translate":
        return f"🔤 Translated version of: '{message}'"
    elif mode == "Poemify":
        return f"🪄 Poemified version of: '{message}'"
    elif mode == "Emojify":
        return f"😄 Emojified version of: '{message}'"
    elif mode == "Summarize":
        return f"📝 Summary of: '{message}'"
    elif mode == "Rephrase":
        return f"♻️ Rephrased: '{message}'"
    else:
        return f"🤖 Default mode: '{message}'"
