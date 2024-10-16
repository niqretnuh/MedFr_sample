import streamlit as st
import google.generativeai as genai

# Initialize the Gemini API with the user's API key
def initialize_gemini(gemini_api_key):
    genai.configure(api_key=gemini_api_key)
    return genai.GenerativeModel('gemini-pro')

# Function to load preset prompts from text files
def load_preset_prompt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Main UI of the app
def main():
    st.title("Medieval French-English Translation Tool")
    st.write("A tool for researchers to translate documents between Medieval French and English. Please enter your Google Gemini API key and select your translation preferences. Instructions on creating a new API key can be found here: https://aistudio.google.com/app/apikey")

    # Input for API key
    api_key = st.text_input("Enter your API key", type="password")

    # Selection for translation direction
    translation_direction = st.radio("Translation Direction", ('Medieval French to English', 'English to Medieval French'))
    
    # Dropdown for location and time period
    location_time = st.selectbox("Select Location/Time Period", 
                                 ('Francien',
                                  'England in the 11th Century - Anglo Norman',
                                  'South of France in the 13th Century - Occitan',
                                  'Picard',
                                  'Late Medieval French (14th-15th Century)'))

    poem_prose = st.selectbox("Output Format", ('Poem', 'Prose'))

    # Load the preset prompt based on user selection
    if location_time == 'Francien':
        preset_prompt_file = "francien_to_english.txt" if translation_direction == 'Medieval French to English' else "english_to_francien.txt"
    elif location_time == 'England in the 11th Century - Anglo Norman':
        preset_prompt_file = "anglo_norman_to_english.txt" if translation_direction == 'Medieval French to English' else "english_to_anglo_norman.txt"
    elif location_time == 'South of France in the 13th Century - Occitan':
        preset_prompt_file = "occitan_to_english.txt" if translation_direction == 'Medieval French to English' else "english_to_occitan.txt"
    elif location_time == 'Picard':
        preset_prompt_file = "picard_to_english.txt" if translation_direction == 'Medieval French to English' else "english_to_picard.txt"
    elif location_time == 'Late Medieval French (14th-15th Century)':
        preset_prompt_file = "late_french_to_english.txt" if translation_direction == 'Medieval French to English' else "english_to_late_french.txt"
    
    preset_prompt = load_preset_prompt(preset_prompt_file) + f" return the translation in {poem_prose} format only!"
    
    # Text input for translation or document upload
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Input text or upload document for translation")
        text_to_translate = st.text_area("Text to translate", height=300)
        uploaded_file = st.file_uploader("Or upload a document (text files only)", type=['txt'])
        
        if uploaded_file is not None:
            # If a file is uploaded, read the file and set the text_to_translate variable
            text_to_translate = str(uploaded_file.read(), 'utf-8')
    
    # Translate button always visible
    translate_button_clicked = st.button("Translate")

    if api_key and text_to_translate and translate_button_clicked:
        model = initialize_gemini(api_key)
        # Append the user's text to the preset prompt and send it to the model
        full_prompt = preset_prompt + "\n\n" + text_to_translate
        response = model.generate_content(
            full_prompt
        )

        # Display the translated text
        with col2:
            st.write("Translated text")
            st.text_area("Result", value=response.text, height=300)
    else:
        with col2:
            st.write("Translated text will appear here")

if __name__ == "__main__":
    main()
