import matplotlib.pyplot as plt
import numpy as np
import read_in

# # dataset1 fitness plot
d1fitness = read_in.d1fitness()

my_range = np.arange(-5, 5.0, step=.01)
    
fig, ax = plt.subplots()
x = np.array(d1fitness['Generation'].tolist(), dtype='float')
y = np.array(d1fitness['Fitness'].tolist(), dtype='float')

ax.plot(x, y, label='f(x) = x^2-6x+14', color='C2')

plt.xticks([0,1,2,3,4])
ax.set_yscale('log')
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness of Best Candidate Function')
ax.legend()
plt.suptitle('Fitness Values of Candidate Functions for Dataset1')
plt.show()

# dataset1 MSE plot
d1mse = read_in.d1mse()

my_range = np.arange(-5, 5.0, step=.01)
    
fig, ax = plt.subplots()
x = np.array(d1mse['Generation'].tolist(), dtype='float')
y = np.array(d1mse['MSE'].tolist(), dtype='float')

ax.plot(x, y, label='f(x) = x^2-6x+14', color='C3')

plt.xticks([0,1,2,3,4])
ax.set_xlabel('Generation')
ax.set_ylabel('Mean Squared Error of Best Candidate Function')
ax.legend()
plt.suptitle('Mean Squared Error of Candidate Functions for Dataset1')
plt.show()

# dataset2 fitness values
d2fitness1 = read_in.d2fitness1()
d2fitness2 = read_in.d2fitness2()
d2fitness3 = read_in.d2fitness3()
d2fitness4 = read_in.d2fitness4()
d2fitness5 = read_in.d2fitness5()


my_range = np.arange(-5, 5.0, step=.01)
    
fig, ax = plt.subplots()
x1 = np.array(d2fitness1['Generation'].tolist(), dtype='float')
y1 = np.array(d2fitness1['Fitness'].tolist(), dtype='float')
x2 = np.array(d2fitness2['Generation'].tolist(), dtype='float')
y2 = np.array(d2fitness2['Fitness'].tolist(), dtype='float')
x3 = np.array(d2fitness3['Generation'].tolist(), dtype='float')
y3 = np.array(d2fitness3['Fitness'].tolist(), dtype='float')
x4 = np.array(d2fitness4['Generation'].tolist(), dtype='float')
y4 = np.array(d2fitness4['Fitness'].tolist(), dtype='float')
x5 = np.array(d2fitness5['Generation'].tolist(), dtype='float')
y5 = np.array(d2fitness5['Fitness'].tolist(), dtype='float')

ax.plot(x1, y1,label='Trial 1', color='blue')
ax.plot(x2, y2,label='Trial 2', color='green')
ax.plot(x3, y3,label='Trial 3', color='red')
ax.plot(x4, y4,label='Trial 4', color='orange')
ax.plot(x5, y5,label='Trial 5', color='black')

# plt.xticks([])
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness Values of Best Candidate Function')
ax.legend()
plt.suptitle('Fitness Values of Candidate Functions for Dataset2')
plt.show()

# dataset2 MSE values
d2mse1 = read_in.d2mse1()
d2mse2 = read_in.d2mse2()
d2mse3 = read_in.d2mse3()
d2mse4 = read_in.d2mse4()
d2mse5 = read_in.d2mse5()

my_range = np.arange(-5, 5.0, step=.01)
    
fig, ax = plt.subplots()
x1 = np.array(d2mse1['Generation'].tolist(), dtype='float')
y1 = np.array(d2mse1['MSE'].tolist(), dtype='float')
x2 = np.array(d2mse2['Generation'].tolist(), dtype='float')
y2 = np.array(d2mse2['MSE'].tolist(), dtype='float')
x3 = np.array(d2mse3['Generation'].tolist(), dtype='float')
y3 = np.array(d2mse3['MSE'].tolist(), dtype='float')
x4 = np.array(d2mse4['Generation'].tolist(), dtype='float')
y4 = np.array(d2mse4['MSE'].tolist(), dtype='float')
x5 = np.array(d2mse5['Generation'].tolist(), dtype='float')
y5 = np.array(d2mse5['MSE'].tolist(), dtype='float')

ax.plot(x1, y1,label='Trial 1', color='blue')
ax.plot(x2, y2,label='Trial 2', color='green')
ax.plot(x3, y3,label='Trial 3', color='red')
ax.plot(x4, y4,label='Trial 4', color='orange')
ax.plot(x5, y5,label='Trial 5', color='black')

ax.set_yscale('log')
ax.set_xlabel('Generation')
ax.set_ylabel('Mean Squared Error of Best Candidate Function')
ax.legend()
plt.suptitle('Mean Squared Error of Candidate Functions for Dataset2')
plt.show()


