import random
import time

# 🟢 포켓몬 기본 클래스
class Pokemon:
    def __init__(self, name, level, hp, attack_power, special_attack_power):
        self.name = name
        self.level = level
        self.hp = hp
        self.attack_power = attack_power
        self.special_attack_power = special_attack_power

    def attack(self, opponent):
        damage = random.randint(self.attack_power - 2, self.attack_power + 2)
        opponent.hp -= damage
        print(f"⚔️ {self.name}이(가) {opponent.name}을(를) 공격! {damage}의 피해!")

    def special_attack(self, opponent):
        damage = random.randint(self.special_attack_power - 5, self.special_attack_power + 5)
        opponent.hp -= damage
        print(f"💥 {self.name}이(가) 강력한 기술을 사용! {opponent.name}에게 {damage}의 피해!")

    def heal(self):
        heal_amount = random.randint(10, 20)
        self.hp += heal_amount
        print(f"✨ {self.name}이(가) 회복했다! +{heal_amount} HP")

    def is_defeated(self):
        return self.hp <= 0


# 🟠 피카츄 (전기 속성)
class Pikachu(Pokemon):
    def __init__(self):
        super().__init__(name="피카츄", level=10, hp=100, attack_power=15, special_attack_power=25)

    def special_attack(self, opponent):
        damage = random.randint(self.special_attack_power - 3, self.special_attack_power + 3)
        opponent.hp -= damage
        print(f"⚡ {self.name}이(가) 백만 볼트 사용! {opponent.name}에게 {damage}의 피해!")


# 🔥 리자몽 (불 속성)
class Charizard(Pokemon):
    def __init__(self):
        super().__init__(name="리자몽", level=12, hp=120, attack_power=18, special_attack_power=30)

    def special_attack(self, opponent):
        damage = random.randint(self.special_attack_power - 5, self.special_attack_power + 5)
        opponent.hp -= damage
        print(f"🔥 {self.name}이(가) 화염 방사를 사용! {opponent.name}에게 {damage}의 피해!")


# 🎮 배틀 시스템
def battle(player_pokemon, ai_pokemon):
    print(f"\n⚔️ 배틀 시작! {player_pokemon.name} vs {ai_pokemon.name}\n")

    while True:
        print(f"\n🔹 {player_pokemon.name} (HP: {player_pokemon.hp})")
        print(f"🔸 {ai_pokemon.name} (HP: {ai_pokemon.hp})\n")

        # 플레이어 턴
        print("📜 선택:")
        print("1. 기본 공격")
        print("2. 특수 공격")
        print("3. 회복")

        choice = input("👉 선택하세요 (1/2/3): ")

        if choice == "1":
            player_pokemon.attack(ai_pokemon)
        elif choice == "2":
            player_pokemon.special_attack(ai_pokemon)
        elif choice == "3":
            player_pokemon.heal()
        else:
            print("⚠️ 잘못된 입력입니다. 다시 선택하세요!")
            continue

        if ai_pokemon.is_defeated():
            print(f"\n🎉 {player_pokemon.name} 승리!")
            break

        time.sleep(1)

        # AI 턴
        ai_choice = random.choice(["1", "2", "3"])
        if ai_choice == "1":
            ai_pokemon.attack(player_pokemon)
        elif ai_choice == "2":
            ai_pokemon.special_attack(player_pokemon)
        elif ai_choice == "3":
            ai_pokemon.heal()

        if player_pokemon.is_defeated():
            print(f"\n💀 {ai_pokemon.name} 승리!")
            break

        time.sleep(1)


# 🏆 게임 시작
def main():
    print("\n🎮 포켓몬 배틀 게임!")
    print("1. 피카츄 ⚡")
    print("2. 리자몽 🔥")

    choice = input("👉 포켓몬을 선택하세요 (1/2): ")
    if choice == "1":
        player_pokemon = Pikachu()
        ai_pokemon = Charizard()
    elif choice == "2":
        player_pokemon = Charizard()
        ai_pokemon = Pikachu()
    else:
        print("⚠️ 잘못된 입력입니다. 게임을 종료합니다.")
        return

    battle(player_pokemon, ai_pokemon)


# 게임 실행
if __name__ == "__main__":
    main()
