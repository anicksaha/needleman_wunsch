def compute(a,b):
    n = len(a)
    score = 0
    gap = -2
    mismatch = -3
    match = 1
    for i in range(n):
        if a[i] == '_' or b[i] == '_':
            score += gap
        else:
            if a[i] == b[i]:
                score += match
            else:
                score += mismatch
    
    return score