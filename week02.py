# 1) Ice amricano 2600, Ice latte 3300, Ice choco 3600
# 2) 아메리카노, 라떼, 초코 중 하나를 입력받는다.
# 3) 주문한 음료의 가격을 출력한다.
price = [2600, 3300, 3600]
menu = ["Ice Americano", "Ice Latte", "Ice Choco"]   

while True:
    order = int(input(f"주문하세요({menu[0]} {price[0]}원: 1, {menu[1]} {price[1]}원: 2, {menu[2]} {price[2]}원: 3, Exit: 4): "))

    if order == 1:
        print(f"{price[0]}원 입니다.")
    elif order == 2:
        print(f"{price[1]}원 입니다.")
    elif order == 3:
        print(f"{price[2]}원 입니다.")
    elif order == 4:
        print(f"서비스를 종료합니다.")
        break
    else:
        print("메뉴에 없습니다.")
    