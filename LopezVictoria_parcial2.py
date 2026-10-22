"""
Modelos y Simulación 2024 - Parcial 2 (16/05/2024)
Victoria López
"""
import math
from random import random


# ===========================================================================
# ENUNCIADO - Ejercicio 1
# El siguiente código simula valores de una variable aleatoria X.
#
#     from random import random
#     A = [0,1,1,2,2,2,3,3,3]
#     B = [0,0,0,1,1,2,2,2,2,2]
#     def UrnaX():
#         U = random()
#         if U < 0.9:
#             return A[int(random() * 9)]
#         else:
#             return B[int(random() * 10)]
#
#   a) Dar la función de probabilidad de masa de la variable X.
#   b) Dar un algoritmo basado en el método de aceptación y rechazo para generar
#      valores de la misma variable. ▶ Escribir el correspondiente código en Python
#      algo_x(p) cuyo argumento sea el vector de probabilidades de X.
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución
# UrnaX: con prob 0.9 elige uniforme en A = [0,1,1,2,2,2,3,3,3] y con prob 0.1
# uniforme en B = [0,0,0,1,1,2,2,2,2,2].
#   p0 = 0.9*1/9 + 0.1*3/10 = 0.13
#   p1 = 0.9*2/9 + 0.1*2/10 = 0.22
#   p2 = 0.9*3/9 + 0.1*5/10 = 0.35
#   p3 = 0.9*3/9 + 0.1*0/10 = 0.30
# Aceptación y rechazo con Y ~ U{0,1,2,3} (q_j = 1/4):
#   c = max_j p_j / q_j = 0.35 / 0.25 = 1.4
#   Generar Y, U; si U < p_Y / (c q_Y) devolver Y, si no repetir.
# ---------------------------------------------------------------------------
P_X = [0.13, 0.22, 0.35, 0.30]


def algo_x(p):
    k = len(p)
    q = 1 / k
    c = max(p) / q
    while True:
        y = int(random() * k)            # Y uniforme en {0, ..., k-1}
        if random() < p[y] / (c * q):
            return y


def ejercicio1():
    n_sim = 100_000
    frec = [0] * len(P_X)
    for _ in range(n_sim):
        frec[algo_x(P_X)] += 1
    print("Ejercicio 1")
    print(f"  a) p(X=0)={P_X[0]}, p(X=1)={P_X[1]}, p(X=2)={P_X[2]}, p(X=3)={P_X[3]}")
    print(f"  b) c = {max(P_X) / 0.25}. Frecuencias con algo_x ({n_sim} sim.):")
    for j, f in enumerate(frec):
        print(f"     X={j}: {f / n_sim:.4f}  (teórico {P_X[j]})")


# ===========================================================================
# ENUNCIADO - Ejercicio 2
# Considerar una variable aleatoria X con función de densidad f dada por:
#     f(x) = sqrt(x)   si 0 <= x < 1
#            1/3       si 1 <= x <= 2
#            0         en cualquier otro caso.
#   a) Explicar cómo se aplica el método de la transformada inversa para obtener un
#      algoritmo que simula valores de X. Considerar U ~ U(0, 1). Calcular
#      explícitamente el valor de X que devuelve el algoritmo para cada uno de los
#      siguientes valores de U: U = 0.2, U = 0.5, U = 0.8.
#   b) ▶ Escribir un código en Python ejercicio2() que genere valores de X según a).
#      Utilizar este código para estimar P(X > 4).
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución
# f(x) = sqrt(x) en [0,1), 1/3 en [1,2].
#   F(x) = (2/3) x^(3/2)          si 0 <= x < 1   (F(1) = 2/3)
#   F(x) = 2/3 + (x - 1)/3        si 1 <= x <= 2
# Inversa:
#   U < 2/3  -> X = (3U/2)^(2/3)
#   U >= 2/3 -> X = 3U - 1
# U=0.2 -> 0.3^(2/3) ≈ 0.4481 ; U=0.5 -> 0.75^(2/3) ≈ 0.8255 ; U=0.8 -> 1.4
# ---------------------------------------------------------------------------
def inversa_ej2(u):
    if u < 2 / 3:
        return (3 * u / 2) ** (2 / 3)
    return 3 * u - 1


def gen_ej2():
    return inversa_ej2(random())


def ejercicio2():
    n_sim = 10_000
    exitos = sum(1 for _ in range(n_sim) if gen_ej2() > 4)
    print("Ejercicio 2")
    for u in [0.2, 0.5, 0.8]:
        print(f"  a) U = {u} -> X = {inversa_ej2(u):.4f}")
    print(f"  b) P(X > 4) estimada con {n_sim} sim.: {exitos / n_sim}"
          " (X toma valores en [0, 2], así que P(X > 4) = 0)")


