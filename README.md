Of course, here is the updated, highly detailed README.md for the "Creative Text Engine" project, incorporating the additional details you provided.

# 🧠 Creative Text Engine

A generative AI-powered application that creatively transforms text across languages, styles, and tones — built with open-source LLMs and Streamlit. This project was developed as part of a 24-hour hackathon.

-----

## 🎯 Problem Statement

The challenge was to build an AI translator that not only translates text but also preserves the original voice and style of the content. Beyond literal translation, the goal was to create a tool that can adapt tone and style, for instance, by transforming modern English into Shakespearean English or converting prose into poetry, all while maintaining the core meaning and nuance of the original text.

-----

## ✨ Features

  - **💬 Chat Mode**: Engage in open-ended conversations and ask general questions. This mode allows for a free-form dialogue with the AI.
  - 🌍 **Translate**: Seamlessly translate text between various languages while preserving the original tone and meaning.
  - ✍️ **Rephrase**: Rephrase text in different styles to enhance clarity and impact.
  - 🎭 **Shakespearean Mode**: Rewrite any text in the iconic style of William Shakespeare.
  - 🪶 **Prose to Poem Conversion**: Transform ordinary prose into a lyrical poem.
  - 🎵 **Songify**: Turn plain text into song lyrics.
  - 🔁 **Creative Rephrasing**: Preserve the core meaning of a text while shifting its expression for a fresh perspective.
  - 🎛️ **Interactive Interface**: A user-friendly, ChatGPT-like experience with interactive buttons for each mode.

-----

## 📦 Tech Stack

| Layer | Tech | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | The core framework for building the interactive web application. |
| **LLM Backend** | Gemini 2.5 Flash | The generative model used for all text transformations. |
| **Deployment** | Hugging Face Spaces | The application is set up for continuous deployment to Hugging Face Spaces using GitHub Actions. |
| **Version Control** | Git & GitHub | Used for source code management and version control. |
| **Styling** | CSS | Custom CSS is used to create a modern, dark-themed user interface. |

-----

## 🚀 Getting Started

### 🔧 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SakshamAnand/creative-text-engine.git
    cd creative-text-engine
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up your environment:**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```
    GEMINI_API_KEY="YOUR_API_KEY"
    ```
4.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

-----

## 🧠 How It Works

The Creative Text Engine is a web application built with **Streamlit** that allows users to transform text in various creative ways. Here’s a breakdown of how it works:

1.  **User Interface**: The frontend is created with Streamlit and features a simple, chat-like interface where users can input text and select a transformation mode from a dropdown menu.

2.  **Mode Selection**: The `modes.py` file defines a dictionary of available modes, such as "Translate," "Poemify," and "Shakespearean."

3.  **Backend Processing**: When a user submits text, the Streamlit app sends the input and the selected mode to the `generate_response` function in the `model_handler.py` file.

4.  **Prompt Engineering**: The `get_prompt` function in `prompts.py` constructs a specific prompt tailored to the selected mode. For example, if the "Poemify" mode is chosen, the prompt will instruct the AI to convert the text into a poem.

5.  **API Integration**: The `model_handler.py` file then makes a POST request to the Gemini API with the generated prompt. The API key is securely loaded from a `.env` file.

6.  **Response Handling**: The application processes the JSON response from the Gemini API, extracts the transformed text, and displays it in the chat interface. Error handling is in place to manage any issues with the API call.

-----

### Prompt Engineering and Testing

A critical component of this project was the development of highly optimized prompts to ensure the integrity of the user's input. We conducted extensive testing with over **1,000 prompts** to fine-tune the instructions given to the AI for each specific task.

Our primary objective was to ensure that the **tone and context** of the user's input were preserved throughout the transformation process. To achieve this, we implemented a rigorous testing methodology:

1.  **Semantic Similarity Analysis**: The user's original input and the model's output were passed to a sentence transformer model.
2.  **Cosine Similarity**: We then calculated the cosine similarity between the embeddings of the input and output to quantitatively measure how well the meaning was preserved.
3.  **Prompt Optimization**: Based on these similarity scores, we iteratively refined the prompts, selecting the shortest and most effective prompts for each mode to ensure both accuracy and efficiency.

This data-driven approach allowed us to craft prompts that consistently produce high-quality, context-aware results.

-----

## 🌐 Modes Supported

| Mode | Description |
| :--- | :--- |
| **Chat** | Engage in an open-ended conversation with the AI. |
| **Translate** | Translates the input text to a different language while preserving the original meaning and tone. |
| **Poemify** | Converts a given text into a well-structured poem. |
| **Songify** | Transforms the input text into song lyrics. |
| **Shakespeare** | Rewrites the text in the classic style of Shakespearean English. |
| **Formal ↔ Casual** | Toggles the tone of the text between professional and relaxed. |
| **Rephrase** | Offers a creative restyling of the text while keeping the original meaning intact. |

-----

## 🤝 Team

  - **Saksham Anand**: LLM, Prompt Engineering, Backend
  - **Rudra Raj Krishna**: Streamlit UI, Deployment, Integration

-----

## 📄 License

This project is open source and free to use under the MIT License.
