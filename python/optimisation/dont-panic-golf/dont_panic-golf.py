I=input
a=lambda:[int(i)for i in I().split()]
s=lambda x:(x<0,-1)[x<0]
w="WAIT"
_,_,_,f,p,_,_,e=a()
m=dict(a() for _ in[1]*e)
m[f]=p
while 1:
 z,g,d=I().split();z=int(z)
 if z<0:print(w);continue
 t=m[z]-int(g);print(("BLOCK",w)[s(t)==s((1,-1)[d[0]<"R"]) or t==0])

# TODO PROBABLY DIFFERENT/SHORTER ALGO is a way to go!
