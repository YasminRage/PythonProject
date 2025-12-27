# class declaration
class Dog:
    """A simple dog model"""

    def __init__(self, name, age):
        """Initialize name and age attributes"""
        self.name = name
        self.age = age

    def sit(self):
        """Simulate a dog sitting in response to a command"""
        print(f"{self.name} is now sitting.")

    def roll_over(self):
        """Simulate rolling over in response to a command."""
        print(f"{self.name} rolled over!")


# Creating a Dog object
my_dog = Dog('Willie', 6)
print(my_dog.name)
my_dog.sit()
my_dog.roll_over()   

