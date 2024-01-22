import time
import logging

def retry_on_exception(exceptions, max_attempts):
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logging.exception(f"Exception {e} caught. Retrying in 1 second...")
                    attempts += 1
                    time.sleep(1)
            logging.error(f"Maximum number of attempts ({max_attempts}) reached. Reraising exception...")
            raise e
        return wrapper
    return decorator