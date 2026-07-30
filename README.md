# lote-ejecutable

El EOQ te da un número que casi nunca se puede comprar. El proveedor vende por
tarima, el camión cierra en cierto número de tarimas y el almacén no recibe
fracciones.

Este módulo calcula el EOQ, lo baja al lote que sí puedes comprar y te dice
**cuánto te costó ese redondeo**.

Esa última parte es la que sirve. Cerca del óptimo la curva de costo total es
plana, así que redondear a la tarima casi siempre sale gratis. Cuando no sale
gratis, la restricción ya no es de planeación, es de negociación con el
proveedor o de espacio en el almacén.

## Correr

    python3 lote_ejecutable.py

Trae tres casos de ejemplo:

| Caso | Restricción | Sobrecosto |
|---|---|---|
| 1 | tarima de 1,200 pz | 0.6% |
| 2 | el proveedor no surte menos de 12,000 pz | 56.9% |
| 3 | el almacén no recibe más de 2,400 pz | 131.8% |

El primero es redondeo y no vale la pena discutirlo. Los otros dos ya no se
arreglan desde planeación.

## Usarlo con tus números

```python
from lote_ejecutable import evaluar, reporte

r = evaluar(
    demanda_anual=48000,
    costo_por_orden=3500,
    costo_mantener_unidad_anual=18,   # costo de mantener UNA pieza un año
    multiplo=1200,                    # tarima, caja, unidad indivisible
    minimo=None,                      # mínimo de compra del proveedor
    maximo=None,                      # tope por espacio o caducidad
)
print(reporte(r))
```

Devuelve el EOQ teórico, los lotes que sí puedes comprar alrededor de él, el
sobrecosto de cada uno y cuál de las tres restricciones te está empujando lejos
del óptimo.

## Lo que necesitas antes de correrlo

Nada de esto sirve si el costo por orden y el costo de mantener son inventados.

El costo por orden incluye el tiempo de quien la levanta, la revisión y la
recepción. El costo de mantener incluye espacio, merma, seguro y el dinero
parado.

Python 3.8+. Sin dependencias.
