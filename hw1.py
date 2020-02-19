from turtle import Turtle
from math import sin, radians


def otocenie1(degree, dir_right, arrow_turtle):
    if dir_right:
        arrow_turtle.right(degree)
    else:
        arrow_turtle.left(degree)


def otocenie2(degree, dir_right, arrow_turtle):
    if dir_right:
        arrow_turtle.left(degree)
    else:
        arrow_turtle.right(degree)


def arrow(length, width, point_length, dir_right):
    arrow_turtle = Turtle()
    if not dir_right:
        arrow_turtle.right(180)
    arrow_turtle.forward(length)
    otocenie1(90, dir_right, arrow_turtle)
    new_length = (point_length - width) / 2
    arrow_turtle.forward(new_length)
    for i in range(2):
        otocenie2(120, dir_right, arrow_turtle)
        arrow_turtle.forward(point_length)
    otocenie2(120, dir_right, arrow_turtle)
    arrow_turtle.forward(new_length)
    otocenie1(90, dir_right, arrow_turtle)
    arrow_turtle.forward(length)
    otocenie2(90, dir_right, arrow_turtle)
    arrow_turtle.forward(width)
arrow(20, 120, 200, True)

def piggy(width, height, head_angle):
    piggy_turtle = Turtle()

    def nohy(length):
        piggy_turtle.right(120)
        for i in range(2):
            piggy_turtle.forward(length)
            piggy_turtle.backward(length)
            piggy_turtle.left(60)

    nohy(height / 4)
    piggy_turtle.forward(width)
    nohy(height / 4)
    piggy_turtle.left(90)
    piggy_turtle.forward(height)
    piggy_turtle.left(90)
    piggy_turtle.forward(width)
    piggy_turtle.left(90)
    piggy_turtle.forward(height)
    piggy_turtle.right(180 - ((180 - head_angle) / 2))
    if head_angle == 0:
        sinv = 0
    else:
        sinv = (height / 2) // sin(radians(head_angle / 2))
    piggy_turtle.forward(sinv)
    piggy_turtle.right(180 - head_angle)
    piggy_turtle.forward(sinv)


def common_multiples(count, num_a, num_b):
    greater = max(num_b, num_a)
    while not ((greater % num_a == 0) and (greater % num_b == 0)):
        greater += 1
    for i in range(count):
        print(greater * (i+1), end=" ")


def print_e(size):
    print("E" * size)
    for i in range(size - 3):
        print("E", end="")
        print("." * (size - 1))
        if ((size - 3) // 2) == (i+1):
            print("E" * (size // 2 + 1), end="")
            print("." * (size // 2))
    print("E" * size)


def table_min(size):
    print("   |  ", end="")
    for i in range(size):
        if i < 8:
            print(i + 1, end="  ")
        else:
            print(i + 1, end=" ")
    print()
    print("---+", end="")
    for i in range(size):
        print("---", end="")
    print("-")
    for i in range(size):
        if i < 9:
            print("", i + 1, "|", end=" ")
        else:
            print(i + 1, "|", end=" ")
        for j in range(size):
            mini = min(i+1, j+1)
            if j < 9:
                print("", mini, end=" ")
            else:
                if mini < 10:
                    print("", mini, end=" ")
                else:
                    print(mini, end=" ")
        print()


def exact_multi_prime_divisor(num, power):
    i = 2
    count = 0
    while i <= num:
        while num % i == 0:
            num = num // i
            count += 1
        if count == power:
            print(i, end=" ")
        count = 0
        i += 1
