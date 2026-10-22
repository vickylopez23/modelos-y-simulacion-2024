"""
Modelos y Simulación 2024 - Parcial 3 (13/06/2024)
Victoria López

El ejercicio 1 (cadena de Markov) se resuelve en papel; no lleva código.
"""

# ===========================================================================
# ENUNCIADO - Ejercicio 1 (se resuelve en papel)
# Para la cadena de Markov representada en el diagrama del enunciado
# (estados 0, 1, 2 y 3):
#   a) Dar la matriz de transición.
#   b) Determinar los estados recurrentes, transitorios, absorbentes y periódicos.
#   c) Determinar las clases comunicantes y subconjuntos cerrados.
#   d) Para el estado {2} determinar probabilidades de alcance y tiempo medio de
#      alcance desde cada uno de los estados.
#   e) Determinar el tiempo medio de alcance al conjunto A = {2, 3} desde cada uno
#      de los estados.
# ===========================================================================
import math
from random import random

from scipy import stats

NIVEL_RECHAZO = 0.0004   # 0.04 %


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------
def media(xs):
    return sum(xs) / len(xs)


def var_muestral(xs):
    m = media(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def normal_cdf(x, mu, sigma):
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))


def estadistico_ks(valores_F):
    """D = max_j max( j/n - F(x_(j)), F(x_(j)) - (j-1)/n ), con F evaluada en la muestra ordenada."""
    u = sorted(valores_F)
    n = len(u)
    return max(max((j + 1) / n - u[j], u[j] - j / n) for j in range(n))


def binomial(n, p):
    return sum(1 for _ in range(n) if random() < p)


# ===========================================================================
# ENUNCIADO - Ejercicio 2
# Los pesos, medidos en kilogramos, de nueve zapallos recolectados de una huerta
# fueron: 1.628, 1.352, 1.800, 1.420, 1.594, 2.132, 1.614, 1.924 y 1.692.
#   a) Diseñar una prueba de hipótesis usando el estadístico de Kolmogorov-Smirnov,
#      para determinar si los datos provienen de una distribución normal. Indicar
#      los parámetros estimados y las correspondientes estimaciones.
#   b) Calcule el valor del estadístico.
#   c) Defina el p-valor a partir de la hipótesis nula.
#   d) ▶ Determine si la hipótesis nula es rechazada o no, con un nivel de rechazo
#      del 0.04 %. Para esto utilice simulaciones con variables uniformes.
#   e) Suponer que en una de las simulaciones se obtuvieron los siguientes valores
#      para las simulaciones: U1 = 0.23, U2 = 0.12, U3 = 0.45, U4 = 0.67,
#      U5 = 0.01, U6 = 0.51, U7 = 0.38, U8 = 0.92 y U9 = 0.84.
#      ¿Cómo resulta el valor del estadístico para estos datos, en relación al
#      estadístico observado?
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución - Kolmogorov-Smirnov, H0: los pesos provienen de una normal
# Parámetros estimados: mu = media muestral, sigma^2 = varianza muestral (S^2).
# p-valor = P_H0(D >= d). Con variables uniformes: si X ~ F, F(X) ~ U(0,1), así que
# se aproxima P(D >= d) generando n uniformes, calculando su D y contando cuántas
# veces D >= d.
# ---------------------------------------------------------------------------
PESOS = [1.628, 1.352, 1.800, 1.420, 1.594, 2.132, 1.614, 1.924, 1.692]


def pvalor_ks_uniformes(d, n, n_sim):
    exitos = 0
    for _ in range(n_sim):
        if estadistico_ks([random() for _ in range(n)]) >= d:
            exitos += 1
    return exitos / n_sim


def ejercicio2():
    n = len(PESOS)
    mu = media(PESOS)
    sigma = math.sqrt(var_muestral(PESOS))
    d = estadistico_ks([normal_cdf(x, mu, sigma) for x in PESOS])

    n_sim = 10_000
    p_valor = pvalor_ks_uniformes(d, n, n_sim)

    U = [0.23, 0.12, 0.45, 0.67, 0.01, 0.51, 0.38, 0.92, 0.84]
    d_U = estadistico_ks(U)

    print("Ejercicio 2")
    print(f"  a) mu estimada = {mu:.4f}, sigma^2 estimada (S^2) = {sigma**2:.4f} (sigma = {sigma:.4f})")
    print(f"  b) D observado = {d:.4f}")
    print("  c) p-valor = P_H0(D >= d)")
    print(f"  d) p-valor simulado con {n_sim} sim. de uniformes = {p_valor:.4f}")
    if p_valor < NIVEL_RECHAZO:
        print("     Se rechaza H0 al nivel 0.04 %")
    else:
        print("     No se rechaza H0 al nivel 0.04 %")
    relacion = "mayor o igual" if d_U >= d else "menor"
    print(f"  e) D para esas uniformes = {d_U:.4f}, {relacion} que el observado ({d:.4f});"
          f" esa simulación {'sí' if d_U >= d else 'no'} cuenta como éxito para el p-valor")


