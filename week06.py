# 이번에는 모듈화 해서 키오스크를 작동하는 프로그램을 작성해보자.

from kiosk import Menu, OrderSystem, DiscountPolicy

# 프로그램 실행
if __name__ == "__main__":
    menu = Menu()
    menu.add_item("Ice Americano", 2600)
    menu.add_item("Ice Latte", 3300)
    menu.add_item("Ice Choco", 3600)
    menu.add_item("Ice Tea", 3500)
    
    discount = DiscountPolicy()
    # 할인 정책을 설정합니다.
    
    order_system = OrderSystem(menu, discount)
    order_system.run()
    