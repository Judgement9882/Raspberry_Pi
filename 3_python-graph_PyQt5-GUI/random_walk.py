import matplotlib.pyplot as plt
import numpy as np
import sys

N = 500
if len(sys.argv) > 1:
    N = int(sys.argv[1])

M = 5
k = np.random.randint(-1,2, [N,M])
r = (1j)**k
p = np.zeros([N,M],dtype=complex)
d = (1j)**np.random.randint(0,4,M)

for i in range(1,N):
    p[i,:] = p[i-1,:] + d*r[i,:]
    d   *= r[i,:]

x = np.real(p)
y = np.imag(p)

plt.plot(x,y)
plt.grid(True)
plt.axis('equal')
plt.title('Random Walk')
plt.show()

