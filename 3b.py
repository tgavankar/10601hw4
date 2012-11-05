def h1(x):
	return 2.158*x + 6.220

def h2(x):
	return 6.498*(x**2) - 5.013*x + 7.598

def h3(x):
	return -175.6*(x**3) + 293.7*(x**2) + 133.9*x + 20.98

def h4(x):
	return -864.1*(x**4) + 1769*(x**3) - 1770*(x**2) + 278.5*x-11.14

def h5(x):
	return -2297*(x**5) + 5417*(x**4) - 4477*(x**3) + 1570*(x**2) - 230.5*x + 19.1

def h6(x):
	return -2812*(x**6) + 6920*(x**5) - 6289*(x**4)+2763*(x**3) - 671.8*(x**2) + 87.49*x+3.477

obs = [
	(0.1, 7.72),
	(0.2, 8.13),
	(0.4, 6.39),
	(0.5, 3.35),
	(0.6, 3.09),
	(0.8, 12.26),
	(0.9, 17.73),
	(1.0, 0.8)
]

def runOn(h):
	print sum([(h(v[0]) - v[1]) ** 2 for v in obs])
	print 1.0 / len(obs) * sum([1 if (abs(h(v[0]) - v[1]) > .000001) else 0 for v in obs])
	print ""


runOn(h1)
runOn(h2)
runOn(h3)
runOn(h4)
runOn(h5)
runOn(h6)


