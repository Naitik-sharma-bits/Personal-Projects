import sys

def get_hashes(word, b):
    h1 = sum(ord(c) for c in word) % b
    h2 = sum((i + 1) * ord(c) for i, c in enumerate(word)) % b
    return h1, h2

def solve():
    line1 = sys.stdin.readline().split()
    if not line1: return
    b, q = int(line1[0]), int(line1[1])
    bits = [0] * b
    
    for _ in range(q):
        line = sys.stdin.readline().split()
        if not line: break
        op, word = line[0].upper(), line[1]
        h1, h2 = get_hashes(word, b)
        
        if op == "ADD":
            bits[h1] = bits[h2] = 1
        else:
            print("POSSIBLY" if bits[h1] and bits[h2] else "NO")

if __name__ == "__main__":
    solve() 