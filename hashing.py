def linear_probing(m, keys):
    table = [-1] * m # -1 for empty slots [cite: 83]
    for k in keys:
        for i in range(m):
            idx = (k + i) % m
            if table[idx] == -1:
                table[idx] = k
                break
    return table

def double_hashing(m, keys):
    table = [-1] * m
    for k in keys:
        h1 = k % m
        h2 = 1 + (k % (m - 1)) # [cite: 75]
        for i in range(m):
            idx = (h1 + i * h2) % m
            if table[idx] == -1:
                table[idx] = k
                break
    return table

if __name__ == "__main__":
    m, n = map(int, input().split()) # [cite: 77]
    keys = list(map(int, input().split())) # [cite: 78]
    
    lp = linear_probing(m, keys)
    dh = double_hashing(m, keys)
    
    print("LinearProbing:", *lp) # [cite: 81]
    print("DoubleHashing:", *dh) # [cite: 82]