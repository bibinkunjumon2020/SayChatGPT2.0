from saybot import openai,os,logging

async def generate_response(prompt):
    # Set up OpenAI API key
    logging.info("Using text-davinci-003")
    openai.api_key = os.getenv("API_OPENAI")
    prompt += "?"
    try:
        message_response="Server Error or Usage Limit" # To avoid HTTPSConnectionPool(host='api.openai.com', port=443): Read timed out
       
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=250,
            n=1,
            stop=None,
            temperature=0.2,
        )
        if response is not None and len(response.choices[0].text) > 0:
            message_response = response.choices[0].text
        else:
            message_response = "Sorry, no response could be generated."
    except Exception as e:
        logging.error(e)
        message_response = "Sorry, an error occurred while generating the response.\n"+ e
    finally:
        return message_response
    
    