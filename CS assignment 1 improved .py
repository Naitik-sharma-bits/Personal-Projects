def uglycheck(u):
    if u <= 0:
        return False
    elif u == 1:
        return True
    for f in [2, 3, 5]:
        while u % f == 0:
            u //= f
    return u == 1
try:
    with open(r"C:\Users\naiti\OneDrive\Documents\INPUT.txt", 'r') as f1:
        with open(r"C:\Users\naiti\OneDrive\Documents\Ugly.txt", 'w') as f2:
            r = f1.readlines()
            c = ["ID", "First Name", "Last Name", "Email"]
            columns = f"{c[0]}\t\t{c[1]}     {c[2]}\t  {c[3]}\n"
            f2.write(columns)
            m = []
            collecting = False 
            for i in r:
                for k in i.split():
                    if k[0].isnumeric():
                        m = []
                        collecting = False
                        try:
                            l = int(k[9:13])
                            if uglycheck(l):
                                collecting = True
                                m.append(k)
                        except (ValueError, IndexError):
                            pass 
                            
                    elif collecting:
                        m.append(k)
                        if len(m) == 3:
                            email = f'{m[0].lower()}@bitspilani-digital.edu.in'
                            data = f"{m[0]}\t\t{m[1]}     {m[2]}\t  {email}\n"
                            f2.write(data)
                            collecting = False
                            m = []
except FileNotFoundError:
    print("Error: INPUT.txt not found.")
except Exception as e:
    print(f"An error occurred: {e}")
print("FILE CREATED")