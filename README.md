# Práctica 5 · Simultaneidad y Asincronía

Script en Python que simula la descarga de **4 archivos con duración aleatoria** y compara la ejecución **secuencial (bloqueante)** con la **asincrónica (no bloqueante)** usando `async`, `await` y `asyncio.gather()`. Incluye una página interactiva que muestra la diferencia en tiempo real.

**Alumna:** Alondra Goretti González Martínez (218534681) · **Materia:** Programación Paralela y Concurrente · CUCEI · **Profesor:** Mtro. Zeus Emanuel Gutiérrez Cobián

## Contenido

| Archivo / carpeta | Descripción |
|---|---|
| `index.html` | Página interactiva (se publica con GitHub Pages) |
| `descargas.py` | **Código de la práctica**: bloque secuencial, bloque asincrónico y tabla comparativa |
| `experimento.py` | Experimento completo: corrida única, 10 repeticiones y escalamiento; genera CSV y gráficas |
| `requirements.txt` | Dependencias de Python |
| `resultados/` | `corrida_unica.csv`, `repeticiones.csv`, `resumen.csv`, `escalamiento.csv` |
| `figs/` | Línea de tiempo, repeticiones y escalamiento |
| `informe/` | Informe en PDF (`Practica5_Asincronia_Informe.pdf`), `generar_informe.py` para regenerarlo y `assets/` (logo) |
| `.github/workflows/asyncio.yml` | Ejecuta los scripts en GitHub Actions |
| `.nojekyll` | Indica a GitHub Pages que sirva los archivos tal cual |

## Ejecutar en tu computadora

```bash
pip install -r requirements.txt
python descargas.py                 # lo que pide la práctica (tiempos aleatorios)
python descargas.py --semilla 2025  # mismas duraciones siempre (reproducible)
python experimento.py               # tablas y gráficas (~2 min); --rapido para probar
```

`descargas.py` solo usa la biblioteca estándar. En **Google Colab / Jupyter** ya existe un bucle de eventos, así que en lugar de `asyncio.run(...)` escribe `await main_asincrono(duraciones)`.

## Regenerar el informe

El informe sigue el formato de la Práctica 4 (portada UdeG, banners, código y terminal en ventanas). Los datos de portada están al inicio de `informe/generar_informe.py`. Después de `experimento.py` ejecuta:

```bash
python informe/generar_informe.py
```

## Publicar en GitHub Pages (paso a paso)

1. En GitHub crea un repositorio nuevo (por ejemplo `asincronia-descargas`) como **Public**.
2. **Add file → Upload files**, arrastra **todo el contenido** de esta carpeta (incluida `.github`) y confirma con **Commit changes**.
3. **Settings → Pages**: *Deploy from a branch*, rama `main`, carpeta `/ (root)`, guardar.
4. En uno o dos minutos la página queda en `https://TU-USUARIO.github.io/asincronia-descargas/`.

Con Git en la terminal:

```bash
git init
git add .
git commit -m "Practica 5 asincronia"
git branch -M main
git remote add origin https://github.com/TU-USUARIO/asincronia-descargas.git
git push -u origin main
```

## Ejecutar Python en GitHub (Actions)

Cada `push` lanza la pestaña **Actions**, que corre `descargas.py` y `experimento.py` y guarda `resultados/` y `figs/` como artefacto descargable (*resultados-asyncio*). También se puede lanzar a mano con **Run workflow**.

## Idea principal

Con descargas independientes, el tiempo secuencial es la **suma** de las duraciones y el asincrónico es aproximadamente la **mayor** de ellas, porque mientras una descarga espera, el bucle de eventos avanza las demás.
