import json,os,urllib.request as U
def J(p,b):return json.load(U.urlopen(U.Request(os.getenv("MAKEFUN_ENV_URL")+p,data=json.dumps(b).encode())))
V=(0,100,320,330,500,975,0)
KN=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2))
D8=((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1))
DR=[KN,D8[4:],D8[:4],D8,D8]
CM=[15-{0:2,7:1,4:3,56:8,63:4,60:12}.get(i,0)for i in range(64)]
B=[0]*64;KP=[0,0];TT={};UN=[]
def pf(f):
 global S,C,EP
 w=f.split();i=0;B[:]=[0]*64
 for ch in w[0]:
  if ch.isdigit():i+=int(ch)
  elif ch!="/":
   p="pnbrqk".index(ch.lower())+1
   if ch.islower():p=-p
   x=56-(i&56)+(i&7);B[x]=p
   if abs(p)==6:KP[p<0]=x
   i+=1
 S=1-2*(w[1]<"w");C=sum(1<<i for i,c in enumerate("KQkq")if c in w[2]);EP=0 if w[3]=="-"else ord(w[3][0])+8*int(w[3][1])-105
def att(x,by):
 f=x&7
 for dy in(7,9):
  y=x-dy*by
  if 0<=y<64 and B[y]==by and abs((y&7)-f)==1:return 1
 for df,dr in KN:
  y=x+df+8*dr
  if 0<=y<64 and abs((y&7)-f)==abs(df)and B[y]==2*by:return 1
 for df,dr in D8:
  nf,nr=f+df,x//8+dr;d=0
  while 0<=nf<8 and 0<=nr<8:
   p=B[nr*8+nf];d+=1
   if p:
    if p*by>0:
     t=abs(p)
     if t==5 or(t==6 and d==1)or(t==3 and df*dr)or(t==4 and not df*dr):return 1
    break
   nf+=df;nr+=dr
 return 0
def gen(cap):
 ms=[];ap=ms.append;w6=6-(S<0)*5
 for i,p in enumerate(B):
  if p*S<=0:continue
  t=abs(p);f=i&7;r=i>>3
  if t==1:
   d=8*S;o=i+d;pr=r==w6;pz=(5,4,3,2)if pr else(0,);tg=[]
   if B[o]==0 and(not cap or pr):tg.append(o)
   for df in(-1,1):
    j=o+df
    if 0<=f+df<8 and(B[j]*S<0 or(EP and j==EP)):tg.append(j)
   for to in tg:
    for z in pz:ap(i|to<<6|z<<12)
   if not cap and not pr and B[o]==0 and r==7-w6 and B[i+2*d]==0:ap(i|(i+2*d)<<6)
  else:
   for df,dr in DR[t-2]:
    nf,nr=f+df,r+dr
    while 0<=nf<8 and 0<=nr<8:
     j=nr*8+nf;q=B[j]
     if q*S<0 or not(q or cap):ap(i|j<<6)
     if q or t in(2,6):break
     nf+=df;nr+=dr
 if not cap:
  for bit,kf,kt in((1,4,6),(2,4,2),(4,60,62),(8,60,58)):
   md=(kf+kt)//2
   if C&bit and all(B[x]==0 for x in((md,kt)if kt>kf else(md,kt,kf-3)))and not(att(kf,-S)or att(md,-S)or att(kt,-S)):ap(kf|kt<<6)
 return ms
def mk(m):
 global S,C,EP
 fr=m&63;to=(m>>6)&63;p=B[fr];cs=-1
 if EP and p*p==1 and to==EP:cs=to-8*S
 UN.append((B[:],S,C,EP,KP[:]))
 if cs>=0:B[cs]=0
 B[to]=(m>>12)*S if m>>12 else p;B[fr]=0
 if abs(p)==6:
  KP[S<0]=to
  if abs(to-fr)==2:
   rf,rt=(to+1,to-1)if to in(6,62)else(to-2,to+1);B[rt]=B[rf];B[rf]=0
 C&=CM[fr]&CM[to];EP=(fr+to)//2 if p*p==1 and abs(to-fr)==16 else 0;S=-S
def un():
 global S,C,EP
 b,S,C,EP,k=UN.pop();B[:]=b;KP[:]=k
def ev():return sum((V[abs(p)]+(((i^(p<0)*56)>>3)*4-4 if p*p==1 else 0))*(p>0 or-1)for i,p in enumerate(B)if p)
def sc(m):
 v=B[(m>>6)&63]
 return(1<<24)+abs(v)*16 if v else 0
def sr(d,a,b):
 global ND;ND+=1
 if ND>LIM:1/0
 sd=S
 if d<=0:
  st=ev()*sd
  if st>=b:return st
  a=max(a,st);bt=st;ms=gen(1)
 else:
  a0=a;k=bytes(x+6 for x in B)+bytes((S<0,C,EP));e=TT.get(k)
  if e and e[0]>=d:
   v=e[1]
   if e[2]==0:return v
   if e[2]==1:a=max(a,v)
   else:b=min(b,v)
   if a>=b:return v
  bt=-10**7;ms=gen(0)
 bm=0
 ms.sort(key=sc,reverse=True)
 for m in ms:
  mk(m)
  if att(KP[S>0],S):un();continue
  v=-sr(d-1,-b,-a);un()
  if v>bt:bt=v;bm=m
  if v>a:a=v
  if a>=b:break
 if not bm:return-100000 if att(KP[S<0],-S)else(0 if d>0 else bt)
 if d>0:TT[k]=(d,bt,2 if bt<=a0 else 1 if bt>=b else 0)
 return bt
def uci(m):
 s=f"{chr(97+(m&7))}{(m>>3&7)+1}{chr(97+(m>>6&7))}{((m>>9)&7)+1}"
 if m>>12:s+="nbrq"[(m>>12)-2]
 return s
def root():
 global ND,LIM
 ms=[]
 for m in gen(0):
  mk(m)
  if not att(KP[S>0],S):ms.append(m)
  un()
 ND=0;LIM=3e4;best=ms[0]
 for d in range(70):
  try:
   a=-10**7;bm=0;ms.sort(key=lambda m:(m!=best,-sc(m)))
   for m in ms:
    mk(m);v=-sr(d-1,-10**7,-a);un()
    if v>a:a=v;bm=m
   best=bm
  except Exception:break
 return best
if __name__=="__main__":
 while 1:
  g=J("/game",{})
  if g["status"]=="done":break
  while g["status"]=="your_move":
   try:
    pf(g["fen"]);m=root();u=uci(m)if m is not None else g["legal_moves"][0]
    g=J("/move",{"game":g["game"],"move":u})
   except Exception:g=J("/game",{})
