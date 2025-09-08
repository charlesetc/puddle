def cache(func):
    """Simple cache decorator that stores function results"""
    cache_dict = {}

    def wrapper(*args, **kwargs):
        # Create a key from arguments
        key = str(args) + str(kwargs)

        # Return cached result if available
        if key in cache_dict:
            return cache_dict[key]

        # Otherwise compute and cache the result
        result = func(*args, **kwargs)
        cache_dict[key] = result
        return result

    return wrapper
