from enum import Enum

class Tk(Enum):
    (RESWD,NUMLIT,END)=range(3)

class Token:
    """トークン"""
    def __init__(self,type,image):
        self.type = type
        self.image = image

class Que:
    def __init__(self,st):
        self.buff=st+"\n"
        self.pos=-1

    def pop(self):
        self.pos+=1
        return self.buff[self.pos]

def make_token(st):
    global inp,ch
    
    tokens=[]

    inp=Que(st) 

    ch=inp.pop()

    while ch != "\n":
        if ch in "*/()":
            tokens.append(Token(Tk.RESWD,ch))
            ch=inp.pop()
            continue
        if ch in "+-":
            if len(tokens)>0:
                tkn=tokens[-1]
                if tkn.type == Tk.NUMLIT or tkn.type==Tk.RESWD and tkn.image==")":
                    tokens.append(Token(Tk.RESWD,ch))
                    ch=inp.pop()
                    continue
            tokens.append(tkn_numlit())
            continue
        # 数字トークン
        if "0"<=ch <="9" or ch == ".":
            tokens.append(tkn_numlit())
            continue
        if ch == " ":
            ch=inp.pop()
            continue
        print("許されない文字がある"+"["+str(ch)+"]")
        return[Token(Tk.END,"")]

    tokens.append(Token(Tk.END,""))
    return tokens

def tkn_numlit():

	'''
	数字定数トークンの作成
		[+|-] { {0-9}… | [0-9]… .{0-9}… }
	'''
	global inp, ch
	
	decimal_point = False
	integer = 0
	decimal = 0
	image = ""
	state = 0
	
	while "0" <= ch <= "9" or ch in ".+-":
		if state == 0:
			if ch in "+-":
				state = 1
				image += ch
				ch = inp.pop()
				continue
			state = 1
			continue
		if state == 1:
			if "0" <= ch <= "9":
				integer += 1
				image += ch
				state = 1
				ch = inp.pop()
				continue
			if ch == ".":
				decimal_point = True
				image += ch
				state = 2
				ch = inp.pop()
				continue
			break
		if state == 2:
			if "0" <= ch <= "9":
				decimal += 1
				image += ch
				state = 2
				ch = inp.pop()
				continue
			break

	if decimal_point and decimal == 0:
		print("数字として正しくない")
		return Token(Tk.END, "")
	if not decimal_point and integer == 0:
		print("数字として正しくない")
		return Token(Tk.END, "")

	return Token(Tk.NUMLIT, image)


if __name__ == "__main__":
    tokens= make_token("+12-+56*(3-5*-4)-2")
    for token in tokens:
        print(token.type,token.image)