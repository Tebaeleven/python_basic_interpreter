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

def main():
    """
    数字1 {{+|-|*|/} 数字2 | = }・・・
    0     1        2     1   1
    """
    stk=Stack()
    state=0
    while True:
        stk.print()
        #print("stateの数"+str(state))
        st=input(">")
        if st.upper() == "QUIT":
            break
        if state == 0:
            # 数字1の入力
            if not isNumeric(st):
                print("数字ではありません")
                continue
            stk.push(float(st))
            state=1
            continue
        if state == 1:
            # 演算子の入力
            if st=="=":
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
                print(a)
                stk.push(a)
                state=1
                continue
            if len(st)!=1 or st not in "+-*/":
                print("演算子(+,-,*,/)ではない")
                continue
            op=st
            if op in "*/":
                stk.push(st)
            else: # +,-
                if stk.size()==3:
                    b=stk.pop()
                    op1=stk.pop()
                    a=stk.pop()
                    if op1=="+":
                        a+=b
                    else:
                        a-=b
                    stk.push(a)
                    stk.push(op)
                else:
                    stk.push(op)
            state=2
            continue
        if state == 2:
            # 数字2の入力
            if not isNumeric(st):
                print("数字ではありません")
                continue
            b=float(st)
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
            continue


def isNumeric(st):
    """
    数字（少数含む）かどうかのチェックルーチン
        [+|-]{{0-9}・・・|[0-9]・・・ .[0-9]・・・}
    """
    st +="\n"
    pos=0
    # 小数点があるか
    decimal_point=False
    # 数字
    integer=0
    # 小数
    decimal=0
    state=0
    while True:
        # +,-判定
        ch = st[pos]
        if state==0:
            if ch in "+-":
                state=1
                pos=pos+1
                continue
            state=1
            continue
        # 整数、小数判定
        if state ==1:
            if "0" <= ch <= "9":
                integer+=1
                state=1
                pos+=1
                continue
            if ch == ".":
                decimal_point=True
                state=2
                pos+=1
                continue
            state=100
            continue
        # 小数の後の整数判定
        if state==2:
            if "0" <= ch <= "9":
                decimal+=1
                state=2
                pos+=1
                continue
            state=100
            continue
        if state==100:
            # 小数点があるのに小数がない場合
            if decimal_point and decimal==0:
                return False
            # 小数点がないのに数字が0個の場合
            if not decimal_point and integer==0:
                return False
            if ch=="\n":
                return True
            return False


if __name__ == '__main__':
    main()