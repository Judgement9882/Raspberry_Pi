import sys
import matplotlib.pyplot as plt
import numpy as np


def onestep(pos, i):
    while True:
        direction = np.random.randint(1, 5)
        if np.abs(direction - pos[2][i - 1]) != 2:
            break
        if direction == 1:  # 상
            pos[0][i] = pos[0][i - 1]
            pos[1][i] = pos[1][i - 1] + 1
            pos[2][i] = direction
        elif direction == 3:  # 하
            pos[0][i] = pos[0][i - 1]
            pos[1][i] = pos[1][i - 1] - 1
            pos[2][i] = direction
        elif direction == 2:  # 좌
            pos[0][i] = pos[0][i - 1] - 1
            pos[1][i] = pos[1][i - 1]
            pos[2][i] = direction
        elif direction == 4:  # 우
            pos[0][i] = pos[0][i - 1] + 1
            pos[1][i] = pos[1][i - 1]
            pos[2][i] = direction
        return pos


pos1 = np.zeros((3, 1000 + 1))
pos2 = np.zeros((3, 1000 + 1))

if len(sys.argv) == 1:
    pos2[1][0] = 4
else:
    pos2[1][0] = sys.argv[1]

match_index = 0

for i in range(1, 1000 + 1):
    pos1 = onestep(pos1, i)
    pos2 = onestep(pos2, i)

    if pos1[0][i] == pos2[0][i] and pos1[1][i] == pos2[1][i]:
        match_index = i
        break

if match_index == 0:
    plt.plot(pos1[0], pos1[1], pos2[0], pos2[1])
    print('No luck!')
else:
    plt.plot(pos1[0, 0:match_index+1], pos1[1, 0:match_index+1],
             pos2[0, 0:match_index+1], pos2[1, 0:match_index+1])

    plt.scatter(pos1[0][match_index], pos1[1][match_index], c='r')
    print('Match at %d step' % match_index)

plt.title("Random Walk")
plt.axis('equal')
plt.grid()
plt.show()
