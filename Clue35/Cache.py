import json
import string
import sys

from bs4 import BeautifulSoup as bs
import requests

CLUE_URL = 'http://op011.com/1cmjnckjhtwks0cs/'

## Encodes a non-negative number as base-36.
## \param[in] number - The base-10 number to encode.
## \returns The number enced as base-36.
## \throws A TypeError if an invalid type was provided.
## \throws A ValueError if the argument was negative.
def Encode(number):
    # Check if the correct type was given.
    if not isinstance(number, (int, long)):
        raise TypeError('Base 36 encode: Number must be an integer.')
    
    # Check if the argument is positive.
    if number < 0:
        raise ValueError('Base 36 encode: Number must be positive.')
    
    # Initialize the base-36 string.
    base36string = ''
    
    # Check if we can short-circuit because the number is small.
    ALPHABET = string.digits + string.lowercase
    if number < len(ALPHABET):
        return ALPHABET[number]
    
    # Add characters to the base-36 encoding.
    while number != 0:
        number, alphabet_index = divmod(number, len(ALPHABET))
        base36string = ALPHABET[alphabet_index] + base36string
    
    return base36string

## Saves the clue data to a JSON file.
## \param[in] request_count - The number of requests that should be successfully completed.
## \param[in] cache_filepath - The filepath to save the cache to.
## \returns True if the correct number of data points could be cached. False otherwise.
def Save(request_count, cache_filepath):
    # Track the current input.
    current_input = 1

    # Get the requested number of data points.
    data = list()
    successful_request_count = 0
    total_request_count = 0
    max_requests_before_failure = (2 * request_count)
    while successful_request_count < request_count:
        # Record the request attempt.
        total_request_count += 1
        if (total_request_count >= max_requests_before_failure):
            return False
            
        # Request the web page.
        request = requests.post(CLUE_URL, data = { 'a': Encode(current_input) })
        if request is None:
            continue
        
        # Parse the request text.
        try:
            soup = bs(request.text, 'html.parser')
        except:
            continue
        
        # Get the main element.
        main_element = soup.find(id = 'main')
        if main_element is None:
            continue
        
        # Get the output.
        output = (main_element.get_text().split(' ')[-1] == 'true')

        # Create the data point.
        data_point = {
            'input': Encode(current_input),
            'input_10': current_input,
            'output': output
        }
        
        # Store the data point.
        data.append(data_point)
        
        # Increase the input.
        current_input += 1
        
        # Log the successful request.
        successful_request_count += 1

    # Export the results as a JSON file.
    with open(cache_filepath, 'w') as cache_file:
        cache_file.write(json.dumps(data, indent = 2))
    
    # Indicate that the operation was successful.
    return True

## Loads cached clue data from a JSON file.
## \param[in] cache_filepath - The absolute or relative (to the execution directory) filepath to the cache.
## \returns A list of the cached data. None on error.
def Load(cache_filepath):
    try:
        # Open the file.
        with open(cache_filepath, 'r') as cache_file:
            # Try to load the file as JSON.
            cached_data = json.load(cache_file)
            
            # Return the loaded object.
            # Screw checking formatting.
            return cached_data
    except:
        # Indicate that an error occurred.
        return None
    
if __name__ == '__main__':
    # Verify that the correct number of arguments were provided.
    argument_count = len(sys.argv)
    EXPECTED_ARGUMENT_COUNT = 3
    if (argument_count < EXPECTED_ARGUMENT_COUNT):
        print('Usage: python Clue35/Cache.py <# Trials> <Filepath>')
        exit(1)

    # Get the number of trials to perform.
    try:
        request_count = int(sys.argv[1])
    except:
        print('Error: The first argument must be an integer. Got: {}'.format(sys.argv[1]))
        exit(1)

    # Get the filepath where the cache should be saved.
    cache_filepath = sys.argv[2]
    try:
        # Try to open the filepath.
        # This is done early on to prevent work being done that cannot be saved.
        with open(cache_filepath, 'w') as cache_file:
            pass
    except:
        print('Error: Failed to open {} for writing.'.format(cache_filepath))
        exit(1)

    # Cache the information.
    cache_created_successfully = Save(request_count, cache_filepath)
    
    # Check whether the operation succeeded.
    if cache_created_successfully:
        # Inform the user that the data has been cached.
        print('Success! {} requests for clue 34 cached at {}. Let the games begin.'.format(request_count, cache_filepath))
        exit(0)
    else:
        print('Failure! The cache could not be created.')
        exit(1)