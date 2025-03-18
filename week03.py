# 1) Ice amricano 2600, Ice latte 3300, Ice choco 3600
# 2) 아메리카노, 라떼, 초코 중 하나를 입력받는다.
# 3) 주문한 음료의 가격을 출력한다.
price = [2600, 3300, 3600]
menu = ["Ice Americano", "Ice Latte", "Ice Choco"]   
amount = [0] * len(price)
total = 0

#  메뉴 처리 부분
menuLists = ""
for k in range(len(menu)):
    menuLists += f"{menu[k]} | {price[k]}won: {k+1}, "
menuLists += f" Exit: {len(price)+1} \nEnter the menu number: "

# 프로그램 실행 루프 부분
while True:
    order = int(input(menuLists))

    if order == 1:
        total += price[0]
        amount[0] +=1
        print(f"Selected menu {price[0]}won.\nCumulated price:{total}won.")

    elif order == 2:
        total += price[1]
        amount[1] +=1

        print(f"Selected menu {price[1]}won.\nCumulated price:{total}won.")
        
    elif order == 3:
        total += price[2]
        amount[2] +=1
        print(f"Selected menu {price[2]}won.\nCumulated price:{total}won.")
        
    elif order == 4:
        print(f"Exit.\nCumulated price: {total}won.")
        
        break
    else:
        print("There no exist. \nPlz choose again.")

print("Product name | Amount | Subtotal")
print("-------------------------------")
for i in range(len(price)):
    if amount[i] != 0:
        print(f"{menu[i]} | {amount[i]} | {amount[i] * price[i]}")
print(f"Total : {total}원")
    

    