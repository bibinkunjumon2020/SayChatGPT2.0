from saybot import openai,os,logging

def generate_chat(prompt):
    # Set up OpenAI API key
    logging.info("Contacting ChatGPT 3.5 Turbo")
    openai.api_key = os.getenv("API_OPENAI")
    try:
        message_response="Server Error" # To avoid HTTPSConnectionPool(host='api.openai.com', port=443): Read timed out
       
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role":"user","content":prompt}
            ],
            temperature=0.7,
            
        )
        answer = response['choices'][0]["message"]["content"]
        logging.info(answer)
        if response is not None and len(answer) > 0:
            message_response = answer
        else:
            message_response = "Sorry, no response could be generated."
    except Exception as e:
        logging.error("error occurred while generating the response"+e)
        message_response = "Sorry, an error occurred while generating the response.\n"+ e
    finally:
        return message_response
    
    