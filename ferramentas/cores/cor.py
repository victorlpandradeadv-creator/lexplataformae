import math
def oklch_to_oklab(L,C,h):
    return L, C*math.cos(math.radians(h)), C*math.sin(math.radians(h))
def oklab_to_lin(L,a,b):
    l_=L+0.3963377774*a+0.2158037573*b; m_=L-0.1055613458*a-0.0638541728*b; s_=L-0.0894841775*a-1.2914855480*b
    l,m,s=l_**3,m_**3,s_**3
    return (4.0767416621*l-3.3077115913*m+0.2309699292*s, -1.2684380046*l+2.6097574011*m-0.3413193965*s, -0.0041960863*l-0.7034186147*m+1.7076147010*s)
def lin_to_oklab(r,g,b):
    l=0.4122214708*r+0.5363325363*g+0.0514459929*b; m=0.2119034982*r+0.6806995451*g+0.1073969566*b; s=0.0883024619*r+0.2817188376*g+0.6299787005*b
    l_,m_,s_=[math.copysign(abs(x)**(1/3),x) for x in (l,m,s)]
    return (0.2104542553*l_+0.7936177850*m_-0.0040720468*s_, 1.9779984951*l_-2.4285922050*m_+0.4505937099*s_, 0.0259040371*l_+0.7827717662*m_-0.8086757660*s_)
def ingamut(rgb): return all(-1e-4<=x<=1+1e-4 for x in rgb)
def oklch_lin(L,C,h):
    c=C
    while c>0 and not ingamut(oklab_to_lin(*oklch_to_oklab(L,c,h))): c-=0.002
    return tuple(min(1,max(0,x)) for x in oklab_to_lin(*oklch_to_oklab(L,max(c,0),h))), max(c,0)
def enc(x): return 12.92*x if x<=0.0031308 else 1.055*x**(1/2.4)-0.055
def dec(x): return x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4
def hexa(lin): return '#'+''.join(f"{round(enc(x)*255):02x}" for x in lin)
def lin_hex(h): h=h.lstrip('#'); return tuple(dec(int(h[i:i+2],16)/255) for i in (0,2,4))
def lum(lin): return 0.2126*lin[0]+0.7152*lin[1]+0.0722*lin[2]
def contraste(a,b):
    la,lb=lum(lin_hex(a)),lum(lin_hex(b)); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
M={'protan':[[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]],
   'deutan':[[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]],
   'tritan':[[1.255528,-0.076749,-0.178779],[-0.078411,0.930809,0.147602],[0.004733,0.691367,0.303900]]}
def simular(hx,tipo):
    if tipo=='normal': return hx
    v=lin_hex(hx); m=M[tipo]
    return hexa(tuple(min(1,max(0,sum(m[i][j]*v[j] for j in range(3)))) for i in range(3)))
def dist(a,b):
    A=lin_to_oklab(*lin_hex(a)); B=lin_to_oklab(*lin_hex(b)); return 100*math.dist(A,B)
def cor(L,C,h):
    lin,c=oklch_lin(L,C,h); return hexa(lin)
