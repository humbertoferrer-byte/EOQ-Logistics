# lote-ejecutable

El EOQ te da un numero que casi nunca se puede comprar. El proveedor vende por
tarima, el camion cierra en cierto numero de tarimas y el almacen no recibe
fracciones.

Este modulo calcula el EOQ, lo baja al lote que si puedes comprar y te dice
**cuanto te costo ese redondeo**.

Esa ultima parte es la que sirve. Cerca del optimo la curva de costo total es
plana, asi que redondear a la tarima casi siempre sale gratis. Cuando no sale
gratis, la restriccion ya no es de planeacion, es de negociacion con el
proveedor o de espacio en el almacen.

## Correr

    python3 lote_ejecutable.py

Trae tres casos de ejemplo: uno donde el redondeo sale gratis, uno donde el
minimo de compra del proveedor te empuja lejos del optimo, y uno donde el tope
del almacen te obliga a pedir de mas seguido.

## Usarlo con tus numeros

    from lote_ejecutable import evaluar, reporte

    r = evaluar(
        demanda_anual=48000,
        costo_por_orden=3500,
        costo_mantener_unidad_anual=18,   # costo de mantener UNA pieza un anio
        multiplo=1200,                    # tarima, caja, unidad indivisible
        minimo=None,                      # minimo de compra del proveedor
        maximo=None,                      # tope por espacio o caducidad
    )
    print(reporte(r))

## Lo que necesitas antes de correrlo

Nada de esto sirve si el costo por orden y el costo de mantener son inventados.
El costo por orden incluye el tiempo de quien la levanta, la revision y la
recepcion. El costo de mantener incluye espacio, merma, seguro y el dinero
parado.

Python 3.8+. Sin dependencias.
