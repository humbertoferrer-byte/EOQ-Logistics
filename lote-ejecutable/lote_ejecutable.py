"""
lote_ejecutable.py

El EOQ te da un número que casi nunca se puede comprar. El proveedor vende por
tarima, el camion cierra en cierto numero de tarimas y el almacen no recibe
fracciones.

Este modulo calcula el EOQ, lo baja al lote que si puedes comprar y te dice
cuanto te costo ese redondeo. Esa ultima parte es la que importa: cerca del
optimo la curva de costo total es plana, asi que redondear casi siempre sale
gratis. Cuando NO sale gratis, quiere decir que la restriccion no es de
planeacion, es de negociacion con el proveedor.

Python 3.8+. Sin dependencias.
"""

from math import sqrt, ceil, floor


# --------------------------------------------------------------------------
# Calculo base
# --------------------------------------------------------------------------

def eoq(demanda_anual, costo_por_orden, costo_mantener_unidad_anual):
    """EOQ clasico. Devuelve la cantidad teorica, casi siempre con decimales."""
    if demanda_anual <= 0:
        raise ValueError("la demanda anual tiene que ser mayor a cero")
    if costo_por_orden <= 0:
        raise ValueError("el costo por orden tiene que ser mayor a cero")
    if costo_mantener_unidad_anual <= 0:
        raise ValueError("el costo de mantener tiene que ser mayor a cero")
    return sqrt(2 * demanda_anual * costo_por_orden / costo_mantener_unidad_anual)


def costo_total_anual(q, demanda_anual, costo_por_orden, costo_mantener_unidad_anual):
    """Costo de ordenar mas costo de mantener, para un lote q."""
    if q <= 0:
        raise ValueError("el lote tiene que ser mayor a cero")
    return (demanda_anual / q) * costo_por_orden + (q / 2) * costo_mantener_unidad_anual


# --------------------------------------------------------------------------
# Restricciones reales de compra
# --------------------------------------------------------------------------

def opciones_comprables(q_teorico, multiplo=1, minimo=None, maximo=None):
    """
    Devuelve los lotes que si se pueden comprar alrededor del EOQ.

    multiplo : unidad indivisible de compra (caja, tarima, camion)
    minimo   : minimo de compra que impone el proveedor
    maximo   : tope por espacio, caducidad o capacidad de camion
    """
    if multiplo <= 0:
        raise ValueError("el multiplo tiene que ser mayor a cero")

    abajo = floor(q_teorico / multiplo) * multiplo
    arriba = ceil(q_teorico / multiplo) * multiplo

    candidatos = {abajo, arriba}
    candidatos.discard(0)

    if minimo:
        candidatos = {c for c in candidatos if c >= minimo}
        if not candidatos:
            # todo quedo por debajo del minimo: el minimo se vuelve el lote
            candidatos = {ceil(minimo / multiplo) * multiplo}
    if maximo:
        candidatos = {c for c in candidatos if c <= maximo}
        if not candidatos:
            candidatos = {floor(maximo / multiplo) * multiplo}

    return sorted(c for c in candidatos if c > 0)


def evaluar(demanda_anual, costo_por_orden, costo_mantener_unidad_anual,
            multiplo=1, minimo=None, maximo=None, umbral_alerta=0.05):
    """
    Calcula el EOQ, elige el mejor lote comprable y mide el sobrecosto.

    umbral_alerta : arriba de este sobrecosto, el redondeo deja de ser gratis.
                    0.05 = 5 por ciento.
    """
    q_t = eoq(demanda_anual, costo_por_orden, costo_mantener_unidad_anual)
    costo_t = costo_total_anual(q_t, demanda_anual, costo_por_orden,
                                costo_mantener_unidad_anual)

    opciones = []
    for q in opciones_comprables(q_t, multiplo, minimo, maximo):
        c = costo_total_anual(q, demanda_anual, costo_por_orden,
                              costo_mantener_unidad_anual)
        opciones.append({
            "lote": q,
            "ordenes_al_anio": demanda_anual / q,
            "costo_total": c,
            "sobrecosto": (c - costo_t) / costo_t,
        })

    opciones.sort(key=lambda o: o["costo_total"])
    elegido = opciones[0]

    if elegido["sobrecosto"] <= umbral_alerta:
        lectura = "el redondeo casi no cuesta, comprala en el multiplo y no lo discutas"
        causa = None
    else:
        lectura = "el redondeo si cuesta, esto ya no se arregla desde planeacion"
        if minimo and elegido["lote"] >= minimo and elegido["lote"] > q_t:
            causa = "el minimo de compra del proveedor te esta empujando arriba del optimo"
        elif maximo and elegido["lote"] < q_t:
            causa = "el tope de espacio o caducidad te esta empujando abajo del optimo"
        else:
            causa = "el multiplo de compra es grande frente a tu lote optimo"

    return {
        "eoq_teorico": q_t,
        "costo_teorico": costo_t,
        "opciones": opciones,
        "elegido": elegido,
        "lectura": lectura,
        "causa": causa,
    }


# --------------------------------------------------------------------------
# Salida legible
# --------------------------------------------------------------------------

def reporte(r, unidad="pz"):
    out = []
    out.append("EOQ teorico          {:>12,.0f} {}".format(r["eoq_teorico"], unidad))
    out.append("costo total anual    {:>12,.0f}".format(r["costo_teorico"]))
    out.append("")
    out.append("lotes que si puedes comprar")
    out.append("  {:>12}  {:>10}  {:>14}  {:>11}".format(
        "lote", "ordenes/anio", "costo total", "sobrecosto"))
    for o in r["opciones"]:
        marca = "<-" if o is r["elegido"] else "  "
        out.append("  {:>12,.0f}  {:>10.1f}  {:>14,.0f}  {:>10.1%} {}".format(
            o["lote"], o["ordenes_al_anio"], o["costo_total"], o["sobrecosto"], marca))
    out.append("")
    out.append(r["lectura"])
    if r["causa"]:
        out.append("causa: " + r["causa"])
    return "\n".join(out)


# --------------------------------------------------------------------------
# Ejemplos
# --------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 66)
    print("CASO 1  el redondeo sale gratis")
    print("=" * 66)
    print("compras por tarima de 1,200 pz y el EOQ no cae en tarima cerrada\n")
    r1 = evaluar(demanda_anual=48000, costo_por_orden=3500,
                 costo_mantener_unidad_anual=18, multiplo=1200)
    print(reporte(r1))

    print()
    print("=" * 66)
    print("CASO 2  el minimo del proveedor te empuja lejos del optimo")
    print("=" * 66)
    print("mismo material, pero el proveedor no surte menos de 12,000 pz\n")
    r2 = evaluar(demanda_anual=48000, costo_por_orden=3500,
                 costo_mantener_unidad_anual=18, multiplo=1200, minimo=12000)
    print(reporte(r2))

    print()
    print("=" * 66)
    print("CASO 3  el almacen te topa por espacio")
    print("=" * 66)
    print("no caben mas de 2,400 pz de este material\n")
    r3 = evaluar(demanda_anual=120000, costo_por_orden=4200,
                 costo_mantener_unidad_anual=9, multiplo=600, maximo=2400)
    print(reporte(r3))
