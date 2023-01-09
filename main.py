from token_1 import *
from program import *

class Stack:
	'''スタック'''
	
	def __init__(self):
		self.buff = []
		
	def push(self, st):
		self.buff.insert(0, st)
		
	def pop(self):
		if len(self.buff) == 0:
			print("Stack Error")
			return None
		return self.buff.pop(0)
	
	def size(self):
		return len(self.buff)
		
	def print(self):
		print(self.buff)

def expression(tokens):

	'''
	数字1または変数1 { {+|-|*|/} 数字2または変数2 | = }…
	0                  1         2               1  1
	'''
	global print_stk, assign
	
	stk = Stack()
	paren = 0
	state = 0
	
	tkn = tokens.pop(0)
	
	while tkn.type != Tk.END:
		if print_stk:
			stk.print()
		if state == 0:
			#「(」の入力
			if tkn.isRes("("):
				paren += 1
				stk.push("(")
				state = 0
				tkn = tokens.pop(0)
				continue
			# 単項演算子 +, - の場合
			if tkn.isRes("+"):
				state = 0
				tkn = tokens.pop(0)
				continue
			if tkn.isRes("-"):
				tokens.insert(0, Token(Tk.RESWD, "*", -1))
				tokens.insert(0, Token(Tk.NUMLIT, "-1", -1))
				state = 0
				tkn = tokens.pop(0)
				continue
			# 数字1または変数1の入力
			if tkn.type == Tk.VAR:
				if tkn.image in assign.keys():
					stk.push(float(assign[tkn.image]))
					state = 1
					tkn = tokens.pop(0)
					continue
				else:
					print_msg("E005: 未定義の変数である", tkn.pos)
					return None
			if tkn.type != Tk.NUMLIT:
				print_msg("E001: 数字ではない", tkn.pos) #L002のエラー
				return None
			stk.push(float(tkn.image))
			state = 1
			tkn = tokens.pop(0)
			continue
		if state == 1:
			#「)」の入力
			if tkn.isRes(")"):
				if paren == 0:
					print_msg("E002: 括弧の対応がとれていない", tkn.pos)
					return None
				paren -= 1
				b = stk.pop()
				op = stk.pop()
				if op in "+-":
					a = stk.pop()
					if op == "+":
						a += b
					else:
						a -= b
					b = a
					stk.pop() #「(」の読み飛ばし
				else: #「(」のはず
					pass
				if stk.size() == 0:
					stk.push(b)
					state = 1
					tkn = tokens.pop(0)
					continue
				op = stk.pop()
				if op in "+-*/":
					a = stk.pop()
					if op == "+":
						a += b
					if op == "-":
						a -= b
					if op == "*":
						a *= b
					if op == "/":
						a /= b
					stk.push(a)
					state = 1
					tkn = tokens.pop(0)
					continue
				#opが「(」の場合
				stk.push(op)
				stk.push(b)
				state = 1
				tkn = tokens.pop(0)
				continue
			if tkn.type != Tk.RESWD or tkn.image not in "+-*/":
				print_msg("E003: 演算子(+,-,*,/)ではない", tkn.pos)
				return None
			op = tkn.image
			if op in "*/":
				stk.push(op)
			else: #+, -
				if stk.size() >= 3:
					b = stk.pop()
					op1 = stk.pop()
					if op1 in "+-":
						a = stk.pop()
						if op1 == "+":
							a += b
						else:
							a -= b
						stk.push(a)
						stk.push(op)
					else: #「(」のはず
						stk.push(op1)
						stk.push(b)
						stk.push(op)
				else:
					stk.push(op)
			state = 2
			tkn = tokens.pop(0)
			continue
		if state == 2:
			#「(」の入力
			if tkn.isRes("("):
				paren += 1
				stk.push("(")
				state = 0
				tkn = tokens.pop(0)
				continue
			# 単項演算子 +, - の場合
			if tkn.isRes("+"):
				state = 2
				tkn = tokens.pop(0)
				continue
			if tkn.isRes("-"):
				tokens.insert(0, Token(Tk.RESWD, "*", -1))
				tokens.insert(0, Token(Tk.NUMLIT, "-1", -1))
				state = 2
				tkn = tokens.pop(0)
				continue
			#数字2/変数2の入力
			if tkn.type == Tk.VAR:
				if tkn.image in assign.keys():
					b = float(assign[tkn.image])
				else:
					print_msg("E006: 未定義の変数である", tkn.pos)
					return None
			elif tkn.type == Tk.NUMLIT:
				b = float(tkn.image)
			else:
				print_msg("E004: 数字ではない", tkn.pos) #L002のエラー
				return None
			op = stk.pop()
			a = stk.pop()
			if op in "*/":
				if op == "*":
					a *= b
				else:
					a /= b
				stk.push(a)
			else:
				stk.push(a)
				stk.push(op)
				stk.push(b)
			state = 1
			tkn = tokens.pop(0)
			continue

	if state != 1:
		print_msg("E005: 計算式誤り", 0)
		return None
		
	if paren > 0:
		print_msg("E006: 括弧の対応がとれていない", 0)
		return None
		
	if stk.size() == 1:
		a = stk.pop()
	else:
		b = stk.pop()
		op = stk.pop()
		a = stk.pop()
		if op == "+":
			a += b
		else:
			a -= b
	return a
	
