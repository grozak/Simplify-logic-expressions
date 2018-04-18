# Grzegorz Różak
#
# Dostępne operatory: and - &,  or - |, not - ~, xor - ^, implikacja - >, równoważność - =
#Jako zmienne przyjmuje ciągi małych liter :/
#simplify(string) zwraca uproszczone wyrażenie

import string

def generateCharList():
    variables ="".join([chr(i) for i in range(97,123)])
    return variables

def validateAndGetVariables(expr):
    variables=[]
    VARS=generateCharList()
    OPS="&|^>="
    currentvar=""
    state = True  # True - oczekiwany nawias ( lub zmienna, False - oczekiwany nawias ) lub operator
    par_count = 0
    for char in expr:
        if currentvar!="" and char in VARS:
                currentvar+=char
        else:
            if currentvar!="":
                variables.append(currentvar)
                currentvar=""
            if char=="0" or char=="1":
                state=False
                continue
            if char == " ":
                continue
            if state:
                if char=="~":
                    continue
                if char in VARS:
                    state = False
                    currentvar+=char
                elif char == "(":
                    par_count += 1
                else:
                    return None
            else:
                if char in OPS: state = True
                elif char == ")":
                    par_count -= 1
                else:
                    return None
        if par_count < 0:
            return
    if currentvar!="":
        variables.append(currentvar)
        state=False
    variables=list(set(variables))
    if par_count == 0 and not state:
        return variables
    else:
        return False

def genValues(N):
    values=[]
    for i in range (2**N):
        b=bin(i)[2:]
        l=len(b)
        b=str(0)*(N-l)+b
        values.append(b)
    return values

def exprToOnp(str):
    precendence={'&': 4, '|': 2,'~': 5, '^': 2, '>': 2, '=': 2, '(': 1, ')':1};
    ops=[]
    out=[]
    while str!="":
        token=str[:1]
        str=str[1:]
        if(token==" "):
            continue;
        if(token=="0" or token=="1"):
            out.append(token)
        elif(token=="~"):
            ops.append(token)
        elif(token=="("):
            ops.append(token)
        elif(token==")"):
            op=""
            while(op!="("):
                op=ops.pop()
                if(op!="("):
                    out.append(op)
        else:
            if(len(ops)>0):
                op=ops[len(ops)-1]
                while((op=="~" or precendence[op]>=precendence[token]) and op!="("):
                    op=ops.pop()
                    out.append(op)
                    if(len(ops)>0):
                        op=ops[len(ops)-1]
                    else:
                        break
            ops.append(token)
    while(ops!=[]):
        op=ops.pop()
        out.append(op)
    return ''.join(out)

def evalOnp(expr):
    stack=[]
    for char in expr:
        if(char=="0"):
            stack.append(False)
        elif(char=="1"):
            stack.append(True)
        elif(char=="~"):
            p=stack.pop()
            stack.append(not p)
        elif(char=="&"):
            p=stack.pop()
            q=stack.pop()
            stack.append(p and q)
        elif(char=="|"):
            p=stack.pop()
            q=stack.pop()
            stack.append(p or q)
        elif(char=="^"):
            p=stack.pop()
            q=stack.pop()
            stack.append((p or q) and not(p and q))
        elif(char==">"):
            p=stack.pop()
            q=stack.pop()
            stack.append(p or not q)
        elif(char=="="):
            p=stack.pop()
            q=stack.pop()
            stack.append(p==q)
    return stack.pop()

def replaceInExpr(expr, vamount):
    list=[]
    var=""
    for char in expr:
        continue

def areSimilar(str1, str2):
    found_diff=False
    r=""
    for i in range (len(str1)):
        if(str1[i]==str2[i]):
            r+=str1[i]
        elif(found_diff==True):
            return None
        else:
            r+="x"
            found_diff=True
    if(found_diff==False):
        return None
    return r

def findSimpliestValues(dict):
    dictA=dict
    dictB={}
    state=True
    while(state):
        indexlist=[]
        state=False
        for key1 in dictA:
            for key2 in dictA:
                if(key1==key2):
                    continue
                x=areSimilar(key1, key2)
                if(x!=None):
                    state=True
                    dictB[x]=dictA[key1]+dictA[key2]
                    indexlist.append(key1)
                    indexlist.append(key2)
        for key in dictA:
            if(key not in indexlist):
                dictB[key]=dictA[key]
        dictA=dictB
        dictB={}
    return dictA


def makeExpresion(variables, values):
    vamount=len(variables)
    expr=""
    state=False
    for value in values:
        state=False
        for i in range (vamount):
            if(value[i]!="x"):
                expr+=" "
            if(value[i]=="0"):
                if(state):
                    expr+="& "
                expr+="~"+variables[i]
                state=True
            elif(value[i]=="1"):
                if(state):
                    expr+="& "
                expr+=variables[i]
                state=True
            elif(value[i]=="x"):
                continue
            else:
                return
        if(value!=values[len(values)-1]):
            expr+=" |"
    return expr

def getDict(str):
    variables=sorted(validateAndGetVariables(str), key=len)[::-1]
    vamount=len(variables)
    values=genValues(vamount)

    print(variables)
    print(values)

    dictA={}
    for value in values:
        strcopy=str
        for i in range (vamount):
            strcopy=strcopy.replace(variables[i], value[i])
        if(evalOnp(exprToOnp(strcopy))==True):
            dictA[value]=[value]
        exp=exprToOnp(strcopy)
        print(exp+" == %s" % evalOnp(exp))
    print("\n")
    dictB=findSimpliestValues(dictA)
    print("DictFinal: ")
    print(dictB)
    print("\n")
    return dictB


def simplify(str):
    variables=validateAndGetVariables(str);
    if(variables==None):
        print("Wrong expression")
        return
    variables=sorted(variables, key=len)[::-1]
    vamount=len(variables)
    values=genValues(vamount)

    dictA={}
    truecounter=0
    for value in values:
        strcopy=str
        for i in range (vamount):
            strcopy=strcopy.replace(variables[i], value[i])
        if(evalOnp(exprToOnp(strcopy))==True):
            dictA[value]=[value]
            truecounter+=1
        exp=exprToOnp(strcopy)


    dictB=findSimpliestValues(dictA)
    keys=list(dictB.keys())
    mask=genValues(len(keys))

    possible=[]
    found=False
    for m in mask:
        tmplist=[]
        for i in range (len(keys)):
            if(m[i]=="1"):
                tmplist.append(keys[i])
        tmpexpr=makeExpresion(variables, tmplist)

        counter=0
        for value in values:
            strcopy=tmpexpr
            for i in range (vamount):
                strcopy=strcopy.replace(variables[i], value[i])
            if(strcopy!="" and evalOnp(exprToOnp(strcopy))==True):
                counter+=1
        if(counter==truecounter):
            possible.append(tmpexpr)
    final=sorted(possible, key=lambda x: x.count("|"))[0]
    return final



def main():
    examples=[]
    examples.append("(aaa | bb) > (dd & ~dd) | c ^ f^ bb")
    examples.append("a | 0 | (1 & ~bum)")

    for ex in examples:
        print("Original: "+ex)
        sim=simplify(ex)
        if(sim):
            print("Simplified: "+sim+"\n")






if __name__ == "__main__":
    main()
