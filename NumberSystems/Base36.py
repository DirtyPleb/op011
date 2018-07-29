import string

## The alphabet used for encoding/decoding.
ALPHABET = (string.digits + string.lowercase)

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
    if number < len(ALPHABET):
        return ALPHABET[number]
    
    # Add characters to the base-36 encoding.
    while number != 0:
        number, alphabet_index = divmod(number, len(ALPHABET))
        base36string = ALPHABET[alphabet_index] + base36string
    
    return base36string
    
## Decodes a non-negative base-36 string into an integer.
## \param[in] number_as_string - The base-36 number as a string.
## \returns The number decoded as a string.
## \throws An exception if the alphabet is exceeded.
def Decode(number_as_string):
    return int(number_as_string, 36)