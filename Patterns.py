

## Finds all indices for the start of a pattern in an array.
## \param[in] pattern - The pattern to find.
## \param[in] array - The array to search.
## \returns The start indices of the patterns.
def FindAllPatternInArray(pattern, array):
    # Cache the lengths.
    pattern_length = len(pattern)
    array_length = len(array)
    
    # Iterate over starting positions.
    pattern_start_indices = list()
    for start_index in range(array_length - pattern_length + 1):
        if array[start_index:(start_index + pattern_length)] == pattern:
            pattern_start_indices.append(start_index)
    
    return pattern_start_indices

## Finds the longest repeated pattern in an array.
## \param[in] array - The array to search.
## \returns A tuple containing the longest pattern and the start index of the first occurrence in the given array.
def FindLongestRepeatedPattern(array):
    # Cache the array length.
    array_length = len(array)
    
    # Iterate over all pattern lengths, starting with the longest possible.
    for pattern_length in range(array_length, 0, -1):
        for start_index in range(array_length - pattern_length + 1):
            end_index = start_index + pattern_length
            pattern = array[start_index:end_index]
            if len(FindAllPatternInArray(pattern, array)) > 1:
                return (start_index, pattern)
    
    return []