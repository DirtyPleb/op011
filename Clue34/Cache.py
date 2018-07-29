import json
import sys

from bs4 import BeautifulSoup as bs
import requests

CLUE_URL = 'http://op011.com/s669bfwg8odtgxrz/'

## Saves the clue data to a JSON file.
## \param[in] request_count - The number of requests that should be successfully completed.
## \param[in] cache_filepath - The filepath to save the cache to.
## \returns True if the correct number of data points could be cached. False otherwise.
def Save(request_count, cache_filepath):
    # Track whether the request has been seeded with a GET request.
    seeded = False
    last_name = ''

    # Get the requested number of data points.
    data = list()
    successful_request_count = 0
    total_request_count = 0
    max_requests_before_failure = (3 * request_count)
    while successful_request_count < request_count:
        # Record the request attempt.
        total_request_count += 1
        if (total_request_count >= max_requests_before_failure):
            return False
            
        # Request the web page.
        request = None
        if not seeded:
            request = requests.get(CLUE_URL)
        else:
            ARBITRARY_LONG_ABOVE_MOD = 10000000000000L
            request = requests.post(CLUE_URL, data = { last_name: str(ARBITRARY_LONG_ABOVE_MOD) })
            if request is None:
                seeded = False
                continue
        
        # Parse the request text.
        try:
            soup = bs(request.text, 'html.parser')
        except:
            seeded = False
            continue
        
        # Get the main element.
        main_element = soup.find(id = 'main')
        if main_element is None:
            seeded = False
            continue
        
        # Get the output.
        output = main_element.get_text().split(' ')[-1]
        
        # Get the form.
        forms = main_element.find_all('form')
        if forms is None or len(forms) != 1:
            seeded = False
            continue
        form = forms[0]
        
        # Get the text box.
        inputs = form.find_all('input')
        if inputs is None or len(inputs) != 2:
            seeded = False
            continue
        text_box = inputs[0]
        name = text_box.attrs['name']
        
        # Cache the last name for use in further POST requests.
        last_name = name
        if not seeded:
            # Track that we have been seeded.
            seeded = True
            
            # Continue on to perform a POST.
            continue

        # Create the data point.
        data_point = {
            'name': int(name, 36),
            'output': int(output.strip(), 36),
            'input': int(str(ARBITRARY_LONG_ABOVE_MOD), 36)
        }
        
        # Store the data point.
        data.append(data_point)
        
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
        print('Usage: python Clue34/Cache.py <# Trials> <Filepath>')
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