def merge_the_tools(string, k):
    string=list(string)
    n=len(string)
    l=[]
    g=[]
    m=0
    d=0
    for i in range(n):
        for j in range(m,n):
            l.append(string[j])
            d+=1
            if d==k:
                g.append(l)
                
            elif d>k:
                d=0
                m+=(k-1)
    print(l)
    
if __name__ == '__main__':
    string, k = input(), int(input())
    merge_the_tools(string, k)