I=input
if int(I())<1:I(0)
*l,=map(int,I().split())
m=min(map(abs,l))
I((-m,m)[m in l])
