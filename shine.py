def analyse(token):
    if token[0]=='{':group(token)
    elif token[0]=='for':loop(token)
    elif token[0]=='let':value=token[3:];variable[token[1]]=convert(value)

    if token[0]=='color':
        t=paraments(token[1:],3)[1:]
        print('%g %g %g setrgbcolor'%(t[0],t[1],t[2]))
    elif token[0]=='linewidth':
        try:
            print('%g setlinewidth'%float(token[2]))
        except:
            print('%g setlinewidth'%convert(token[1:-1]))

    if token[0]=='translate':addstack(token,2)
    elif token[0]=='rotate':addstack(token,1)
    elif token[0]=='scale':addstack(token,1)

    if token[0]=='line':line(token)
    elif token[0]=='rect':rect(token);print('stroke')
    elif token[0]=='filledrect':rect(token);print('fill')
    elif token[0]=='ngon':ngon(token);print('stroke')
    elif token[0]=='filledngon':ngon(token);print('fill')
    elif token[0]=='sector':sector(token);print('stroke')
    elif token[0]=='filledsector':sector(token);print('fill')
    elif token[0]=='tri':token.insert(-1,',');token.insert(-1,3);ngon(token);print('stroke')
    elif token[0]=='filledtri':token.insert(-1,',');token.insert(-1,3);ngon(token);print('fill')
    elif token[0]=='square':token.insert(-1,',');token.insert(-1,4);ngon(token);print('stroke')
    elif token[0]=='filledsquare':token.insert(-1,',');token.insert(-1,4);ngon(token);print('fill')
    elif token[0]=='penta':token.insert(-1,',');token.insert(-1,5);ngon(token);print('stroke')
    elif token[0]=='filledpenta':token.insert(-1,',');token.insert(-1,5);ngon(token);print('fill')
    elif token[0]=='hexa':token.insert(-1,',');token.insert(-1,6);ngon(token);print('stroke')
    elif token[0]=='filledhexa':token.insert(-1,',');token.insert(-1,6);ngon(token);print('fill')

def group(arg):
    global transformations,datas
    pretrans=transformations.copy()
    predatas=datas.copy()
    n,t=[0],[]
    a=b=f=0
    try:
        for j in range(1,len(arg)-2):
            if arg[j]=='{':f=1;a+=1
            elif arg[j]=='}':b+=1;if a==b:a=b=f=0
            if arg[j]==';' and f==0:n.append(j)
        n.append(len(arg)-1)
        for j in range(len(n)-1):
            t.append(arg[n[j]+1:n[j+1]])
        for j in t:
            analyse(j)
            transformations=pretrans.copy()
            datas=predatas.copy()
    except:pass

def loop(arg):
    l,h,f,ff=[],[],0,0
    for i in arg:
        if i=='in' and ff==0:f=ff=1
        elif i=='..':f=2
        elif i=='{':f=arg.index(i);break
        if f==1:l.append(i)
        elif f==2:h.append(i)
    l,h=round(convert(l[1:])),round(convert(h[1:]))
    if arg[1] in variable:previous=variable[arg[1]]
    try:
        for i in range(l,h+1):
            variable[arg[1]]=i
            group(arg[f:])
    except:pass
    try:
        variable[arg[1]]=previous
    except:pass

def addstack(arg,x):
    transformations.append(arg[0])
    pa=paraments(arg[1:],x)
    datas.append(pa[1:])
    analyse(arg[2:pa[0]])

def transform(arg):
    points=[]
    if transformations==[]:return arg
    else:
        for p in arg:
            point,data=p.copy(),datas.copy()
            for s in transformations[::-1]:
                d=data.pop()
                if s=='translate':point[0]+=d[0];point[1]+=d[1]
                elif s=='rotate':
                    sin=math.sin(math.radians(d[0]))
                    cos=math.cos(math.radians(d[0]))
                    x,y=point[0],point[1]
                    point[0],point[1]=x*cos-y*sin,x*sin+y*cos
                elif s=='scale':point[0]*=d[0];point[1]*=d[0]
            points.append(point)
        return points

def tran_sector(r,b,e):
    data=datas.copy()
    if transformations==[]:pass
    else:
        for s in transformations[::-1]:
            d=data.pop()
            if s=='scale':r*=d[0]
            elif s=='rotate':b+=d[0];e+=d[0]
    return r,b,e

def rect(token):
    t=paraments(token[1:],4)[1:]
    x,y,w,h=t[0],t[1],t[2],t[3]
    points=[[x,y],[x+w,y],[x+w,y+h],[x,y+h]]
    p=transform(points)
    print('''%g %g moveto\n%g %g lineto\n%g %g lineto\n%g %g lineto\n%g %g lineto'''
        %(p[0][0],p[0][1],p[1][0],p[1][1],p[2][0],p[2][1],p[3][0],p[3][1],p[0][0],p[0][1]))

