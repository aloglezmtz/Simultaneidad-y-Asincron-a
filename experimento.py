"""Práctica 5 · Experimento completo: tablas, CSV y gráficas.

Genera:
  resultados/corrida_unica.csv     tiempo de cada archivo en una corrida (semilla fija)
  resultados/repeticiones.csv      N corridas con duraciones distintas
  resultados/escalamiento.csv      tiempo vs número de archivos
  figs/*.png                       gráficas usadas en el informe y en la página

Uso:  python experimento.py            (≈ 2 min: usa sleeps reales)
      python experimento.py --rapido   (duraciones 10 veces menores, para probar)
"""
import argparse
import os
import statistics as st

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from descargas import (ARCHIVOS, ejecutar_asincrono, ejecutar_secuencial,
                       generar_duraciones)

SEMILLA = 2025
REPETICIONES = 10
C_SEC, C_ASY = "#d95f02", "#1b9e77"


def corrida_unica(escala):
    dur = [round(d * escala, 2) for d in generar_duraciones(4, semilla=SEMILLA)]
    t_sec, ev_sec = ejecutar_secuencial(dur, ARCHIVOS, verbose=False)
    t_asy, ev_asy = ejecutar_asincrono(dur, ARCHIVOS, verbose=False)
    filas = []
    for enfoque, evs in (("Secuencial", ev_sec), ("Asincrónico", ev_asy)):
        for nombre, ini, fin, d in sorted(evs, key=lambda e: ARCHIVOS.index(e[0])):
            filas.append(dict(enfoque=enfoque, archivo=nombre, duracion_s=d,
                              inicio_s=round(ini, 3), fin_s=round(fin, 3)))
    pd.DataFrame(filas).to_csv("resultados/corrida_unica.csv", index=False)
    print(f"Corrida única  secuencial={t_sec:.2f}s  asincrónico={t_asy:.2f}s")

    # Gráfica tipo Gantt
    fig, ax = plt.subplots(1, 2, figsize=(12, 3.6), sharex=True)
    for a, (titulo, evs, t, col) in zip(ax, (("Secuencial (bloqueante)", ev_sec, t_sec, C_SEC),
                                              ("Asincrónico (asyncio.gather)", ev_asy, t_asy, C_ASY))):
        for i, nombre in enumerate(ARCHIVOS):
            _, ini, fin, _ = next(e for e in evs if e[0] == nombre)
            a.barh(i, fin - ini, left=ini, color=col, edgecolor="white")
            a.text(ini + (fin - ini) / 2, i, f"{fin - ini:.2f}s", ha="center", va="center", color="white", fontsize=9)
        a.axvline(t, color="black", ls="--", lw=1)
        a.set_yticks(range(len(ARCHIVOS))); a.set_yticklabels(ARCHIVOS); a.invert_yaxis()
        a.set_title(f"{titulo}: {t:.2f} s"); a.set_xlabel("Tiempo (s)")
        a.grid(axis="x", alpha=.3)
    fig.tight_layout(); fig.savefig("figs/linea_de_tiempo.png", dpi=150); plt.close(fig)

    fig, a = plt.subplots(figsize=(4.8, 3.6))
    b = a.bar(["Secuencial", "Asincrónico"], [t_sec, t_asy], color=[C_SEC, C_ASY])
    a.bar_label(b, fmt="%.2f s"); a.set_ylabel("Tiempo total (s)")
    a.set_title("Corrida única (4 archivos)"); fig.tight_layout()
    fig.savefig("figs/corrida_unica.png", dpi=150); plt.close(fig)


def repeticiones(escala):
    filas = []
    for r in range(1, REPETICIONES + 1):
        dur = [round(d * escala, 2) for d in generar_duraciones(4, semilla=SEMILLA + r)]
        t_sec, _ = ejecutar_secuencial(dur, verbose=False)
        t_asy, _ = ejecutar_asincrono(dur, verbose=False)
        filas.append(dict(corrida=r, duraciones=" / ".join(f"{d:.2f}" for d in dur),
                          suma_duraciones=round(sum(dur), 2), mayor_duracion=max(dur),
                          t_secuencial=round(t_sec, 3), t_asincrono=round(t_asy, 3),
                          aceleracion=round(t_sec / t_asy, 2)))
        print(f"Corrida {r:2d}: sec={t_sec:6.2f}s  asy={t_asy:6.2f}s  x{t_sec / t_asy:.2f}")
    df = pd.DataFrame(filas); df.to_csv("resultados/repeticiones.csv", index=False)

    fig, a = plt.subplots(figsize=(8, 3.8))
    a.plot(df.corrida, df.t_secuencial, "o-", color=C_SEC, label="Secuencial")
    a.plot(df.corrida, df.t_asincrono, "s-", color=C_ASY, label="Asincrónico")
    a.plot(df.corrida, df.mayor_duracion, ":", color="gray", label="Mayor duración individual")
    a.set_xlabel("Corrida"); a.set_ylabel("Tiempo total (s)"); a.set_xticks(df.corrida)
    a.legend(); a.grid(alpha=.3); a.set_title(f"{REPETICIONES} corridas con duraciones aleatorias")
    fig.tight_layout(); fig.savefig("figs/repeticiones.png", dpi=150); plt.close(fig)

    res = pd.DataFrame({
        "metrica": ["promedio", "desv_estandar", "minimo", "maximo"],
        "secuencial_s": [st.mean(df.t_secuencial), st.stdev(df.t_secuencial), df.t_secuencial.min(), df.t_secuencial.max()],
        "asincrono_s": [st.mean(df.t_asincrono), st.stdev(df.t_asincrono), df.t_asincrono.min(), df.t_asincrono.max()],
    }).round(3)
    res.to_csv("resultados/resumen.csv", index=False)
    print(res.to_string(index=False))


def escalamiento():
    filas = []
    for n in (1, 2, 4, 8, 16, 32):
        dur = generar_duraciones(n, 0.1, 0.5, semilla=SEMILLA)
        t_sec, _ = ejecutar_secuencial(dur, verbose=False)
        t_asy, _ = ejecutar_asincrono(dur, verbose=False)
        filas.append(dict(n_archivos=n, t_secuencial=round(t_sec, 3), t_asincrono=round(t_asy, 3),
                          aceleracion=round(t_sec / t_asy, 2)))
    df = pd.DataFrame(filas); df.to_csv("resultados/escalamiento.csv", index=False)
    print(df.to_string(index=False))
    fig, a = plt.subplots(figsize=(6.4, 3.8))
    a.plot(df.n_archivos, df.t_secuencial, "o-", color=C_SEC, label="Secuencial")
    a.plot(df.n_archivos, df.t_asincrono, "s-", color=C_ASY, label="Asincrónico")
    a.set_xlabel("Número de archivos (0.1–0.5 s c/u)"); a.set_ylabel("Tiempo total (s)")
    a.legend(); a.grid(alpha=.3); a.set_title("Escalamiento con el número de descargas")
    fig.tight_layout(); fig.savefig("figs/escalamiento.png", dpi=150); plt.close(fig)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true", help="duraciones 10 veces menores")
    escala = 0.1 if ap.parse_args().rapido else 1.0
    os.makedirs("resultados", exist_ok=True); os.makedirs("figs", exist_ok=True)
    corrida_unica(escala); repeticiones(escala); escalamiento()
