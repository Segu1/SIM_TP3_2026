import math
import random


import random
import math

# =======================
# DISTRIBUCIONES
# =======================

def dist_normal(media=15.0, desv=5.0):
    """
    Distribución normal usando Box-Muller.
    Devuelve:
        valor, r1, r2
    """

    r1 = random.random()
    r2 = random.random()

    n1 = (
        math.sqrt(-2 * math.log(r1))
        * math.cos(2 * math.pi * r2)
    ) * desv + media

    valor = max(0, math.trunc(n1))

    return valor, r1, r2


def dist_uniforme_tiempo(a=30, b=95):
    """
    Distribución uniforme.
    Devuelve:
        valor, rnd
    """

    r = random.random()

    valor = math.trunc(a + (b - a) * r)

    return valor, r


def dist_exp_tiempo_extra(media=8):
    """
    Distribución exponencial.
    Devuelve:
        valor, rnd
    """

    r = random.random()

    valor = math.trunc(-media * math.log(1 - r))

    return valor, r


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
    Ejecuta UNA iteración del modelo Monte Carlo.
    """

    # =====================
    # ESTADO
    # =====================

    n = int(state["n"])
    i = int(state["i"])

    total_tiempo = float(state["total_tiempo"])

    cont_edicion_y_extra = int(
        state["cont_edicion_y_extra"]
    )

    cont_sin_pausa_sin_extra = int(
        state["cont_sin_pausa_sin_extra"]
    )

    # NUEVOS CONTADORES

    cont_acciones_extra = int(
        state["cont_acciones_extra"]
    )

    cont_carrusel = int(
        state["cont_carrusel"]
    )

    cont_mayor_60_min = int(
        state["cont_mayor_60_min"]
    )

    max_tiempo = float(state["max_tiempo"])
    min_tiempo = float(state["min_tiempo"])

    # =====================
    # NUEVA ITERACIÓN
    # =====================

    iter_idx = i + 1

    tiempo_total = 0

    # ==================================================
    # FORMATO
    # ==================================================

    rnd_formato = random.random()

    formato = tabla_de_freq_formatos(rnd_formato)

    # ==================================================
    # TIEMPO BASE (UNIFORME)
    # ==================================================

    tiempo_base, rnd_uniforme = dist_uniforme_tiempo()

    tiempo_total += tiempo_base

    # ==================================================
    # EDICIÓN
    # ==================================================

    rnd_edicion = random.random()

    hay_edicion_flag = se_realiza_edicion(rnd_edicion)

    tiempo_edicion = 0

    rnd_norm_r1 = None
    rnd_norm_r2 = None

    if hay_edicion_flag:

        (
            tiempo_edicion,
            rnd_norm_r1,
            rnd_norm_r2
        ) = dist_normal()

        tiempo_total += tiempo_edicion

    # ==================================================
    # DEMORA
    # ==================================================

    rnd_demora = random.random()

    incremento = 0

    if formato in ["imagen", "video"]:

        if hay_demora(rnd_demora):

            incremento = 0.8 * tiempo_base

            tiempo_total += incremento

    # ==================================================
    # ACCIÓN EXTRA
    # ==================================================

    rnd_extra = random.random()

    hay_extra_flag = tabla_accion_extra(rnd_extra)

    tiempo_extra = 0

    rnd_exp = None

    if hay_extra_flag:

        tiempo_extra, rnd_exp = dist_exp_tiempo_extra()

        tiempo_total += tiempo_extra

    # =====================
    # CONTADORES
    # =====================

    if hay_extra_flag:
        cont_acciones_extra += 1

    if formato == "carrusel":
        cont_carrusel += 1

    # MÁS DE 60 MINUTOS

    if tiempo_total > 60:
        cont_mayor_60_min += 1

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

    porcentaje = (
        (cont_edicion_y_extra / i) * 100
        if i > 0 else 0
    )

    porcentaje_mayor_60 = (
        (cont_mayor_60_min / i) * 100
        if i > 0 else 0
    )

    # =====================
    # FILA TABLA
    # =====================

    row = {

        # ================= ITERACIÓN =================

        "Iteración": iter_idx,

        # ================= FORMATO =================

        "rnd_formato":
            round(rnd_formato, 4),

        "Formato":
            formato,

        # ================= UNIFORME =================

        "rnd_uniforme":
            round(rnd_uniforme, 4),

        "Tiempo base":
            tiempo_base,

        # ================= EDICIÓN =================

        "rnd_edic":
            round(rnd_edicion, 4),

        "Edición":
            "Sí" if hay_edicion_flag else "No",

        "rnd_norm_r1":
            round(rnd_norm_r1, 4)
            if rnd_norm_r1 is not None else "-",

        "rnd_norm_r2":
            round(rnd_norm_r2, 4)
            if rnd_norm_r2 is not None else "-",

        "Tiempo edición":
            tiempo_edicion,

        # ================= DEMORA =================

        "rnd_dem":
            round(rnd_demora, 4),

        "Rehacer - Demora":
            "Sí" if incremento > 0 else "No",

        "Incremento":
            round(incremento, 2),

        # ================= EXTRA =================

        "rnd_ext":
            round(rnd_extra, 4),

        "Acc. Extra":
            "Sí" if hay_extra_flag else "No",

        "rnd_exp":
            round(rnd_exp, 4)
            if rnd_exp is not None else "-",

        "Tiempo extra":
            tiempo_extra,

        # ================= RESULTADOS =================

        "Tiempo total":
            round(tiempo_total, 2),

        "Tiempo total acumulado":
            round(total_tiempo, 2),

        "Promedio":
            round(promedio, 2),

        # ================= MÉTRICAS =================

        "Cant de edic + extra":
            cont_edicion_y_extra,

        "% Edición+Extra":
            round(porcentaje, 2),

        "Sin pausa ni extra (acum)":
            cont_sin_pausa_sin_extra,

        "Conteo acciones extra":
            cont_acciones_extra,

        "Conteo carrusel":
            cont_carrusel,

        "Trabajos > 60 min":
            cont_mayor_60_min,

        "% Trabajos > 60 min":
            round(porcentaje_mayor_60, 2),

        "Máximo tiempo":
            round(max_tiempo, 2),

        "Mínimo tiempo":
            round(min_tiempo, 2)
    }

    # =====================
    # NUEVO ESTADO
    # =====================

    new_state = {
        "n": n,
        "i": i,

        "total_tiempo":
            total_tiempo,

        "cont_edicion_y_extra":
            cont_edicion_y_extra,

        "cont_sin_pausa_sin_extra":
            cont_sin_pausa_sin_extra,

        "cont_acciones_extra":
            cont_acciones_extra,

        "cont_carrusel":
            cont_carrusel,

        "cont_mayor_60_min":
            cont_mayor_60_min,

        "max_tiempo":
            max_tiempo,

        "min_tiempo":
            min_tiempo
    }

    return new_state, row


# =======================
# ESTADO INICIAL
# =======================

state = {
    "n": 1000,
    "i": 0,

    "total_tiempo": 0,

    "cont_edicion_y_extra": 0,

    "cont_sin_pausa_sin_extra": 0,

    "cont_acciones_extra": 0,

    "cont_carrusel": 0,

    "cont_mayor_60_min": 0,

    "max_tiempo": 0,

    "min_tiempo": 999999
}