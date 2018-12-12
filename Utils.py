
# Import useful helper files
import random
import io

# Returns True when random number falls in chance percent
def TryChance(probability):

    # Test int between 0 and 100
    test = random.randint(0, 100)
    # Create split to see if Test is within that range
    split = probability * 100
    # If test lower than split, it's a hit
    if test <= split:
        return True
    else:
        return False

def RandBetween(x, y):
    return random.randint(x, y)
