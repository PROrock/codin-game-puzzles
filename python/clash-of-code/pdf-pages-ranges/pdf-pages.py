n = int(input())
s=""
b=[]
x=lambda:f",{b[0]}" if len(b)==1 else f",{b[0]}-{b[-1]}"
for i in input().split():
    p = int(i)
    if not b or b[-1]+1==p:
        pass
    else:
        s+=x()
        b=[]
    b.append(p)
s+=x()
print(s[1:])