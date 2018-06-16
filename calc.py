import math

'Distância euclidiana entre dois pontos'
def distance(p1, p2):
	return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

'Conversão de coordenadas cartesianas para polares'
def cartesian2Polar(x, y):
    rho = math.sqrt(x**2 + y**2)
    phi = math.atan2(y, x)
    return (rho, phi)

'Conversão de coordenadas polares para cartesianas'
def polar2Cartesian(rho, phi):
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return (x, y)

'Conversão de ângulos em quaternion para Euler'
def quaternion2Euler(x, y, z, w):
	t0 = 2 * (w * x + y * z)
	t1 = 1 - 2 * (x * x + y**2)
	X = math.atan2(t0, t1)
	t2 = 2 * (w * y - z * x)
	t2 = +1 if t2 > +1 else t2
	t2 = -1 if t2 < -1 else t2
	Y = math.asin(t2)
	t3 = +2 * (w * z + x * y)
	t4 = +1 - 2 * (y**2 + z * z)
	Z = math.atan2(t3, t4)
	return X, Y, Z