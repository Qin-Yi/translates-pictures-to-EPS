from random import random
from random import randint
import sys
final1=''

def print(s,end='\n'):
    global final1
    final1+=str(s)+end

def getSpace():
    a=randint(0,3)
    w=(' ','\t','\r','\n')
    return w[a]

def output():
    s=final1
    ii=' '
    ss=''
    for i in range(len(s)):
        if s[i].isalpha() or s[i].isdigit() or s[i]=='_' or s[i] in (' ','\t','\r','\n'):
            ss+=s[i]
        elif s[i] =='.':
            if s[i+1]=='.':
                ss+=getSpace()+s[i]
            elif s[i-1]=='.':
                ss+=s[i]+getSpace()
            else:
                ss+=s[i]
        elif s[i]=='-' and (not s[i-1].isdigit()):
                ss+=getSpace()+s[i]
        elif not s[i] in (' ','\t','\r','\n'):
            ss+=getSpace()+s[i]+getSpace()
    temp.write(ss)

varname=('rect','square','sector','let','for','in','_in1','_1_in','_1in2','_1','po_1','l_let')
picturename={"line" :4 , "rect" :4 , "tri" :3, "square":3 , "penta":3 , "hexa":3 , "ngon":4 , "sector":5 ,
 "filledrect":4 , "filledtri":3 , "filledsquare":3 , "filledpenta":3 ,
  "filledhexa":3 , "filledngon":4 , "filledsector":5}
transformationname={"translate":2 , "rotate":1 , "scale":1}
drawname={"color":3,"linewidth":1}
bop=('+','-','*','/')
uop=('cos','sin')


def graph():
    times=randint(7,35)
    for i in varname:
        print('let '+i+' = '+str(random()*100))
    for i in range(times):
        command();

def command():
    cmdtype=randint(0,16)
    cmdname=(transformable,drawingparameter,assignment,forcmd)
    cmdname[cmdtype//5]()

def transformable():
    cmdtype=randint(0,11)
    if cmdtype<5:
        cmdtype=0
    elif cmdtype<9:
        cmdtype=1
    else:
        cmdtype=2
    cmdname=(picture,transformation,group)
    cmdname[cmdtype]()

def picture():
    pic=list(picturename.keys())[randint(0,len(picturename)-1)]
    print(pic+'(',end='')
    for i in range(picturename[pic]-1):
        expression();
        print(',',end='')
    expression();
    print(')',end='')

def transformation():
    pic=list(transformationname.keys())[randint(0,len(transformationname)-1)]
    print(pic+'(',end='')
    command()
    print(',',end='')
    for i in range(transformationname[pic]-1):
        expression();
        print(',',end='')
    expression();
    print(')',end='')

def group():
    print('{',end=' ')
    command()
    for i in range(randint(0,2)):
        print(';',end='')
        command()
    print('}',end=' ')

def drawingparameter():
    pic=list(drawname.keys())[randint(0,len(drawname)-1)]
    print(pic+'(',end='')
    for i in range(drawname[pic]-1):
        expression(1)
        print(',',end='')
    expression(1)
    print(')',end='')

def assignment():
    print('let '+varname[randint(0,len(varname)-1)]+'=')
    expression()

def forcmd():
    print('for '+varname[randint(0,len(varname)-1)]+' in ')
    expression()
    print('..',end='')
    expression()
    group()

def expression(n=10):
    chance=random()
    if chance<0.4:
        print(varname[randint(0,len(varname)-1)])
    elif chance<0.7:
        print(random()*9+0.01,end=' ')
    elif chance<0.85:
        print('(')
        expression()
        print(bop[randint(0,len(bop)-1)])
        expression()
        print(')')
    else:
        print('(')
        print(uop[randint(0,len(uop)-1)])
        expression()
        print(')')


if __name__=="__main__":
    temp=open("temp","w")
    graph()
    output()
    temp.close()
