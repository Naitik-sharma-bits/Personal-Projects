import sys

def is_balanced(expression):
    stack = []
    bracket_map = {')': '(', '}': '{', ']': '['}
    
    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in ")}]":
            if not stack or stack.pop() != bracket_map[char]:
                return "INVALID"
    
    return "VALID" if not stack else "INVALID"

if __name__ == "__main__":
    try:
        s = input("Enter expression: ").strip()
        print(is_balanced(s))
    except EOFError:
        pass