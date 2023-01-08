from token import *

class Program:
	'''
	プログラムを保存するクラス

		lines  : 行番号を管理するリスト  [行番号…]
		program: プログラムを管理する辞書
			key = 行番号, value = [トークン列…]
		counter: 実行するプログラム行番号(lines上のインデックス値)
		
		例）
		10 a = 1
		20 b = 1
		30 print a + b
		の場合は、
		program = { 10: [a=1のトークン列],
					20: [b=1のトークン列],
					30: [print a+bのトークン列] }
		lines = [ 10, 20, 30 ]
	'''

	def __init__(self):
		self.clear()
		return

	def clear(self):
		self.program = {}
		self.lines = []
		self.counter = 0
		return

	def put(self, line, tkns):
		# 行にトークン追加
		self.program[line] = tkns
		# すでに行番号がある場合return
		if line in self.lines:
			return
		# 行番号を追加
		self.lines.append(line)
		self.lines.sort()
		return
	# 最初の行に設定
	def set_first(self):
		# もし行データがなければエラー
		if len(self.lines) == 0:
			return -1
		self.counter = 0
		return 0

	# 次の行に進める
	def set_next(self):
		self.counter += 1
		# もしカウンタが長さ以上なら最終行なのでエラーを返す
		if self.counter >= len(self.lines):
			return -1
		return 0
		
	# 実行する行を設定
	def set_line(self, line):
		# もしself.linesに引数のline番号があるならば、その番号をindexに設定
		if line in self.lines:
			ind = self.lines.index(line)
			self.counter = ind
			return 0
		return -1
	
	# 行を取得
	def get_line(self):
		# 実行カウンタ(index値)から行番号を取得
		return (self.lines[self.counter], 
		# 行番号からプログラムを取得（コピー）
		self.program[self.lines[self.counter]][:])

	# 行をimageとして一文で返す
	def line_image(self):
		st = ""
		num, tkns = self.get_line()
		for tkn in tkns:
			st += tkn.image + " "
		# 数値を5桁で返す
		return "{0:5d} ".format(num) + st
		
	# 行削除
	def del_line(self, line):
		# もし存在しない行なら中断
		if self.set_line(line) == -1:
			return
		del self.program[self.lines[self.counter]]
		del self.lines[self.counter]
		return