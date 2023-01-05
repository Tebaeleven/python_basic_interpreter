def main():
    """
    整数1 {+|-|*|/} 整数2
    """

    while True:
        # 整数1の入力
        st=input(">")
        if st.upper() == "QUIT":
            break
        a=int(st)
        # 演算子の入力
        st=input(">")
        op=st
        # 整数2の入力
        st=input(">")
        b=int(st)
        # 計算して表示
        if op== "+":
            print (a+b)
        elif op =="-":
            print(a-b)
        elif op =="*":
            print(a*b)
        elif op =="/":
            print(a/b)

if __name__ == '__main__':
    main()