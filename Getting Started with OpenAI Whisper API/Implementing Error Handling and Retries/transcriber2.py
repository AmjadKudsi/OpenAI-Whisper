# Implementing Error Handling and Retries with Python Decorators

from functools import wraps
import time
import random


def retry_on_exception(max_attempts, wait_time):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: implement the retry logic
            retries = 0
            while retries < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_attempts:
                        raise
                    print(f"Error: {e}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator


# Example function using the decorator for retry logic
@retry_on_exception(max_attempts=10, wait_time=1)
def check_random_number():
    num = random.randint(1, 10)
    if num <= 8:
        raise ValueError(f"Number {num} is not greater than 8.")
    return f"Number {num} is greater than 8."


# Execute the function once, it will retry automatically
response = check_random_number()
print(response)