# ===========================================================================
# ENUNCIADO - Ejercicio 3
# En un vivero se plantaron tres semillas de tomate en cada una de 1000 macetas.
# Al cabo de un tiempo se registraron la cantidad de semillas germinadas por maceta
# obteniendo los siguientes datos:
#     Cantidad de semillas que germinaron |   0 |   1 |   2 |  3
#     Frecuencia                          | 490 | 384 | 111 | 15
#   a) Diseñar una prueba de hipótesis usando el test chi-cuadrado para determinar
#      si los datos provienen de una distribución binomial Bin(3, p). Indicar los
#      parámetros estimados y las correspondientes estimaciones.
#   b) Calcular el valor del estadístico.
#   c) Definir el p-valor a partir de la hipótesis nula.
#   d) ▶ Calcule el p-valor usando simulaciones. Explicar en papel el procedimiento
#      usado.
#   e) Determinar si la hipótesis nula es rechazada o no, con un nivel de rechazo
#      del 0.04 %.
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución - Chi-cuadrado, H0: N° de semillas germinadas por maceta ~ Bin(3, p)
# p estimado = (total de semillas germinadas) / (3 * 1000).
# Grados de libertad = k - 1 - m = 4 - 1 - 1 = 2.
# p-valor simulado: generar 1000 macetas con Bin(3, p_est), re-estimar p,
# recalcular el estadístico y contar cuántas veces T >= t_observado.
# ---------------------------------------------------------------------------
FRECUENCIAS = [490, 384, 111, 15]


def chi2_binomial(frec):
    n = sum(frec)
    p = sum(k * f for k, f in enumerate(frec)) / (3 * n)
    esperadas = [n * math.comb(3, k) * p**k * (1 - p) ** (3 - k) for k in range(4)]
    t = sum((frec[k] - esperadas[k]) ** 2 / esperadas[k] for k in range(4))
    return t, p, esperadas


def ejercicio3():
    t_obs, p_est, esperadas = chi2_binomial(FRECUENCIAS)
    n = sum(FRECUENCIAS)
    p_valor = 1 - stats.chi2.cdf(t_obs, df=2)

    n_sim = 1_000
    exitos = 0
    for _ in range(n_sim):
        frec_sim = [0, 0, 0, 0]
        for _ in range(n):
            frec_sim[binomial(3, p_est)] += 1
        if chi2_binomial(frec_sim)[0] >= t_obs:
            exitos += 1
    p_valor_sim = exitos / n_sim

    print("Ejercicio 3")
    print(f"  a) p estimado = {p_est:.4f}")
    print("     Frecuencias esperadas: " + ", ".join(f"{e:.2f}" for e in esperadas))
    print(f"  b) T observado = {t_obs:.4f}")
    print(f"  c) p-valor = P(chi2_2 >= T) = {p_valor:.6f}")
    print(f"  d) p-valor simulado ({n_sim} sim.) = {p_valor_sim:.4f}")
    if p_valor_sim < NIVEL_RECHAZO:
        print("  e) Se rechaza H0 al nivel 0.04 %")
    else:
        print("  e) No se rechaza H0 al nivel 0.04 %")


# ===========================================================================
# ENUNCIADO - Ejercicio 4
# Estime mediante el método de Monte Carlo el valor de la siguiente integral:
#     I = integral_0^inf  x / (1 + x^4) dx
#   a) ▶ Obtenga mediante simulación en computadora el valor de la estimación I
#      deteniendo la simulación cuando el semi-ancho del intervalo de confianza del
#      95 % sea justo inferior a 0.001.
#   b) ▶ Indique cuál es el número de simulaciones Ns necesarias en la simulación
#      realizada para lograr la condición pedida y complete con los valores
#      obtenidos la siguiente tabla (usando 4 decimales):
#          N° de sim. |  I  |  S  | IC(95 %)
#               1 000 |     |     |
#               5 000 |     |     |
#               7 000 |     |     |
#             Ns =    |     |     |
# ===========================================================================
# ---------------------------------------------------------------------------
# Resolución - I = integral_0^inf x / (1 + x^4) dx  (valor exacto pi/4)
# Cambio de variable x = 1/u - 1, dx = du/u^2:
#   I = integral_0^1 g(u) du, g(u) = f(1/u - 1) / u^2.
# Se simula hasta que el semi-ancho del IC 95 %, z_{0.025} * S / sqrt(n), sea
# menor que 0.001 (con al menos 100 simulaciones). Media y varianza se
# actualizan en forma recursiva.
# ---------------------------------------------------------------------------
def f4(x):
    return x / (1 + x**4)


def g4(u):
    return f4(1 / u - 1) / u**2


def ejercicio4():
    z = 1.96
    cota = 0.001
    tabla_N = {1_000, 5_000, 7_000}
    filas = {}

    u = 1 - random()
    media_n = g4(u)
    s2 = 0.0
    n = 1
    while n < 100 or z * math.sqrt(s2 / n) >= cota:
        n += 1
        x = g4(1 - random())
        media_ant = media_n
        media_n = media_ant + (x - media_ant) / n
        s2 = (1 - 1 / (n - 1)) * s2 + n * (media_n - media_ant) ** 2
        if n in tabla_N:
            filas[n] = (media_n, math.sqrt(s2))
    filas_finales = (n, media_n, math.sqrt(s2))

    print("Ejercicio 4")
    print(f"  {'N° de sim.':>10} | {'I':>8} | {'S':>8} | IC(95 %)")
    for N in sorted(filas):
        m, s = filas[N]
        h = z * s / math.sqrt(N)
        print(f"  {N:>10} | {m:8.4f} | {s:8.4f} | [{m - h:.4f}, {m + h:.4f}]")
    n, m, s = filas_finales
    h = z * s / math.sqrt(n)
    print(f"  {'Ns = ' + str(n):>10} | {m:8.4f} | {s:8.4f} | [{m - h:.4f}, {m + h:.4f}]")
    print(f"  a) I estimada = {m:.4f} (valor exacto pi/4 = {math.pi / 4:.4f})")
    print(f"  b) Ns = {n}")


if __name__ == "__main__":
    ejercicio2()
    print()
    ejercicio3()
    print()
    ejercicio4()
