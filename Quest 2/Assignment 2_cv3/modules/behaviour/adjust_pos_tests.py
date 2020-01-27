import math
import numpy as np

def adjust_position(blueBlob):
    '''
    Input: xy-coordinates of blue blob
    Function: adjusts position according to sonar and blue blob
    '''
    # Calculations on triangle with points A, B, C for robot, Left, Right respectively
    # Sides a, b, c are opposite to A, B, C respectively

    # Sonar meting
    # c, b = self.avg_sonar()
    c, b = [1.2, 1]

    # a = sqrt(b^2 + c^2 - 2bc cos(A))
    a = math.sqrt(b**2 + c**2 - 2 * b * c * math.cos(np.pi/3))

    C_angle = math.acos((a**2 + b**2 - c**2) / (2*a*b))

    h_a = b * math.sin(C_angle)

    B = np.asarray([-0.5 * a, .55])
    C = np.asarray([0.5 * a, .55])

    print(B)
    print(C)

    CD = (b**2 - c**2 + a**2) / (2*a)

    A = C - np.asarray([CD, h_a])

    correction_angle = math.acos(h_a / b)
    print(A, correction_angle)

adjust_position([40, 30])