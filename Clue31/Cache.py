import json
import re
import sys

from bs4 import BeautifulSoup as bs
import requests

def Save(request_count, cache_filepath):
    # Store the URL to request.
    CLUE_31_URL = 'http://op011.com/j8p58jxcx5phhxr0/'

    # Create a regular expression to match each line.
    # I'm lazy about the correctness, sue me.
    EQUATION_PATTERN = r'x\s+(?P<operator>[<>=!]{1,2})\s+(?P<number>\d+)'
    equation_regex = re.compile(EQUATION_PATTERN)

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
        request = requests.get(CLUE_31_URL)
        if request is None:
            continue
        
        # Parse the request text.
        try:
            soup = bs(request.text, 'html.parser')
        except:
            continue
        
        # Get the source text.
        equations_element = soup.find(id = 'source')
        if equations_element is None:
            continue
        equations_text = equations_element.get_text()
        
        # Split the equations text into each individual equation.
        equations = equations_text.splitlines()
        
        # Match the regular expression against each equation.
        # Blank lines will not match properly. I'm lazy, so the failed matches are removed.
        equation_regex_matches = filter(lambda match: match is not None, [equation_regex.search(equation) for equation in equations])
        
        # Get the data point from the regex matches.
        data_point = {
            'number': int(equation_regex_matches[0].group('number')),
            'operators': [match.group('operator') for match in equation_regex_matches]
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
        print('Usage: python CacheClue31.py <# Trials> <Filepath>')
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
        print('Success! {} requests for clue 31 cached at {}. Let the games begin.'.format(request_count, cache_filepath))
        exit(0)
    else:
        print('Failure! The cache could not be created.')
        exit(1)