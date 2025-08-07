def get_prompt(mode, input_text, target_lang=None):
    if mode == "translate":
        return (
            f"You are an expert translator. Translate the text to {target_lang or 'the target language'} "
            f"while preserving exact meaning, emotional tone, and cultural nuance.\n"
            f"If an idiom exists in the target language, use it.\n"
            f"Input:\n{input_text}"
        )

    elif mode == "poem":
        return (
            "You are a master poet. Convert the following into a beautiful, structured poem.\n"
            "Rules:\n"
            "- Preserve meaning and emotional tone.\n"
            "- Use vivid imagery and rhythm.\n"
            "- Output in 2–4 stanzas.\n"
            "Example:\n"
            "Input: I miss you every day.\n"
            "Output:\nEach dawn arrives yet feels untrue,\n"
            "Your shadow fades in morning dew.\n"
            "Though miles apart, you’re near in hue,\n"
            "In dreams, my heart still walks with you.\n\n"
            f"Now, Input:\n{input_text}"
        )

    elif mode == "song":
        return (
            "You are a lyricist. Turn the following into song lyrics.\n"
            "Rules:\n"
            "- Keep meaning and emotional tone.\n"
            "- Use repetition and rhymes.\n"
            "- Separate into verses and chorus.\n"
            "Example:\n"
            "Input: I miss you every day.\n"
            "Output:\n[Verse 1]\nI wake up and you’re still gone,\nThe night feels twice as long...\n"
            "[Chorus]\nEvery day, I miss you more,\nWaiting by that open door...\n\n"
            f"Now, Input:\n{input_text}"
        )

    elif mode == "shakespeare":
        return (
            "You are William Shakespeare reincarnated. Rewrite the text in authentic Elizabethan English.\n"
            "Rules:\n"
            "- Use archaic vocabulary and grammar.\n"
            "- Preserve meaning and tone.\n"
            "- Sound poetic and dramatic.\n"
            "Example:\n"
            "Input: I don't understand what's happening.\n"
            "Output: I comprehendeth not what strange events dost now unfold.\n\n"
            f"Now, Input:\n{input_text}"
        )

    elif mode == "casual":
        return (
            "Rewrite the text into a light, friendly, conversational tone.\n"
            "Rules:\n"
            "- Preserve meaning.\n"
            "- Use contractions and simple words.\n"
            "- Add warmth but avoid slang.\n"
            "Example:\n"
            "Input: I will be unable to attend the meeting tomorrow.\n"
            "Output: Hey, I can’t make it to the meeting tomorrow.\n\n"
            f"Now, Input:\n{input_text}"
        )

    elif mode == "formal":
        return (
            "Rewrite the text into a professional, formal tone.\n"
            "Rules:\n"
            "- Preserve meaning and tone.\n"
            "- Avoid contractions.\n"
            "- Use polished vocabulary.\n"
            "Example:\n"
            "Input: Hey, I can’t make it to the meeting tomorrow.\n"
            "Output: I regret to inform you that I will be unable to attend tomorrow’s meeting.\n\n"
            f"Now, Input:\n{input_text}"
        )

    elif mode == "rephrase":
        return (
            "Rephrase the following text to improve clarity and style.\n"
            "Rules:\n"
            "- Preserve meaning and tone.\n"
            "- Simplify without losing detail.\n"
            "Example:\n"
            "Input: Due to unforeseen circumstances, the project deadline may be affected.\n"
            "Output: The project deadline might change because of unexpected events.\n\n"
            f"Now, Input:\n{input_text}"
        )

    else:
        return input_text
