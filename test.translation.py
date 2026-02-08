from translation_service import translate_query_to_english, translate_response_to_language, SUPPORTED_LANGUAGES

def test_service():
    print(f"✅ Supported Languages: {SUPPORTED_LANGUAGES}")
    
    test_query = "भूजल स्तर क्या है?" # "What is the groundwater level?" in Hindi
    test_lang = "hi"
    
    try:
        print(f"\nTesting Translation to English...")
        eng_text = translate_query_to_english(test_query, test_lang)
        print(f"Input (HI): {test_query}")
        print(f"Output (EN): {eng_text}")
        
        print(f"\nTesting Translation back to Hindi...")
        hi_text = translate_response_to_language("The water level is stable.", test_lang)
        print(f"Input (EN): The water level is stable.")
        print(f"Output (HI): {hi_text}")
        
        print("\n✨ SERVICE IS WORKING!")
    except Exception as e:
        print(f"\n❌ SERVICE FAILED!")
        print(f"Error details: {e}")

if __name__ == "__main__":
    test_service()