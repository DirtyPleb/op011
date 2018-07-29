import fractions
import random

import Cache

def Analyze(cache_filepath):
    # Load the cache.
    data = Cache.Load(cache_filepath)
    
    # Choose two random indices.
    random.seed()
    i1 = random.randint(0, len(data))
    i2 = random.randint(0, len(data))
    
    # Get the random data points.
    d1 = data[i1]
    d2 = data[i2]
    
    # Get the list of prime fibonacci numbers.
    FIBS = [89, 233, 1597, 28657, 514229, 433494437L, 2971215073L, 99194853094755497L]
    
    # Try all combinations of fibonacci numbers.
    for fib1 in FIBS:
        for fib2 in FIBS:
            nmod1 = (d1['input'] * (fib1 + d1['name']) - d1['output'])
            nmod2 = (d2['input'] * (fib2 + d2['name']) - d2['output'])
            print(fractions.gcd(nmod1, nmod2))
            
            # Try all n
            #for n1 in range(1, 10000):
            #    for n2 in range(1, 10000):
            #        
            #        gcd = fractions.gcd(nmod1, nmod2)
            #        if gcd > 10000:
            #            print(gcd)