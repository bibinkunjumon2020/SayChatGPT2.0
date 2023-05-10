from saybot import logging
from functools import partial
import asyncio

#--- the following is used for timeoutcheck for async function

async def check_api_request(func_api_caller, prompt):
    # Set the timeout value (in seconds)
    logging.info("Inside Check API requests")
    timeout_seconds = 10

    # Create a partial function to wrap the async function call
    async_func = partial(func_api_caller, prompt)

    try:
        # Run the async function with a timeout
        response = await asyncio.wait_for(async_func(), timeout=timeout_seconds)
    except asyncio.TimeoutError:
        # Handle timeout
        logging.info("Request timed out!!")
        response = None

    return response


#--- the following is used for timeoutcheck for SYNC function

# import concurrent.futures
# # from saybot import generate_image
# from saybot import logging

# '''
# Here each api calls to open ai is checked in our code.and limited by 10 seconds.
# Many times DALL.E fails to respond.

# '''
# def check_api_request(func_api_caller,prompt):
#     # Set the timeout value (in seconds)
#     logging.info("Inside Check API requests")
#     timeout_seconds = 10
#     response = None
#     # Create an executor to run the function with a timeout
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future = executor.submit(func_api_caller, prompt)
#         try:
#             response = future.result(timeout=timeout_seconds)
#             # Process the response as needed
#         except concurrent.futures.TimeoutError:
#             # Handle timeout
#             logging.info("Request timed out!!")
#     return response