def copy_until(tokens, imglist):

	ret = []
	
	tkn = tokens.pop(0)
	while tkn.type != Tk.END:
		if tkn.type == Tk.RESWD and tkn.image in imglist:
			tokens.insert(0, tkn)
			ret.append(Token(Tk.END, "", -1))
			return 0, ret
		ret.append(tkn)
		tkn = tokens.pop(0)
		
	ret.append(Token(Tk.END, "", -1))	
	return -1, ret
	
def search_next(currline):

	global prg
	
	nest = 0
	prg.set_line(currline)
	
	while True:
		if prg.set_next() == -1:
			return None
		line, tokens = prg.get_line()
		tkn = tokens.pop(0)
		if tkn.isRes("for"):
			nest += 1
			continue
		if tkn.isRes("next"):
			if nest == 0:
				return line
			nest -= 1
			continue
	
def print_err(msg):

	global prg, running_flg
	
	if running_flg:
		print(prg.line_image())
	print(msg)
	
def statement(tokens):

	global assign, prg, trace_flg, running_flg

	if trace_flg and running_flg:
		print("exec: "+prg.line_image())
	
	tkn = tokens.pop(0)
	
	if tkn.isRes("for"):
		tkn = tokens.pop(0)
		if tkn.type != Tk.VAR:
			print_err("for文の変数が指定されていない")
			return -1
		var = tkn.image
		tkn = tokens.pop(0)
		if not tkn.isRes("="):
			print_err("=がない")
			return -1
		ret, exps = copy_until(tokens,["to"])
		if ret == -1:
			print_err("toがない")
			return -1
		init_val = expression(exps)
		if init_val == None:
			print_err("初期値が正しくない")
			return -1
		tkn = tokens.pop(0) # toの読み飛ばし
		ret, exps = copy_until(tokens, ["step"])
		to_val = expression(exps)
		if to_val == None:
			print_err("終了値が正しくない")
			return -1
		if ret == 0: # step指定がある
			tkn = tokens.pop(0) #step文の読み飛ばし
			step_val = expression(tokens)
			if step_val == None:
				print_err("加算値が正しくない")
				return -1
		else:
			step_val = 1
		for_line , _ = prg.get_line()
		next_line = search_next(for_line)
		if next_line == None:
			print_err("next文がない")
			return -1
		prg.set_line(for_line)
		if prg.set_next() == -1:
			print_err("for文が正しく終わっていない")
			return -1
		assign[var] = init_val
		cont_line, tokens = prg.get_line()
		while True:
			tkn = tokens.pop(0)
			if tkn.isRes("next"):
				assign[var] += step_val
				if step_val > 0 and assign[var] > to_val:
					return 0
				if step_val < 0 and assign[var] < to_val:
					return 0
				if prg.set_line(cont_line) == -1:
					print_err("for文の後に位置づけることができない")
					return -1
				_, tokens = prg.get_line()
				continue
			tokens.insert(0, tkn)
			ret = statement(tokens)
			if ret == 0:
				if prg.set_next() == -1:
					print_err("for文が正しく終わっていない")
					return -1
				_, tokens = prg.get_line()
				continue
			if ret == -1: #終了
				return -1
			if for_line < ret <= next_line:
				if prg.set_line(ret) == -1:
					print_err("飛び先が見つからない")
					return -1
				_, tokens = prg.get_line()
				continue
			return ret
	
	if tkn.isRes("if"):
		ret, lside = copy_until(tokens,["=", "<>", ">", "<", ">=", "<="])
		if ret == -1:
			print_err("条件式が正しくない(左辺)")
			return -1
		lval = expression(lside)
		if lval == None:
			return -1
		tkn = tokens.pop(0)
		cmp = tkn.image
		ret, rside = copy_until(tokens,["goto"])
		if ret == -1:
			print_err("条件式が正しくない(右辺)")
			return -1
		rval = expression(rside)
		if rval == None:
			return -1
		val = lval - rval
		if not (cmp == "=" and val == 0 or \
		   cmp == "<>" and val != 0 or \
		   cmp == ">=" and val >= 0 or \
		   cmp == "<=" and val <= 0 or \
		   cmp == ">"  and val >  0 or \
		   cmp == "<"  and val <  0):
		   	return 0
		tkn = tokens.pop(0) # gotoトークンの読み飛ばし
		tkn = tokens.pop(0)
		if tkn.type != Tk.NUMLIT:
			print_err("行番号が正しくない")
			return -1
		return int(tkn.image)
	
	if tkn.isRes("goto"):
		tkn = tokens.pop(0)
		if tkn.type != Tk.NUMLIT:
			print_err("行番号が正しくない")
			return -1
		return int(tkn.image)
	
	if tkn.isRes("clear"):
		assign = {}
		return 0
	
	if tkn.isRes("print"):
		ans = expression(tokens)
		if ans != None:
			print(ans)
			return 0
		else:
			return -1
	
	if tkn.type == Tk.VAR: #代入文
		var = tkn
		tkn = tokens.pop(0)
		if tkn.isRes("="):
			ans =  expression(tokens)
			if ans != None:
				assign[var.image] = ans
				return 0
			else:
				return -1
		else:
			print_err("A001: 代入文の「=」がない")
			return -1

	print_err("未定義の命令")
	return -1
	
	
