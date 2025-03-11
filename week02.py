# 1) Ice amricano 2600, Ice latte 3300, Ice choco 3600
# 2) 아메리카노, 라떼, 초코 중 하나를 입력받는다.
# 3) 주문한 음료의 가격을 출력한다.
ame = 2600
latte = 3300
choco = 3600
while True:
    order = int(input("주문하세요(Ice americano: 1, Ice Latte: 2, Ice choco: 3600, Exit: 4): "))

    if order == 1:
        print(f"{ame}원 입니다.")
    elif order == 2:
        print(f"{latte}원 입니다.")
    elif order == 3:
        print(f"{choco}원 입니다.")
    elif order == 4:
        print(f"서비스를 종료합니다.")
        break
    else:
        print("메뉴에 없습니다.")
    