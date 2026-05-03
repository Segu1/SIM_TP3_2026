import math
import random


# =======================
# DISTRIBUCIONES
# =======================

def dist_normal(media=15.0, desv=5.0) -> int:
    r1 = random.random()
    r2 = random.random()
    n1 = (math.sqrt(-2 * math.log(r1)) * math.cos(2 * math.pi * r2)) * desv + media
    return max(0, math.trunc(n1))


def dist_uniforme_tiempo(a=30, b=95) -> int:
    r = random.random()
    return math.trunc(a + (b - a) * r)


def dist_exp_tiempo_extra(media=8) -> int:
    r = random.random()
    return math.trunc(-media * math.log(1 - r))


# =======================
# TABLAS
# =======================

def tabla_accion_extra(freq: float) -> int:
    return 1 if freq <= 0.25 else 0


def tabla_de_freq_formatos(freq: float) -> str:
    if freq < 0.3:
        return "imagen"
    elif freq < 0.4:
        return "carrusel"
    else:
        return "video"


def se_realiza_edicion(freq: float) -> int:
    return 1 if freq < 0.65 else 0


def hay_demora(freq: float) -> int:
    return 1 if freq <= 0.35 else 0


# =======================
# MONTECARLO STEP
# =======================

def montecarlo_step(state: dict):
    """
    Ejecuta UNA iteración del modelo.
    """

    # -------- estado --------
    n = int(state["n"])
    i = int(state["i"])

    total_tiempo = float(state["total_tiempo"])
    cont_edicion_y_extra = int(state["cont_edicion_y_extra"])
    cont_sin_pausa_sin_extra = int(state["cont_sin_pausa_sin_extra"])

    max_tiempo = float(state["max_tiempo"])
    min_tiempo = float(state["min_tiempo"])

    # =====================
    # SIMULACIÓN
    # =====================

    iter_idx = i + 1
    tiempo_total = 0

    # -------- FORMATO --------
    rnd_formato = random.random()
    formato = tabla_de_freq_formatos(rnd_formato)

    # -------- TIEMPO BASE --------
    tiempo_base = dist_uniforme_tiempo()
    tiempo_total += tiempo_base

    # -------- EDICIÓN --------
    rnd_edicion = random.random()
    hay_edicion_flag = se_realiza_edicion(rnd_edicion)

    tiempo_edicion = 0
    if hay_edicion_flag:
        tiempo_edicion = dist_normal()
        tiempo_total += tiempo_edicion

    # -------- DEMORA --------
    rnd_demora = random.random()
    incremento = 0

    if formato in ["imagen", "video"]:
        if hay_demora(rnd_demora):
            incremento = 0.8 * tiempo_base
            tiempo_total += incremento

    # -------- ACCIÓN EXTRA --------
    rnd_extra = random.random()
    hay_extra_flag = tabla_accion_extra(rnd_extra)

    tiempo_extra = 0
    if hay_extra_flag:
        tiempo_extra = dist_exp_tiempo_extra()
        tiempo_total += tiempo_extra

    # =====================
    # MÉTRICAS
    # =====================

    total_tiempo += tiempo_total

    if hay_edicion_flag and hay_extra_flag:
        cont_edicion_y_extra += 1

    if not hay_edicion_flag and not hay_extra_flag:
        cont_sin_pausa_sin_extra += 1

    max_tiempo = max(max_tiempo, tiempo_total)
    min_tiempo = min(min_tiempo, tiempo_total)

    i = iter_idx

    promedio = total_tiempo / i if i > 0 else 0
    porcentaje = (cont_edicion_y_extra / i) * 100 if i > 0 else 0

    # =====================
    # FILA (tabla)
    # =====================

    row = {
        "Iteración": iter_idx,
        "rnd_formato": round(rnd_formato, 5),
        "Formato": formato,
        "Tiempo base": tiempo_base,
        "rnd_edicion": round(rnd_edicion, 5),
        "Edición": "Sí" if hay_edicion_flag else "No",
        "Tiempo edición": tiempo_edicion,
        "rnd_demora": round(rnd_demora, 5),
        "Demora": "Sí" if incremento > 0 else "No",
        "Incremento": round(incremento, 2),
        "rnd_extra": round(rnd_extra, 5),
        "Extra": "Sí" if hay_extra_flag else "No",
        "Tiempo extra": tiempo_extra,
        "Tiempo total": round(tiempo_total, 2),
        "Promedio acum": round(promedio, 2),
        "% Edición+Extra": round(porcentaje, 2),
        "Sin pausa ni extra (acum)": cont_sin_pausa_sin_extra
    }

    # =====================
    # NUEVO ESTADO
    # =====================

    new_state = {
        "n": n,
        "i": i,
        "total_tiempo": total_tiempo,
        "cont_edicion_y_extra": cont_edicion_y_extra,
        "cont_sin_pausa_sin_extra": cont_sin_pausa_sin_extra,
        "max_tiempo": max_tiempo,
        "min_tiempo": min_tiempo
    }

    return new_state, row, promedio, porcentaje
    

    

   

