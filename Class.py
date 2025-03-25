class Person:

    # 클레스 변수
    species = 'human'
    
    # # 생성 메서드
    # def __new__(cls):
    #     pass
    # 초기화 메서드
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    # 인스턴스 메서드
    def greeting(self):
        print(f"Hello, I'm {self.name}")
    
    # 클래스 메서드
    @classmethod
    def get_species(cls): # cls는 클래스 자체를 의미 클래스 메서드에 붙여야 함.
        return cls.species
    
    # 스태틱 메서드
    @staticmethod
    def is_adult(age): # self나 cls가 없다.
        return age>=19
    
person1 = Person("John", 36)
person2 = Person("Marry", 24)

print(person1.greeting())
print(person1.get_species())