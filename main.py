from token_1 import *
class Stack:
    """スタック"""
    def __init__(self):
        self.buff=[]

    def push(self,st):
        self.buff.insert(0,st)
    
    def pop(self):
        if len(self.buff)==0:
            print("stack is empty")
            return None
        return self.buff.pop(0)

    def size(self):
            return len(self.buff)

    def print(self):
            print(self.buff)

def expression(tokens):
    """
    数字1または変数1 {{+|-|*|/} 数字2または変数2 | = }・・・
    0               1        2              1   1
    """
    global print_stk
    stk=Stack()
    state=0
    # 括弧
    paren=0

    tkn=tokens.pop(0)
    while tkn.type != Tk.END:
        if print_stk:
            stk.print()
        if state == 0:
            # 「(」の入力
            if tkn.isRes("("):
                paren+=1
                stk.push("(")
                state=0
                tkn=tokens.pop(0)
                continue
            # 数字1または変数1の入力
            if tkn.isRes("+"):
                #特に何もしない
                state=0
                tkn=tokens.pop(0)
                continue
            if tkn.isRes("-"):
                #a = - aを a=-1 * aに変換
                tokens.insert(0,Token(Tk.RESWD,"*",-1))
                tokens.insert(0,Token(Tk.NUMLIT,"-1",-1))
                state=0
                tkn=tokens.pop(0)
                continue 
            # 変数だった場合
            if tkn.type==Tk.VAR:
                # 今までに定義されている変数か判定
                if tkn.image in assign.keys():
                    stk.push(float(assign[tkn.image]))
                    state=1
                    tkn=tokens.pop(0)
                    continue
                else:
                    print_msg("E005:未定義の変数",tkn.pos)
                    return None
            # 
            if tkn.type!=Tk.NUMLIT:
                print_msg("E001:数字ではありません",tkn.pos)
                return None

            stk.push(float(tkn.image))
            state=1
            tkn=tokens.pop(0)
            continue
        if state == 1:
            # 「)」の入力
            if tkn.isRes(")"):

                if paren == 0:
                    print_msg("E002:括弧の数がおかしいです",tkn.pos)
                    return None
                paren-=1
                b=stk.pop()
                op=stk.pop()
                if op in "+-":
                    a=stk.pop()
                    if op =="+":
                        a+=b
                    else:
                        a-=b
                    b=a
                    stk.pop() # 「(」の読み飛ばし
                else: # 「(」のはず
                    pass
                if stk.size()==0:
                    stk.push(b)
                    state=1
                    tkn=tokens.pop(0)
                    continue
                op=stk.pop()
                if op in "+-*/":
                    a=stk.pop()
                    if op=="+":
                        a+=b
                    if op=="-":
                        a-=b
                    if op=="*":
                        a*=b
                    if op=="/":
                        a/=b
                    stk.push(a)
                    state=1
                    tkn=tokens.pop(0)
                    continue
                # opが「(」場合
                stk.push(op)
                stk.push(b)
                state=1
                tkn=tokens.pop(0)
                continue

            if tkn.type !=Tk.RESWD or tkn.image not in "+-*/":
                print_msg("E003:演算子(+,-,*,/)ではない",tkn.pos)
                return None
            op=tkn.image
            if op in "*/":
                stk.push(op)
            else: # +,-
                if stk.size()>=3: 
                    b=stk.pop()
                    op1=stk.pop()
                    if op1 in "+-":
                        a=stk.pop()
                        if op1=="+":
                            a+=b
                        else:
                            a-=b
                        stk.push(a)
                        stk.push(op)
                    else: # 「(」のはず
                        stk.push(op1)
                        stk.push(b)
                        stk.push(op)
                else:
                    stk.push(op)
            state=2
            tkn=tokens.pop(0)
            continue
        if state == 2:
            # 「(」の入力
            if tkn.isRes("("):
                paren+=1
                stk.push("(")
                state=0
                tkn=tokens.pop(0)
                continue
            # 数字2、変数2の入力
            # 単項演算子の入力
            if tkn.isRes("+"):
                #特に何もしない
                tkn=tokens.pop(0)
                continue
            if tkn.isRes("-"):
                #a = - aを a=-1 * aに変換
                tokens.insert(0,Token(Tk.RESWD,"*",-1))
                tokens.insert(0,Token(Tk.NUMLIT,"-1",-1))
                state=2
                tkn=tokens.pop(0)
                continue 
            # 変数だった場合
            if tkn.type==Tk.VAR:
                # 今までに定義されている変数か判定
                if tkn.image in assign.keys():
                    b=float(assign[tkn.image])
                else:
                    print_msg("E005:未定義の変数",tkn.pos)
                    return None
            elif tkn.type == Tk.NUMLIT: 
                b=float(tkn.image)
            else:
                print_msg("E004:数字ではありません",tkn.pos)
                return None
            op=stk.pop()
            a=stk.pop()
            if op in "*/":
                if op=="*":
                    a*=b
                else:
                    a/=b
                stk.push(a)
            else:
                stk.push(a)
                stk.push(op)
                stk.push(b)
            state=1
            tkn=tokens.pop(0)
            continue
    if state !=1:
        print_msg("計算式誤り",0)
        return None

    if paren>0:
        print_msg("E006:括弧の対応が取れていない",0)
        return None

    # 演算子の入力
    if stk.size()==1:
        a=stk.pop()
    else:
        b=stk.pop()
        op=stk.pop()
        a=stk.pop()
        if op=="+":
            a+=b
        else:
            a-=b
    return a

def main():
    global print_stk,assign
    print_tkn=False
    print_stk=False
    assign={}
    while True:
        st=input(">")
        if st.upper()=="QUIT":
            break
        if st.upper()=="TOKEN ON":
            print_tkn=True
            continue
        if st.upper()=="TOKEN OFF":
            print_tkn=False
            continue
        if st.upper()=="STACK ON":
            print_stk=True
            continue
        if st.upper()=="STACK OFF":
            print_stk=False
            continue
        if st.upper()=="PRINT_VAR":
            print(assign)
            continue
        # トークン列を作成する
        tokens=make_token(st)
        if tokens == None:
            continue
        if print_tkn:
            for token in tokens:
                print(token.type,token.image)
        # トークンを使って計算する
        tkn=tokens.pop(0)
        if tkn.isRes("print"):
            ans = expression(tokens) 
            if ans !=None:
                print(ans)
            continue
        if tkn.type==Tk.VAR: #代入文とみなす
            var =tkn 
            tkn=tokens.pop(0)
            if tkn.isRes("="):
                ans=expression(tokens) 
                if ans !=None:
                    assign[var.image] = ans
                else:
                    print_msg("A001:代入文の「＝」がない",tkn.pos)
            continue

if __name__ == '__main__':
    main()