def ngon(token):
    t=paraments(token[1:],4)[1:]
    x,y,r,n=t[0],t[1],t[2],round(t[3])
    points=[[x+r,y]]
    for i in range(1,n):
        points.append([x+r*math.cos(2*i*math.pi/n),y+r*math.sin(2*i*math.pi/n)])
    p=transform(points)
    print('%g %g moveto'%(p[0][0],p[0][1]))
    for i in range(1,n):
        print('%g %g lineto'%(p[i][0],p[i][1]))
    print('%g %g lineto'%(p[0][0],p[0][1]))

def sector(token):
    t=paraments(token[1:],5)[1:]
    x,y,r,b,e=t[0],t[1],t[2],t[3],t[4]
    points=transform([[x,y]])
    x,y=points[0][0],points[0][1]
    r,b,e=tran_sector(r,b,e)
    xx=x+r*math.cos(math.radians(b))
    yy=y+r*math.sin(math.radians(b))
    print('''%g %g moveto\n%g %g lineto\n%g %g %g %g %g arc\n%g %g lineto'''%(x,y,xx,yy,x,y,r,b%360,e%360,x,y))

def line(token):
    t=paraments(token[1:],4)[1:]
    points=[[t[0],t[1]],[t[2],t[3]]]
    points=transform(points)
    x0,y0=points[0][0],points[0][1]
    x,y=points[1][0],points[1][1]
    print('%g %g moveto\n%g %g lineto\nstroke'%(x0,y0,x,y))

def paraments(arg,x):
    n,p,t=[0],[],[]
    for j in range(len(arg)-1):
        if arg[j]==',':
            n.append(j)
    n.append(len(arg)-1)
    t.append(n[-x-1]+1)
    for j in range(len(n)-1):
        p.append(arg[n[j]+1:n[j+1]])
    for j in p[-x:]:
        t.append(convert(j))
    return t

def convert(arg):
    try:
        return float(arg[0])
    except:
        try:
            return variable[arg[0]]
        except:
            new=[]
            for j in range(len(arg)):
                if arg[j] in variable:
                    new.append(variable[arg[j]])
                    if arg[j]=='sin' or arg[j]=='cos':
                        if arg[j+1] in ')+-*/' :pass
                        else:new[-1]=arg[j]
                else:new.append(arg[j])
            return calculate(new)

def calculate(arg):
    stack=[]
    for j in arg:
        if j=='(':pass
        elif j==')':
            v1=stack.pop()
            operator=stack.pop()
            stack.append(cclt(stack,operator,v1))
        else:stack.append(j)
    return stack.pop()

def cclt(a,b,c):
    if b=='sin':return math.sin(math.radians(float(c)))
    elif b=='cos':return math.cos(math.radians(float(c)))
    else:
        a=a.pop()
        a,c=float(a),float(c)
        if b=='+':return a+c
        elif b=='-':return a-c
        elif b=='*':return a*c
        elif b=='/':return a/c

import sys,math
print('%!PS-Adobe-3.0 EPSF-3.0\n%%BoundingBox: 0 0 1239 1752')
file=sys.stdin.read()
tokenlist=file.split()

a=b=c=d=0
flag,f1,f2=[-1],0,0
for i in range(len(tokenlist)-1):
    if tokenlist[i]=='(':a,f1=a+1,1
    elif tokenlist[i]==')':b+=1;if a==b:f1=0
    elif tokenlist[i]=='{':c,f2=c+1,1
    elif tokenlist[i]=='}':d+=1;if c==d:f2=0
    if f1==0 and f2==0:flag.append(i)
flag.append(len(tokenlist)-1)

commandlist,j,f=[[]],0,0
w=['line','rect','filledrect','tri','filledtri','square','filledsquare','penta','filledpenta','hexa','filledhexa','sector','filledsector','ngon','filledngon','color','linewidth','translate','scale','rotate']
for i in range(len(flag)-1):
    command=tokenlist[flag[i]+1:flag[i+1]+1]
    if command==['let'] and f==0:n,f=4,1
    elif command==['for'] and f==0:n,f=7,1
    elif command[0] in w and f==0:n,f=2,1
    elif command[0]=='{':n=1
    commandlist[j]+=command
    n-=1
    if n==0:j+=1;commandlist.append([]);f=0
commandlist.pop()

variable={}
for i in commandlist:
    transformations,datas=[],[]
    analyse(i)
