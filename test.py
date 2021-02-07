import math
if __name__ == "__main__":
    base = [-2,-3]
    a = [-2,4]
    b = [2,-1]
    c = [-1,-2]
    # the problem is to judge which vector is the closest to a in Clockwise direction
    # of course, answer should be (2,-1)
    # it may appear to our mind that what if base meets identical vector
    d = [-2,-3]
    list = [a,b,c,d]
    for vec in list:
        x1 = base[0]
        y1 = base[1]
        x2 = vec[0]
        y2 = vec[1]
        dot = x1 * y2 - x2 * y1
        modulus_1 = math.sqrt(x1 * x1 + y1 * y1)
        modulus_2 = math.sqrt(x2 * x2 + y2 * y2)
        inner = x1 * x2 + y1 * y2
        result = (modulus_1 * modulus_2)
        value = inner / result
        print(value)
        theta = math.acos(value)
        print(theta)
        print(math.degrees(theta))

        if(x1 == x2 and y1 ==y2):
            print("The same")
        else:
            dot = x1*y2 - x2*y1
            if dot > 0:
                print(x2,y2,"is beyond 180")
            else:
                print(x2, y2, "is within 180")


