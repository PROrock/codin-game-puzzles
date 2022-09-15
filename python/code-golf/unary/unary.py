r=b=''
for c in input():b+=format(ord(c),'07b')
z='0'
while b:
    c=b[0];r+=f' {z+z*(c==z)} '
    while b and b[0]==c:r+=z;_,*b=b
print(r[1:])
