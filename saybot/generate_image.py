from saybot import openai,os,logging

def generate_image(prompt):
    # Set up OpenAI API key
    logging.info("Contacting GPT image")
    openai.api_key = os.getenv("API_OPENAI")
    print(openai.api_key)
    try:
        message_response="Server Error" # To avoid HTTPSConnectionPool(host='api.openai.com', port=443): Read timed out
        number_of_picture = 2
        response = openai.Image.create({
            "prompt":prompt,
            "n":number_of_picture,
            "size":"1024*1024"
        }
        )
        url = response['data'][0]["url"]
        if response is not None and len(url) > 0:
            message_response = url
        else:
            message_response = "Sorry, no response could be generated."
    except Exception as e:
        logging.error("error occurred while generating the response"+e)
        message_response = "Sorry, an error occurred while generating the response.\n"+ e
    finally:
        return message_response
    
    