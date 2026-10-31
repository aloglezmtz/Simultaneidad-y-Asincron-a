"""Práctica 5 · Simultaneidad y Asincronía.

Simula la descarga de 4 archivos con duración aleatoria y compara:
  1) Ejecución secuencial (bloqueante)      -> time.sleep()
  2) Ejecución asincrónica (no bloqueante)  -> async / await / asyncio.gather()

Uso:   python descargas.py            (duraciones aleatorias distintas en cada corrida)
       python descargas.py --semilla 7 (mismas duraciones en ambos bloques y reproducibles)

Nota para Google Colab / Jupyter: ahí ya existe un bucle de eventos en marcha, por lo
que en lugar de asyncio.run(...) se escribe:   await main_asincrono(duraciones)
"""
import argparse
import asyncio
import random
import time

ARCHIVOS = ["video.mp4", "documento.pdf", "imagen.png", "datos.csv"]


def generar_duraciones(n=4, minimo=1.0, maximo=4.0, semilla=None):
    """Duración (s) aleatoria para cada archivo. Se generan UNA sola vez y se usan en
    ambos enfoques, para que la comparación sea justa."""
    rng = random.Random(semilla)
    return [round(rng.uniform(minimo, maximo), 2) for _ in range(n)]


# --------------------------------------------------------------------------- #
# 1) BLOQUE SECUENCIAL (bloqueante)
# --------------------------------------------------------------------------- #
def descargar_sync(nombre, duracion, t0, eventos, verbose=True):
    inicio = time.perf_counter() - t0
    if verbose:
        print(f"[{inicio:6.2f} s] Iniciando  {nombre} (durará {duracion:.2f} s)")
    time.sleep(duracion)                      # BLOQUEA: nada más puede ejecutarse
    fin = time.perf_counter() - t0
    if verbose:
        print(f"[{fin:6.2f} s] Terminó     {nombre}")
    eventos.append((nombre, inicio, fin, duracion))


def ejecutar_secuencial(duraciones, nombres=None, verbose=True):
    nombres = nombres or [f"archivo_{i + 1}" for i in range(len(duraciones))]
    eventos = []
    t0 = time.perf_counter()
    for nombre, dur in zip(nombres, duraciones):
        descargar_sync(nombre, dur, t0, eventos, verbose)
    return time.perf_counter() - t0, eventos


# --------------------------------------------------------------------------- #
# 2) BLOQUE ASINCRÓNICO (no bloqueante)
# --------------------------------------------------------------------------- #
async def descargar_async(nombre, duracion, t0, eventos, verbose=True):
    inicio = time.perf_counter() - t0
    if verbose:
        print(f"[{inicio:6.2f} s] Iniciando  {nombre} (durará {duracion:.2f} s)")
    await asyncio.sleep(duracion)             # CEDE el control: otras descargas avanzan
    fin = time.perf_counter() - t0
    if verbose:
        print(f"[{fin:6.2f} s] Terminó     {nombre}")
    eventos.append((nombre, inicio, fin, duracion))


async def main_asincrono(duraciones, nombres=None, verbose=True):
    nombres = nombres or [f"archivo_{i + 1}" for i in range(len(duraciones))]
    eventos = []
    t0 = time.perf_counter()
    await asyncio.gather(*(descargar_async(n, d, t0, eventos, verbose)
                           for n, d in zip(nombres, duraciones)))
    return time.perf_counter() - t0, eventos


def ejecutar_asincrono(duraciones, nombres=None, verbose=True):
    return asyncio.run(main_asincrono(duraciones, nombres, verbose))


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Práctica 5: secuencial vs asincrónico")
    ap.add_argument("--semilla", type=int, default=None, help="semilla para reproducir las duraciones")
    args = ap.parse_args()

    duraciones = generar_duraciones(len(ARCHIVOS), semilla=args.semilla)
    print("Duraciones simuladas:", dict(zip(ARCHIVOS, duraciones)))
    print(f"Suma de duraciones: {sum(duraciones):.2f} s | Mayor duración: {max(duraciones):.2f} s\n")

    print("=== BLOQUE 1: ejecución SECUENCIAL (bloqueante) ===")
    t_sec, _ = ejecutar_secuencial(duraciones, ARCHIVOS)
    print(f"--> Tiempo total secuencial: {t_sec:.2f} s\n")

    print("=== BLOQUE 2: ejecución ASINCRÓNICA (asyncio.gather) ===")
    t_asy, _ = ejecutar_asincrono(duraciones, ARCHIVOS)
    print(f"--> Tiempo total asincrónico: {t_asy:.2f} s\n")

    print("=== TABLA COMPARATIVA ===")
    print(f"{'Enfoque':<22}{'Tiempo total (s)':>18}")
    print(f"{'Secuencial':<22}{t_sec:>18.2f}")
    print(f"{'Asincrónico':<22}{t_asy:>18.2f}")
    print(f"{'Aceleración':<22}{t_sec / t_asy:>17.2f}x")
    print(f"{'Tiempo ahorrado':<22}{t_sec - t_asy:>16.2f} s")


if __name__ == "__main__":
    main()
