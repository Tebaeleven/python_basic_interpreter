from enum import Enum

class Tk(Enum):
	(RESWD,NUMLIT,VAR,END)=range(4)

restbl=[
	"print",
]
class Token:
	"""トークン"""
	def __init__(self,type,image,pos):
		self.type = type
		self.image = image
		self.pos=pos
	def isRes(self,st):
		return self.type == Tk.RESWD and self.image == st

class Que:
	def __init__(self,st):
		self.buff=st+"\n"
		self.pos=-1

	def pop(self):
		self.pos+=1
		return self.buff[self.pos]
	def currPos(self):
		return self.pos
def make_token(st):
	global inp,ch
	
	tokens=[]

	inp=Que(st) 

	ch=inp.pop()

	while ch != "\n":
		if ch in "*/()":
			tokens.append(Token(Tk.RESWD,ch,inp.currPos()))
			ch=inp.pop()
			continue
		if ch in "+-":
			if len(tokens)>0:
				tkn=tokens[-1]
				if tkn.type == Tk.NUMLIT or tkn.type==Tk.RESWD and tkn.image==")":
					tokens.append(Token(Tk.RESWD,ch,inp.currPos()))
					ch=inp.pop()
					continue
			tkn=tkn_numlit()
			if tkn != None:
				tokens.append(tkn)
			else:
				return None
			continue
		# 数字トークン
		if "0"<=ch <="9" or ch == ".":
			tkn=tkn_numlit()
			if tkn != None:
				tokens.append(tkn)
			else:
				return None
			continue
		if "a" <= ch <= "z" or "A" <= ch <= "Z" or ch == "_":
			tkn=tkn_variable()
			if tkn != None:
				# 予約語だった場合、タイプを予約語にして追加
				if tkn.image in restbl:
					tkn.type = Tk.RESWD
				tokens.append(tkn)
			else:
				return None
			continue
		if ch == " ":
			ch=inp.pop()
			continue
		print_msg("L003:許されない文字がある"+"["+str(ch)+"]",inp.currPos())
		return None

	tokens.append(Token(Tk.END,"",-1))
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
	
	startPos=inp.currPos()
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
		print_msg("L001:数字として正しくない",inp.currPos())
		return None
	if not decimal_point and integer == 0:
		print_msg("L002:数字として正しくない",inp.currPos())
		return None

	return Token(Tk.NUMLIT, image,startPos)

def print_msg(msg,pos):
	print("-"*(pos + 1)+"↑")
	print(msg)

def tkn_variable():
	"""
	変数トークンの作成
	{a-z|A-Z|_}[a-z|A-Z|_|0-9]・・・
	"""
	global inp,ch
	startPos=inp.currPos()
	img=""
	while "a" <= ch <= "z" or "A" <= ch <= "Z" or ch == "_" or "0" <= ch <="9":
		img+=ch
		ch=inp.pop()
	return Token(Tk.VAR,img,startPos)

if __name__ == "__main__":
	while True:
		st=input(">")
		if st.upper()=="QUIT":
			break
		# トークン列を作成する
		tokens=make_token(st)
		if tokens != None:
			for token in tokens:
				print(token.type,token.image)