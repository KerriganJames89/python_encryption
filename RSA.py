#The program in this file is the individual work of JAMES KERRIGAN
import numpy
import time
from matplotlib import pyplot as plt



print ("Enter the tempature: ", end="")
num = int(input())

#Matrix creation based on temperature given by user
matrix = numpy.zeros([(num + 2), (num + 2)])
matrix[:, 0] = num
matrix[0, :] = 0
matrix[num + 1, :] = 0

start = time.time()

#Alg based on the temperature equation given for this assignment
for i in range(3000):
  stop_all = True
  for y in range(1, num + 1):
    stop_y = True
    for x in range(1, num + 1):

      new_val = float((1/4) * (matrix[y - 1, x] + matrix[y + 1, x] + matrix[y, x - 1] + matrix[y, x + 1]))
      if stop_y:
        if new_val - matrix[y, x] >= 0.0001:
            stop_y = False
      matrix[y, x] = new_val
    if stop_y:
        break
    stop_all = False

  if stop_all:
    print (i)
    break

end = time.time()
print("Time is: ", end - start)

#Removes halo rows then assigns the matrix to a grid to be displayed
matrix1 = matrix[1:num + 1, 1:num + 1]
c = plt.pcolor(matrix1, edgecolors='k', linewidths=2, cmap= 'jet')
plt.colorbar(c)
plt.axis([0, num, 0, num])
plt.show()
