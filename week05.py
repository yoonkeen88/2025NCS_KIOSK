import random
import time

# 🔊 볼륨 관리 클래스
class Volume:
    def __init__(self, level=5):  # 기본 볼륨 5 (최대 10)
        self.level = level

    def set_volume(self, level):
        if 0 <= level <= 10:
            self.level = level
            print(f"🔊 볼륨 설정: {self.level}")
        else:
            print("⚠️ 볼륨은 0~10 사이여야 합니다!")

    def increase_volume(self):
        if self.level < 10:
            self.level += 1
            print(f"🔊 볼륨 증가: {self.level}")
        else:
            print("⚠️ 최대 볼륨입니다!")

    def decrease_volume(self):
        if self.level > 0:
            self.level -= 1
            print(f"🔉 볼륨 감소: {self.level}")
        else:
            print("⚠️ 최소 볼륨입니다!")


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
        print(f"💥 {self.name}이(가) 특수 기술을 사용! {opponent.name}에게 {damage}의 피해!")

    def heal(self):
        heal_amount = random.randint(10, 20)
        self.hp += heal_amount
        print(f"✨ {self.name}이(가) 체력을 회복했다! +{heal_amount} HP")

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


# 🟦 꼬부기 (물 속성)
class Squirtle(Pokemon):
    def __init__(self):
        super().__init__(name="꼬부기", level=10, hp=110, attack_power=14, special_attack_power=22)

    def special_attack(self, opponent):
        damage = random.randint(self.special_attack_power - 4, self.special_attack_power + 4)
        opponent.hp -= damage
        print(f"💦 {self.name}이(가) 물대포 사용! {opponent.name}에게 {damage}의 피해!")


# 🌿 이상해씨 (풀 속성)
class Bulbasaur(Pokemon):
    def __init__(self):
        super().__init__(name="이상해씨", level=10, hp=105, attack_power=13, special_attack_power=24)

    def special_attack(self, opponent):
        damage = random.randint(self.special_attack_power - 3, self.special_attack_power + 3)
        opponent.hp -= damage
        print(f"🍃 {self.name}이(가) 잎날가르기 사용! {opponent.name}에게 {damage}의 피해!")


# 🎮 배틀 시스템
def battle(player_pokemon, ai_pokemon, volume):
    print(f"\n⚔️ 배틀 시작! {player_pokemon.name} vs {ai_pokemon.name}\n")

    while True:
        print(f"\n🔹 {player_pokemon.name} (HP: {player_pokemon.hp})")
        print(f"🔸 {ai_pokemon.name} (HP: {ai_pokemon.hp})\n")

        # 플레이어 턴
        print("📜 선택:")
        print("1. 기본 공격")
        print("2. 특수 공격")
        print("3. 회복")
        print("4. 볼륨 조절")
        print("5. 종료")

        choice = input("👉 선택하세요 (1/2/3/4/5): ")

        if choice == "1":
            player_pokemon.attack(ai_pokemon)
        elif choice == "2":
            player_pokemon.special_attack(ai_pokemon)
        elif choice == "3":
            player_pokemon.heal()
        elif choice == "4":
            vol_choice = input("볼륨 조절 (🔉: -, 🔊: +, 숫자 입력): ")
            if vol_choice == "+":
                volume.increase_volume()
            elif vol_choice == "-":
                volume.decrease_volume()
            elif vol_choice.isdigit():
                volume.set_volume(int(vol_choice))
            continue
        elif choice == "5":
            print("⚠️ 게임 종료!")
            break
        elif choice == "exit":
            print("⚠️ 게임 종료!")
            break
        elif choice == "q":
            print("⚠️ 게임 종료!")
            break
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
    volume = Volume()

    print("\n🎮 포켓몬 배틀 게임!")
    print("1. 피카츄 ⚡")
    print("2. 리자몽 🔥")
    print("3. 꼬부기 💦")
    print("4. 이상해씨 🍃")

    choice = input("👉 포켓몬을 선택하세요 (1/2/3/4): ")
    pokemon_dict = {"1": Pikachu, "2": Charizard, "3": Squirtle, "4": Bulbasaur}

    if choice in pokemon_dict:
        player_pokemon = pokemon_dict[choice]()
        ai_pokemon = random.choice(list(pokemon_dict.values()))()
    else:
        print("⚠️ 잘못된 입력입니다. 게임을 종료합니다.")
        return

    battle(player_pokemon, ai_pokemon, volume)


# 게임 실행
if __name__ == "__main__":
    main()