def main():

	global print_stk, assign, trace_flg, running_flg, prg
	
	print_tkn = False
	print_stk = False
	trace_flg = False
	running_flg = False
	assign = {}
	prg = Program()
	
	while True:
		st = input(">")
		if st.upper() == "QUIT":
			break
		if st.upper() == "TOKEN ON":
			print_tkn = True
			continue
		if st.upper() == "TOKEN OFF":
			print_tkn = False
			continue
		if st.upper() == "STACK ON":
			print_stk = True
			continue
		if st.upper() == "STACK OFF":
			print_stk = False
			continue
		if st.upper() == "PRINT_VAR":
			print(assign)
			continue
		if st.upper() == "TRACE ON":
			trace_flg = True
			continue
		if st.upper() == "TRACE OFF":
			trace_flg = False
			continue
		if st.upper() == "LIST":
			if prg.set_first() == -1:
				continue
			while True:
				print(prg.line_image())
				if prg.set_next() == -1:
					break
			continue
		if "LOAD" in st.upper():
			load_file = st.split(' ')
			if len(load_file) != 2:
				print("Usage: load file-name")
				continue
			infile = load_file[1]
			try:
				with open(infile, "r") as f:
					lines = f.readlines()
			except Exception as e:
				print("ロードできませんでした: ",e)
				continue
			prg.clear()
			for line in lines:
				if line == "":
					continue
				tokens = make_token(line)
				if tokens == None:
					continue
				tkn = tokens.pop(0)
				if tkn.type == Tk.NUMLIT:
					prg.put(int(tkn.image), tokens)
			continue	
		if "SAVE" in st.upper():
			save_file = st.split(' ')
			if len(save_file) != 2:
				print("Usage: save file-name")
				continue
			outfile = save_file[1]
			try:
				with open(outfile, "w") as f:
					if prg.set_first() == -1:
						print("プログラムがありません")
						continue
					while True:
						f.write(prg.line_image()+"\n")
						if prg.set_next() == -1:
							break
			except Exception as e:
				print("セーブできませんでした: ",e)
				continue
			continue
		if st.upper() == "RUN":
			if prg.set_first() == -1:
				print("実行するプログラムがありません")
				continue
			running_flg = True
			while True:
				_, tokens = prg.get_line()
				ret = statement(tokens)
				if ret == 0: #次の行の実行
					if prg.set_next() == -1:
						break
					continue
				if ret == -1: #終了（STOP文とか）
					break
				#retは次に実行する行番号の場合
				if prg.set_line(ret) == -1:
					print_err("そのような行番号はありません:")
					break
			running_flg = False
			continue
		#トークン列を作成する
		tokens = make_token(st)
		if tokens == None:
			continue
		if print_tkn:
			for token in tokens:
				print(token.type, token.image)
		#トークン列を使って計算する。
		tkn = tokens.pop(0)
		if tkn.type == Tk.NUMLIT: #行番号
			if len(tokens) == 1: # Tk.ENDのときのみ
				prg.del_line(int(tkn.image))
				continue
			prg.put(int(tkn.image), tokens)
			continue
		tokens.insert(0, tkn)
		statement(tokens)

if __name__ == "__main__":
	main()
