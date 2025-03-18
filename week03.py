# 1) Ice amricano 2600, Ice latte 3300, Ice choco 3600
# 2) 아메리카노, 라떼, 초코 중 하나를 입력받는다.
# 3) 주문한 음료의 가격을 출력한다.
price = [2600, 3300, 3600]
menu = ["Ice Americano", "Ice Latte", "Ice Choco"]   
amount = [0] * len(price)
total = 0

# 주문 처리 함수
def orderProcess(idx:int):
    global amount
    amount[idx] += 1
    global total
    total += price[idx]
    print(f"{menu[idx]}: {price[idx]}won")
    print(f"Total: {total}won")
    print("-----------------------------------------------")

#  메뉴 처리 부분
menuLists = ""
for k in range(len(menu)):
    menuLists += f"{menu[k]} | {price[k]}won: {k+1}, "
menuLists += f" Exit: {len(price)+1} \nEnter the menu number: "

# 프로그램 실행 루프 부분
while True:
    order = int(input(menuLists))
    if order == len(price)+1:
        break
    elif order > len(menu):
        print("There no exist. \nPlz choose again.")
    else: 
       orderProcess(order-1)
    
# 주문 통계 출력
print("Product name\t|\tAmount\t|\tSubtotal")
print("-----------------------------------------------")
for i in range(len(price)):
    if amount[i] != 0:
        print(f"{menu[i]}\t|\t{amount[i]}\t|\t{amount[i] * price[i]}")
print(f"Total\t:\t{total}won")
    

    