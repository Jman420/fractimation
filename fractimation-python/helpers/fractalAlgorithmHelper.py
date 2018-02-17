PHI = (1 + 5**0.5) / 2.0
def getFibonocciNumber(index):
    if index < 2:
        return index
    return int(round((PHI**index - (1 - PHI)**index) / 5**0.5))