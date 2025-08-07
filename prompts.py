def get_prompt(mode, input_text, target_lang=None):
    if mode == "translate":
        return f"Translate the following text to the language the user intends, while preserving the original meaning and tone:\n\n{input_text}"
    elif mode == "poem":
        return f"Convert the following text into a poem, while preserving the original meaning and tone:\n\n{input_text}"
    elif mode == "song":
        return f"Transform the following text into song lyrics, while preserving the original meaning and tone:\n\n{input_text}"
    elif mode == "shakespeare":
        return f"Rewrite the following text in Shakespearean English, while preserving the original meaning and tone:\n\n{input_text}"
    elif mode == "casual":
        return f"Rewrite the following text in a casual, conversational tone, while preserving the original meaning and tone:\n\n{input_text}"
    elif mode == "formal":
        return f"Rewrite the following text in a formal, professional tone, while preserving the original meaning and tone:\n\n{input_text}"
    elif mode == "rephrase":
        return f"Rephrase the following text for improved clarity and style, while preserving the original meaning and tone:\n\n{input_text}"
    else:
        return f"{input_text}"
