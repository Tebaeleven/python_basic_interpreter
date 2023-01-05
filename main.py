def main():
    """
    数字1 {+|-|*|/} 数字2
    """
    state=0
    while True:
        st=input(">")
        if st.upper() == "QUIT":
            break
        if state == 0:
            # 数字1の入力
            if not isNumeric(st):
                print("数字ではありません")
                continue
            a=float(st)
            state=1
            continue
        if state == 1:
            # 演算子の入力
            if len(st)!=1 or st not in "+-*/":
                print("演算子(+,-,*,/)ではない")
                continue
            op=st
            state=2
            continue
        if state == 2:
            # 数字2の入力
            if not isNumeric(st):
                print("数字ではありません")
                continue
            b=float(st)
            state=0
            # 計算して表示
            if op== "+":
                print (a+b)
            elif op =="-":
                print(a-b)
            elif op =="*":
                print(a*b)
            elif op =="/":
                print(a/b)
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