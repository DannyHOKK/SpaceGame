class person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def printname(self):
        print(self.name)

class student(person):
    def __init__(self, name, age, year):
        super().__init__(name,age)
        self.graduation = year
    def printgraduation(self):
        print (self.name)

def printage():
    return print("name")