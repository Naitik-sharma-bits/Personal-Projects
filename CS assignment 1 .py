f1= open("INPUT.txt",'r')
f2= open("Ugly.txt",'w')
r=f1.readlines()
c = ["ID", "First Name", "Last Name", "Email"]
m=[]
n=0
columns = f"{c[0]}\t\t{c[1]}     {c[2]}\t  {c[3]}\n"
f2.write(columns)
def uglycheck(u):
    if u<=0:
        return False
    elif u==1:
        return True
    for f in [2,3,5]:
        while u % f == 0:
            u//= f
    if u==1 :
        return True
try:
    for i in r:
        for k in i.split():
            if k[0].isnumeric():
                l=int(k[9:13])
                if uglycheck(l)==True:
                    t=1
                else:
                    t=0
                    n=0
            if t==1:
                m.append(k)
                n+=1
                if n==3:
                    email=f'{m[0].lower()}@bitspilani-digital.edu.in'
                    data = f"{m[0]}\t\t{m[1]}     {m[2]}\t  {email}\n"
                    f2.write(data)
                    n=0
                    m=[]
except EOFError:
    pass
f1.close()
f2.close()