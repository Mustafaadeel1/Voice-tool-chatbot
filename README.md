# Voice-Enabled Chatbot Code Explanation

This document provides an overview and explanation of the Python code for a **Voice-Enabled Chatbot**. The chatbot utilizes Google Generative AI, a speech-to-text library, and text-to-speech functionality.

---

## Code Breakdown

### 1. **Imports**
```python
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading
```
- **`ChatGoogleGenerativeAI`**: Interface for Google Generative AI (Gemini 2.0).
- **`streamlit`**: Framework for building interactive web applications.
- **`speech_recognition`**: Converts spoken audio into text.
- **`pyttsx3`**: Provides text-to-speech capabilities.
- **`threading`**: Allows concurrent execution of text-to-speech.

### 2. **Google Generative AI Model Initialization**
```python
GOOGLE_API_KEY = "<your-api-key>"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)
```
- Replace `<your-api-key>` with a valid Google API key to authenticate requests.
- The model is set to `gemini-2.0-flash-exp`.

### 3. **Text-to-Speech Function**
```python
def text_to_speech(text):
    if "stop" in text.lower():
        engine.stop()
        st.warning("Speech stopped because the word 'stop' was detected.")
    else:
        engine.say(text)
        engine.runAndWait()
```
- **`engine.stop()`**: Stops speaking if the word "stop" is detected in the response.
- **`engine.say()`**: Converts text to audio and speaks it out loud.
- **`engine.runAndWait()`**: Processes the speech queue.

### 4. **Audio Input Handling**
```python
def handle_audio_input():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source)

    try:
        text_input = recognizer.recognize_google(audio)
        st.success(f"Your text: {text_input}")

        st.write("**User Input (Text):**")
        st.write(text_input)

        with st.spinner("AI Responding..."):
            response = llm.invoke(text_input)
            response = str(response.content)

            st.write("**AI Response (Text):**")
            st.write(response)

            if response:
                threading.Thread(target=text_to_speech, args=(response,)).start()

    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Web Speech API; {e}")
```
- **Speech Recognition**:
  - `sr.Recognizer` converts speech to text.
  - `sr.Microphone` listens to audio input from the microphone.
- **Error Handling**:
  - `sr.UnknownValueError`: Triggered if audio cannot be understood.
  - `sr.RequestError`: Triggered if there is an issue with the API.
- **LLM Invocation**:
  - `llm.invoke()`: Sends the recognized text to the LLM and retrieves the response.
- **Multithreading**:
  - Starts a new thread for the text-to-speech function to avoid blocking other processes.

### 5. **Streamlit Interface**
```python
st.title("Voice-Enabled Chatbot 🎙️🤖")

if st.button("🎤 Start Speaking", key="start_speaking_button"):
    with st.spinner("Listening..."):
        handle_audio_input()
```
- **Title**: Displays the app title.
- **Button**: Starts the process of listening for audio input when clicked.
- **Spinner**: Indicates that the system is processing input.

---

## Features
1. **Speech-to-Text**: Captures audio from the microphone and converts it to text.
2. **Text-to-Speech**: Reads out the AI's response using `pyttsx3`.
3. **AI Interaction**: Uses Google Generative AI to respond to user queries.
4. **Streamlit UI**: Provides an interactive interface for users.
5. **Error Handling**: Handles various errors related to audio processing and API usage.

---

## Improvements
- **Authentication**: Replace the placeholder API key with a secure key.
- **Response Logic**: Customize AI responses for specific tasks or use cases.
- **UI Enhancements**: Add input fields for text and configuration options.
- **Audio Output**: Enhance audio quality with advanced libraries like `gTTS` or `pyttsx3` settings.

---

## Dependencies
Install the required libraries using the following command:
```bash
pip install langchain-google-genai streamlit speechrecognition pyttsx3
```
