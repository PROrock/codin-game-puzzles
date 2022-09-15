I=input
a=lambda:map(int,I().split())
_,_,_,g,q,*_,e=a()
m=dict(a() for _ in[1]*e)
m[g]=q
while 1:f,p,d=I().split();f=int(f);d=(d[0]>"L")*2-1;print(("BLOCK","WAIT")[f<0 or d*m[f]>=d*int(p)])
# more cryptic variant with the same chars
# while 1:f,p,d=I().split();f=int(f);d=(d[0]>"L")*2-1;print(("BWLAOICTK")[f<0 or d*m[f]>=d*int(p)::2])
# I'm at 190!
