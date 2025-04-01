# class inheritance
# user - teacher - student
class User:
    def __init__(self, name, age, identity, todo = []):
        self.name = name
        self.age = age
        self.id = identity    
        self.todo = []

    def getTodo(self, todo):
        """
        Returns a todo list for the user.
        """
        self.todo.append(todo)
        return self.todo
            
    def getIdentity(self):
        return self.id
    
    def __str__(self):
        return f"User: {self.name}, Age: {self.age}"
    
class Teacher(User):
    def __init__(self, name, age, identity, subject):
        super().__init__(name, age, identity)
        self.subject = subject
        self.todo = []
        self.student = []
        self.grade = []

    def getTodo(self, todo):
        """
        Returns a todo list for the teacher.
        """
        self.todo.append(todo)
        return self.todo

class Student(User):
    def __init__(self, name, age, identity, grade):
        super().__init__(name, age, identity)
        self.grade = grade
        self.todo = []
        self.teacher = []
        self.subject = []
        self.grade = []


# Association
# has a
# Aggregation
# part of
# Composition