# ===========================================================================
# ENUNCIADO - Ejercicio 3
# Considerar un proceso de Poisson no homogéneo con función de intensidad dada por:
#     lambda(t) = 5 + 5t    si 0 <= t < 3
#                 20        si 3 <= t <= 5
#                 30 - 2t   si 5 < t <= 9.
#   a) Suponer que se aplica el método de adelgazamiento para simular los tiempos de
#      arribos utilizando un proceso de Poisson homogéneo con tasa lambda = 20.
#      ¿Con qué probabilidad se contará un evento del proceso homogéneo en t = 4 y
#      con qué probabilidad en t = 7?
#   b) ▶ Escribir en Python un código hot_dog(T) aplicando el método de
#      adelgazamiento mejorado. El programa debe devolver un arreglo con todos los
#      tiempos de arribo hasta el tiempo T (0 <= T <= 9). Para esto particionar el
#      intervalo [0, 9] en subintervalos con extremos en 0, 1, 2, 6, 8 y 9. Usar este
#      código para estimar el número esperado de arribos en el intervalo [0, 9].
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución - Poisson no homogéneo, adelgazamiento mejorado
# a) Con lambda = 20: P(contar en t=4) = lambda(4)/20 = 20/20 = 1
#                     P(contar en t=7) = lambda(7)/20 = 16/20 = 0.8
# b) Subintervalos [0,1], [1,2], [2,6], [6,8], [8,9] con cota lambda_j = máx de
#    lambda en cada uno: 10, 15, 20, 18, 14.
#    E[N(9)] = integral_0^9 lambda = 37.5 + 40 + 64 = 141.5
# ---------------------------------------------------------------------------
def lamda_ej3(t):
    if 0 <= t < 3:
        return 5 + 5 * t
    if 3 <= t <= 5:
        return 20
    if 5 < t <= 9:
        return 30 - 2 * t
    return 0


EXTREMOS = [1, 2, 6, 8, 9]        # extremos derechos de los subintervalos
LAMDAS = [10, 15, 20, 18, 14]     # cotas superiores de lambda en cada uno


def hot_dog(T):
    """Tiempos de arribo en [0, T] por adelgazamiento mejorado (0 <= T <= 9)."""
    eventos = []
    j = 0
    t = 0.0
    x = -math.log(1 - random()) / LAMDAS[j]
    while t <= T:
        # Si el salto se pasa del subintervalo actual, se reescala al siguiente.
        while t + x > EXTREMOS[j]:
            if j == len(EXTREMOS) - 1:
                return eventos
            x = (x - (EXTREMOS[j] - t)) * LAMDAS[j] / LAMDAS[j + 1]
            t = EXTREMOS[j]
            j += 1
        t += x
        if t > T:
            break
        if random() < lamda_ej3(t) / LAMDAS[j]:
            eventos.append(t)
        x = -math.log(1 - random()) / LAMDAS[j]
    return eventos


def ejercicio3():
    n_sim = 10_000
    total = sum(len(hot_dog(9)) for _ in range(n_sim))
    print("Ejercicio 3")
    print(f"  a) P(contar en t=4) = {lamda_ej3(4) / 20}, P(contar en t=7) = {lamda_ej3(7) / 20}")
    print(f"  b) N° esperado de arribos en [0, 9] ({n_sim} sim.): {total / n_sim:.4f}"
          " (valor exacto: 141.5)")


# ===========================================================================
# ENUNCIADO - Ejercicio 4
# Se desea estimar mediante Monte Carlo el área encerrada por la curva en el plano
# cuyos puntos satisfacen la ecuación:
#     x^2 + (y - |x|^(3/2))^2 = 1.
# La curva queda contenida en el interior del rectángulo con vértices en
# (-1.5, -1.5), (-1.5, 1.5), (1.5, 1.5) y (1.5, -1.5) (gráfico en la Figura 1 del
# enunciado).
#   a) Explicar y fundamentar cómo se estima mediante simulación el área encerrada
#      por la curva por el método de Monte Carlo.
#   b) ▶ Escribir un programa area(N) que estime el área con N simulaciones. Dar el
#      valor obtenido para N = 100000 utilizando 6 decimales.
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución
# Se generan puntos uniformes en el rectángulo R = [-1.5, 1.5] x [-1.5, 1.5]
# (área 9). La proporción de puntos que cae dentro de la curva estima
# área(región)/área(R). Dentro: x^2 + (y - |x|^(3/2))^2 <= 1.
# (Como la región es un disco de radio 1 "corrido" verticalmente, su área es pi.)
# ---------------------------------------------------------------------------
def area(N):
    dentro = 0
    for _ in range(N):
        x = -1.5 + 3 * random()
        y = -1.5 + 3 * random()
        if x**2 + (y - abs(x) ** 1.5) ** 2 <= 1:
            dentro += 1
    return 9 * dentro / N


def ejercicio4():
    N = 100_000
    print("Ejercicio 4")
    print(f"  b) Área estimada con N = {N}: {area(N):.6f}")


if __name__ == "__main__":
    ejercicio1()
    print()
    ejercicio2()
    print()
    ejercicio3()
    print()
    ejercicio4()
