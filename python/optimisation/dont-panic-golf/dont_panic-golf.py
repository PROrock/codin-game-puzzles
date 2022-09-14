I=input
a=lambda:[int(i)for i in I().split()]
s=lambda x:((0,-1)[x<0],1)[x>0]
w="WAIT"
_,_,_,f,p,_,_,e=a()
m=dict(a() for _ in range(e))
m[f]=p
while 1:
 z,g,d=I().split();z=int(z)
 if z<0:print(w);continue
 t=m[z]-int(g);print(("BLOCK",w)[s(t)==s((1,-1)[d=="LEFT"]) or t==0])
