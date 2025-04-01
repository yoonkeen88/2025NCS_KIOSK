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