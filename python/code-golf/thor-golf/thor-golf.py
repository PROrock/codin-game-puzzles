g,h,x,y=map(int,input().split())
while 1:c,d=((0,1)[g>x],-1)[g<x],((0,1)[h>y],-1)[h<y];x+=c;y+=d;print((" SN"[d]+" EW"[c]).strip())
