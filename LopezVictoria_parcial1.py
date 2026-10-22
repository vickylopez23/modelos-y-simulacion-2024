"""
Modelos y Simulación 2024 - Parcial 1 (23/04/2024)
Victoria López
"""
import math
from random import random


# ===========================================================================
# ENUNCIADO - Ejercicio 1
# Se tienen U y V dos variables aleatorias discretas independientes, ambas con
# distribución uniforme. U toma valores en el intervalo natural 1 <= n <= 1000 y
# V toma valores en el intervalo 100 <= n <= 400.
#   a) Calcular P(U + V = 500).
#   b) Calcular el valor esperado E[UV].
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución
# U ~ Uniforme discreta en {1, ..., 1000}, V ~ Uniforme discreta en {100, ..., 400},
# independientes.
# ---------------------------------------------------------------------------
def ejercicio1():
    nU = 1000           # |{1,...,1000}|
    nV = 400 - 100 + 1  # |{100,...,400}| = 301

    # a) P(U + V = 500) = sum_v P(V = v) P(U = 500 - v).
    #    Para todo v en {100,...,400}, 500 - v está en {100,...,400} ⊂ {1,...,1000},
    #    así que los 301 valores de v aportan (1/301)(1/1000).
    casos = sum(1 for v in range(100, 401) if 1 <= 500 - v <= 1000)
    p_a = casos / (nU * nV)

    # b) Por independencia, E[UV] = E[U] E[V] = (1+1000)/2 * (100+400)/2.
    e_b = (1 + 1000) / 2 * (100 + 400) / 2

    print("Ejercicio 1")
    print(f"  a) P(U + V = 500) = {casos}/({nU}*{nV}) = {p_a}")
    print(f"  b) E[UV] = E[U]E[V] = 500.5 * 250 = {e_b}")


# ===========================================================================
# ENUNCIADO - Ejercicio 2
# En una empresa los empleados van al bar a pedir su almuerzo de acuerdo a un
# proceso de Poisson no homogéneo. La tasa de arribo aumenta linealmente de 1 a 2
# empleados por hora entre las 11:00 y las 12:00. Luego se mantiene constante por
# las siguientes dos horas, y decrece linealmente entre 2 a 1 empleado por hora
# entre las 14:00 y las 15:00.
#   a) Dar la fórmula para la función de intensidad de este proceso de Poisson.
#   b) Dar el número esperado de empleados en el bar entre las 11:30 y las 13:30.
#   c) Calcular la probabilidad de que haya al menos 4 empleados en el bar entre
#      las 11:30 y las 13:30.
#   d) Dado que entre las 11:00 y las 13:30 hubo 5 empleados en el bar, ¿cuál es
#      la probabilidad que haya exactamente 4 empleados entre las 11:30 y las 13:30?
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución
# Tomando t = horas desde las 11:00 (t en [0, 4]):
#   lambda(t) = 1 + t   si 0 <= t < 1   (11:00 a 12:00, crece de 1 a 2)
#   lambda(t) = 2       si 1 <= t < 3   (12:00 a 14:00)
#   lambda(t) = 5 - t   si 3 <= t <= 4  (14:00 a 15:00, decrece de 2 a 1)
# ---------------------------------------------------------------------------
def media_poisson_11_a(a, b):
    """m(a,b) = integral de lambda en [a, b] (a, b en [0, 1] o [1, 3] según el caso)."""
    def Lambda(t):  # primitiva de lambda, Lambda(0) = 0
        if t < 1:
            return t + t**2 / 2
        if t < 3:
            return 1.5 + 2 * (t - 1)
        return 5.5 + 5 * (t - 3) - (t**2 - 9) / 2
    return Lambda(b) - Lambda(a)


def poisson_pmf(k, m):
    return math.exp(-m) * m**k / math.factorial(k)


def ejercicio2():
    # b) 11:30 -> t = 0.5 ; 13:30 -> t = 2.5
    m = media_poisson_11_a(0.5, 2.5)   # 0.875 + 3 = 3.875

    # c) N(0.5, 2.5) ~ Poisson(m)
    p_c = 1 - sum(poisson_pmf(k, m) for k in range(4))

    # d) N(0, 0.5) y N(0.5, 2.5) son independientes, con N(0, 2.5) = 5.
    #    Condicionado al total, N(0.5, 2.5) ~ Bin(5, m / m_total).
    m_total = media_poisson_11_a(0, 2.5)   # 0.625 + 3.875 = 4.5
    q = m / m_total
    p_d = math.comb(5, 4) * q**4 * (1 - q)

    print("Ejercicio 2")
    print("  a) lambda(t) = 1+t (0<=t<1), 2 (1<=t<3), 5-t (3<=t<=4), t = horas desde las 11:00")
    print(f"  b) E[N(11:30, 13:30)] = {m}")
    print(f"  c) P(N >= 4) = {p_c:.6f}")
    print(f"  d) P(N(11:30,13:30) = 4 | N(11:00,13:30) = 5) = 5 q^4 (1-q), q = {m}/{m_total} -> {p_d:.6f}")


# ===========================================================================
# ENUNCIADO - Ejercicio 3
# Se desea determinar mediante Monte Carlo el valor de la integral
#     I = integral_1^inf  1 / (x^2 ln(x + 1)) dx.
#   a) Explicar y fundamentar cómo se estima mediante simulación el valor de esta
#      integral por el método de Monte Carlo. Asumir que esta integral es convergente.
#   b) ▶ Escribir un programa monte_carlo(N) que estime el valor de la integral con
#      N simulaciones. Utilizar el programa para completar la siguiente tabla.
#      Completar la tabla con 6 decimales.
#          N° de sim. | Integral
#               1 000 |
#              10 000 |
#             100 000 |
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución
# I = integral_1^inf 1 / (x^2 ln(x+1)) dx
# Cambio de variable x = 1/u, dx = -du/u^2 (u en (0, 1]):
#   I = integral_0^1 (1/u^2) * u^2 / ln(1/u + 1) du = integral_0^1 1 / ln(1 + 1/u) du
#     = E[g(U)], U ~ U(0,1), con g(u) = 1 / ln(1 + 1/u).
# Por la ley de los grandes números, (1/N) sum g(U_i) -> I.
# ---------------------------------------------------------------------------
def g3(u):
    return 1 / math.log(1 + 1 / u)


def monte_carlo(N):
    suma = 0.0
    for _ in range(N):
        u = 1 - random()          # u en (0, 1], evita dividir por 0
        suma += g3(u)
    return suma / N


def ejercicio3():
    print("Ejercicio 3")
    print(f"  {'N° de sim.':>10} | Integral")
    for N in [1_000, 10_000, 100_000]:
        print(f"  {N:>10} | {monte_carlo(N):.6f}")


if __name__ == "__main__":
    ejercicio1()
    print()
    ejercicio2()
    print()
    ejercicio3()
