import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import pandas as pd
import time
from prompt import prompt
GOOGLE_API_KEY = "AIzaSyCEGF6KwvQrx3ePHMggUwZc5RfEFsP2YL0"

def is_pivot_gemini(table_file: str, head_num: int = 8, model_name: str = 'gemini-pro') -> bool:
    
    """Check if it need pivot operation using google gemini"""

    global GOOGLE_API_KEY

    data = pd.read_csv(table_file)
    result_string = data.head(head_num).to_csv(index=False, header=True).strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    response = None
    prompt_text = prompt["pivot"] + str(result_string)

    while response is None:
        try:
            response = model.generate_content(prompt_text)

        except ResourceExhausted:
            print("Quota exhausted. Waiting for the next minute to continue.")
            time.sleep(60)  # Wait for 1 minute before retrying

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    if (len(response.candidates) == 0):
        return str("(False)")

    return response.text

def is_stack_gemini(table_file: str, head_num: int = 8, model_name: str = 'gemini-pro'):
    
    """Check if it need pivot operation using google gemini"""

    global GOOGLE_API_KEY

    data = pd.read_csv(table_file)
    result_string = data.head(head_num).to_csv(index=False, header=True).strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    response = None
    prompt_text = prompt["stack"] + str(result_string)

    while response is None:
        try:
            response = model.generate_content(prompt_text)

        except ResourceExhausted:
            print("Quota exhausted. Waiting for the next minute to continue.")
            time.sleep(60)  # Wait for 1 minute before retrying

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    if (len(response.candidates) == 0):
        return str("(False)")
      
    return response.text

def is_wide_to_long_gemini(table_file: str, head_num: int = 8, model_name: str = 'gemini-pro'):
    
    """Check if it need pivot operation using google gemini"""

    global GOOGLE_API_KEY

    data = pd.read_csv(table_file)
    result_string = data.head(head_num).to_csv(index=False, header=True).strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    response = None
    prompt_text = prompt["wide_to_long"] + str(result_string)

    while response is None:
        try:
            response = model.generate_content(prompt_text)

        except ResourceExhausted:
            print("Quota exhausted. Waiting for the next minute to continue.")
            time.sleep(60)  # Wait for 1 minute before retrying

        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    if (len(response.candidates) == 0):
        return str("(False)")

    return response.text

def is_transpose_gemini(table_file: str, head_num: int = 8, model_name: str = 'gemini-pro') -> bool:
    
    """Check if it need pivot operation using google gemini"""

    global GOOGLE_API_KEY

    data = pd.read_csv(table_file)
    result_string = data.head(head_num).to_csv(index=False, header=True).strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    response = None
    prompt_text = prompt["transpose"] + str(result_string)

    while response is None:
        try:
            response = model.generate_content(prompt_text)

        except ResourceExhausted:
            print("Quota exhausted. Waiting for the next minute to continue.")
            time.sleep(60)  # Wait for 1 minute before retrying

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    if (len(response.candidates) == 0):
        return str("(False)")

    return response.text


def is_explode_gemini(table_file: str, head_num: int = 8, model_name: str = 'gemini-pro') -> bool:
    
    """Check if it need pivot operation using google gemini"""
    global GOOGLE_API_KEY

    data = pd.read_csv(table_file)
    result_string = data.head(head_num).to_csv(index=False, header=True).strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    response = None
    prompt_text = prompt["explode"] + str(result_string)

    while response is None:
        try:
            response = model.generate_content(prompt_text)

        except ResourceExhausted:
            print("Quota exhausted. Waiting for the next minute to continue.")
            time.sleep(60)  # Wait for 1 minute before retrying
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    if (len(response.candidates) == 0):
        return str("(False)")

    return response.text

def is_ffill_gemini(table_file: str, head_num: int = 8, model_name: str = 'gemini-pro') -> bool:
    
    """Check if it need pivot operation using google gemini"""

    global GOOGLE_API_KEY

    data = pd.read_csv(table_file)
    result_string = data.head(head_num).to_csv(index=False, header=True).strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    response = None
    prompt_text = prompt["ffill"] + str(result_string)

    while response is None:
        try:
            response = model.generate_content(prompt_text)
        except ResourceExhausted:
            print("Quota exhausted. Waiting for the next minute to continue.")
            time.sleep(60)  # Wait for 1 minute before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    if (len(response.candidates) == 0):
        return str("(False)")

    return response.text

def is_subtitle_gemini(table_file: str, head_num: int = 8, model_name: str = 'gemini-pro') -> bool:
    
    """Check if it need pivot operation using google gemini"""
    global GOOGLE_API_KEY

    data = pd.read_csv(table_file)
    result_string = data.head(head_num).to_csv(index=False, header=True).strip()

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel(model_name)
    
    response = None
    prompt_text = prompt["subtitle"] + str(result_string)

    while response is None:
        try:
            response = model.generate_content(prompt_text)
        except ResourceExhausted:
            print("Quota exhausted. Waiting for the next minute to continue.")
            time.sleep(60)  # Wait for 1 minute before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    if (len(response.candidates) == 0):
        return str("(False)")

    return response.text

# is_subtitle_gpt("Tables/subtitle1.csv")
def main():
    is_pivot_gemini("Tables/subtitle1.csv")

if __name__ == '__main__':
    main()
    