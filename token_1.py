from enum import Enum

class Tk(Enum):
    (RESWD,NUMLIT,END)=range(3)

class Token:
    """トークン"""
    def __init__(self,type,image):
        self.type = type
        self.image = image

def make_token(st):
    tokens=[]

    st +="\n"
    pos=0

    ch=st[pos]

    while ch != "\n":
        if ch in "+-*/()":
            tokens.append(Token(Tk.RESWD,ch))
            pos+=1
            ch=st[pos]
            continue
        if ch == " ":
            pos+=1
            ch=st[pos]
            continue
        print("許されない文字がある"+"["+str(ch)+"]")
        return[Token(Tk.END,"")]

    tokens.append(Token(Tk.END,""))
    return tokens

if __name__ == "__main__":
    tokens= make_token("+ - * / ( ) ")
    for token in tokens:
        print(token.type,token.image)