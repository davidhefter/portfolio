### THIS CODE WAS ONLY USED FOR TESTING COORDINATE CONVERSIONS, THIS FILE ISN'T USED IN THE MAIN CODE ###

import math
def th1th2_to_xyz(th1, th2):
    th3 = (th1+th2)/2
    th4 = (th1-th2)/2
    x = -math.cos(th3)*math.sin(th4)
    y = math.sin(th3)
    z = -math.cos(th3)*math.cos(th4)
    return[x,y,z]

def xyz_to_th1th2(x, y, z):
    th3 = math.atan(-y/z)                                               # th3 in radians
    if x!=0:
        th4 = -(abs(x)/x)*math.atan( math.sqrt((x*x) / ((y*y)+(z*z))) ) # th4 in radians
    else:
        th4 = 0                                                         # th4 in radians when x=0 (to prevent 0/0 issues)
    th1 = th3+th4                                                       # find th1
    th2=th3-th4                                                         # find th2
    return [th1, th2]

if __name__ == "__main__":
    [th1, th2] = [0.1747132, -0.1747132]

    #th1 = 0.2
    #th2 = 0.15
    [x,y,z] = th1th2_to_xyz(th1, th2)
    n = (x*x)+(y*y)+(z*z)
    print(n)
    print([x,y,z])
    [th1n, th2n] = xyz_to_th1th2(x,y,z)
    print([th1n, th2n])