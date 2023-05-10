from saybot import openai,os,logging

async def generate_image(prompt):
    logging.info("Using DALL.E 2")
    openai.api_key = os.getenv("API_OPENAI")
    try:
        message_response="Server Error or Usage Limit" # To avoid HTTPSConnectionPool(host='api.openai.com', port=443): Read timed out        
        response = openai.Image.create(
            prompt=prompt,
            n=1, # number of pics
            size="1024x1024",
            response_format="url",
        )
        url = response['data'][0]["url"]
        # logging.info(str(url))
        if response is not None and len(url) > 0:
            message_response = url
        else:
            message_response = "Sorry, no response could be generated."
    except Exception as e:
        logging.error("error occurred while generating the response"+e)
        message_response = "Sorry, an error occurred while generating the response.\n"+ e
    except TimeoutError:
        logging.error("DALL.E Timeout")
    finally:
        return message_response
    
    
