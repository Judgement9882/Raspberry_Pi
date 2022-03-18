import matplotlib.pyplot as plt
import numpy as np
import sys

def print_randomwalk(num):
    if (num == 0):
        print("No Luck!")
    else:
        print(f"Match at {num} step")
        
    x = np.real(p)
    y = np.imag(p)
    plt.plot(x,y)
    plt.grid(True)
    plt.axis('equal')
    plt.title('Random Walk')
    plt.show()


N = 1000
if len(sys.argv) > 1:
    D = int(sys.argv[1]) # 입력받은 인자를 (D,0) 으로 등록

M = 2
k = np.random.randint(-1,2, [N,M]) # -1~1 범위에서 N x M array 생성 (-1,0,1)
r = (1j)**k # (-j, 1, j) ==> -1이 안나옴
p = np.zeros([N,M],dtype=complex) # 복소수 타입 영행렬 생성 N x M
p[0][1] = (1j)*D # (0,D) 추가
d = (1j)**np.random.randint(0,4,M) # 0~3 범위에서 크기가 M인 array 생성 

can_meet = 0

for i in range(1,N):
    p[i,:] = p[i-1,:] + d*r[i,:]
    d   *= r[i,:]

    if (p[i][0] == p[i][1]):
        p = p[:i]
        can_meet = i
        break

print_randomwalk(can_meet)



