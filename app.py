from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import speech_recognition as sr
import pyttsx3
import threading  # Import threading

# Initialize the Google Generative AI model
GOOGLE_API_KEY = "AIzaSyCipxZmb0iHDi9vukeeKbb77xSVxvFheZs-2"  # Replace with your actual API key
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", api_key=GOOGLE_API_KEY)

# Initialize pyttsx3
engine = pyttsx3.init()

def text_to_speech(text):
    """Convert text to speech using pyttsx3. Stop speaking if the word 'stop' is detected."""
    if "stop" in text.lower():  # Check if the word "stop" is in the text
        engine.stop()  # Stop speaking immediately
        st.warning("Speech stopped because the word 'stop' was detected.")
    else:
        engine.say(text)
        engine.runAndWait()

def handle_audio_input():
    recognizer = sr.Recognizer()
    
    # Listen for audio input
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source)
    
    try:
        # Recognize speech using Google Web Speech API
        text_input = recognizer.recognize_google(audio)
        st.success(f"Your text: {text_input}")
        
        # Display the user's input as text
        st.write("**User Input (Text):**")
        st.write(text_input)
        
        # Simulate AI response (replace with actual LLM logic)
        with st.spinner("AI Responding..."):
            response = llm.invoke(text_input)  # Replace with actual LLM logic
            response = str(response.content)  # Ensure response is a string
            
            # Display the AI's response as text
            st.write("**AI Response (Text):**")
            st.write(response)
            
            if response:
                # Run text-to-speech in a separate thread
                threading.Thread(target=text_to_speech, args=(response,)).start()
                
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Web Speech API; {e}")

# Streamlit App
st.title("Voice-Enabled Chatbot 🎙️🤖")

# Button to start listening
if st.button("🎤 Start Speaking", key="start_speaking_button"):  # Add a unique key
    with st.spinner("Listening..."):
        handle_audio_input()