import sys
import numpy as np

if __name__ == "__main__":
    size = int(sys.argv[1])
    a = np.zeros((size, size))
    b = np.zeros((size, size))
    c = a @ b

    print(c[0, 0])
