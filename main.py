def main():
    """
    整数1 {+|-|*|/} 整数2
    """
    state=0
    while True:
        st=input(">")
        if st.upper() == "QUIT":
            break

        if state == 0:
            # 整数1の入力
            a=int(st)
            state=1
            continue
        if state == 1:
            op=st
            state=2
            continue
        if state == 2:
            # 整数2の入力
            b=int(st)
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



if __name__ == '__main__':
    main()