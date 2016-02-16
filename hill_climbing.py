import sys
import math
from scipy import optimize
import numpy as np

debugging = False

def frange(start, stop, step):
	i = start
	while i < stop:
		yield i
		i += step


def f(x):
	try:	
		return -(np.sin(x*x/2) / np.sqrt(x))
	except ZeroDivisionError:
		return -sys.maxint - 1


def neighbors(x, dx, xmin, xmax):
	"Generate neighbors of a location x"
	x0 = max(x-dx, xmin, key=float)
	x1 = min(x+dx, xmax, key=float)
	return [x0, x1]


def hill_climbing(f, x, dx, xmin, xmax, steps=100000):
	"Search for an x that maximizes f(x), considering neighbors(x)"
	fx = f(x)
	steps_to_convergence = 0
	try:
		neighborhood = iter(neighbors(x, dx, xmin, xmax))
		for i in range(steps):
			steps_to_convergence += 1
			x2 = neighborhood.next()
			fx2 = f(x2)
			if fx2 > fx:
				x, fx = x2, fx2
				neighborhood = iter(neighbors(x, dx, xmin, xmax))
		if debugging: print "hillclimb:', x, int(fx)"
		return x
	except StopIteration:
		return [x,fx,steps_to_convergence]



xmin = 0
xmax = 10
x0 = [1,2,3,4,5,6,7,8,9,10]
delta_x = [0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,1.0]

print("Hill climbing:\n")
for x in x0:
	for dx in delta_x:
		[x_max, fx_max, steps] = hill_climbing(f, x, dx, xmin, xmax)
		print("(x0,dx) = (" + str(x) + "," + str(dx) + ") : (x*,y*) = (" + str(x_max) + "," + str(fx_max) + ") in " + str(steps) + " steps")
	print('\n')


delta_x = [0.01,0.02,0.03,0.04,0.05,0.06]
T = [1000,500,250,100,90,80,70,60,50,25]
print("Simulated Annealing:\n")
for x in x0:
	for dx in delta_x:
		for t in T:
			[xmin, Jmin, T, feval, iters, accept, status] = optimize.anneal(f, x, full_output=True, T0=t, lower=0, upper=10, learn_rate=delta_x)
			print("(x0,dx,T) = (" + str(x) + "," + str(dx) + "," + str(t) + ") : (x*,y*) = (" + str(xmin) + "," + str(-Jmin) + ") in " + str(feval) + " evaluations, " + str(iters) + " cooling iterations")
