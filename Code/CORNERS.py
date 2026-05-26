from imports import *
import random as rnd

def export_corners_from_random_rectangle():
            while True:
                # Generate bottom-left corner (bl)
                bl_x = rnd.uniform(0, 15)
                bl_y = rnd.uniform(0, 15)
                # Generate top-right corner (tr)
                tr_x = rnd.uniform(0, 15)
                tr_y = rnd.uniform(0, 15)
                # Ensure width and height are at least 1
                width = tr_x - bl_x
                height = tr_y - bl_y
                if width >= 1 and height >= 1:
                    return [(tr_x, tr_y), (bl_x, bl_y)]
                else:
                    while width < 1 or height < 1:
                        # Generate bottom-left corner (bl)
                        bl_x = rnd.uniform(0, 15)
                        bl_y = rnd.uniform(0, 15)
                        # Generate top-right corner (tr)
                        tr_x = rnd.uniform(0, 15)
                        tr_y = rnd.uniform(0, 15)
                        width = tr_x - bl_x
                        height = tr_y - bl_y
                    return [(tr_x, tr_y), (bl_x, bl_y)]
                
if __name__ == '__main__':

    print("beep")
    rects_in_M = int(sys.argv[1])
    rects_in_N = int(sys.argv[2])
    seed = int(sys.argv[3])

    rnd.seed(seed)

    M = [export_corners_from_random_rectangle() for _ in range(rects_in_M)]

    N = [export_corners_from_random_rectangle() for _ in range(rects_in_N)]

    print("M",M)
    print("N",N)

