# EpiRed · Taller 2 y parcial del corte 2

Esta es una **actualización del proyecto que ya teníamos en `EpiRed-main.zip`**. Los cuatro retos están en el mismo `epired_taller2.py`. Solo añadimos un `main.py` para manejarlos desde un menú, las pruebas y los guiones de exposición.

EpiRed representa municipios y conexiones de traslado en un proyecto académico de salud. Todos los datos son ficticios: no representan una red hospitalaria real ni recomendaciones sanitarias.

## 1. Qué teníamos y qué cambiamos

En `EpiRed-Grafo`, el Taller 1 tenía `grafo.py`, `datos.py`, `main.py`, `interfaz.py` y pruebas. Usaba una matriz con cero para ausencia, BFS/DFS, componentes, Dijkstra y una interfaz Tkinter. En el Taller 2, `epired_taller2.py` ya tenía `Grafo`, `Dijkstra`, `RutaDijkstra`, `FloydWarshall` y `RutaFloyd`.

**Conservamos la base del Taller 2:** `inf` significa ausencia y cero en la diagonal. Así no confundimos una conexión de tiempo cero con una conexión inexistente. Cargamos las 13 conexiones originales con `Union`. Reutilizamos sus métodos de Dijkstra y Floyd, añadiendo una comprobación de desbordamiento al sumar pesos. Para el reto 2 adaptamos la idea de BFS y componentes del Taller 1.

| Reto | Lo añadido | Expone |
|---|---|---|
| 1 · 30 % | Capacidades y ruta max-min | Juan, más integración |
| 2 · 30 % | Retiro automático de cada municipio | Sofía |
| 3 · 25 % | Ruta primaria y respaldo sin repetir enlaces | Vanessa |
| 4 · 15 % | Subsidios dirigidos y diagnóstico de ciclos negativos | Vanessa |

El Taller 1 y las versiones de árboles se mantienen. `Informe_Taller2_EpiRed.docx` se conserva como informe histórico; para este parcial se estudian este README y los guiones de `exposiciones/`.

## 2. Ejecutar y usar el menú

Necesitas **Python 3.10 o superior**. No hay paquetes que instalar. En VS Code abre `EpiRed/EpiRed_Taller2` y selecciona Terminal → Nueva terminal. Desde esa carpeta:

```powershell
python main.py
python main.py --demo
python -m unittest discover -s tests -v
```

En Windows también sirve `py -3` en lugar de `python`. En otros sistemas puede llamarse `python3`. Los Word ya están hechos; no necesitas instalar nada para generarlos. `python epired_taller2.py` también abre el menú, pero usamos `main.py` para exponer.

| Opción | Qué hace |
|---|---|
| 1 | Mayor capacidad; pide origen y destino |
| 2 | Prueba la falla de todos los municipios |
| 3 | Ruta con respaldo; pide origen y destino |
| 4 | Muestra los dos escenarios de subsidios |
| 5 | Ejecuta todos los ejemplos |
| 6 | Consulta IDs, nombres y reportes |
| 7 | Compara la red actual con su estado original |
| 0 | Sale |

Al terminar una consulta vuelve al menú. Acepta IDs en minúsculas. Si hay un error de entrada, muestra un mensaje. `--demo` funciona sin interacción e imprime primero la ficha de dominio.

## 3. Datos que usamos

A Medellín; B Bello; C Itagüí; D Envigado; E Sabaneta; F Caldas; G Copacabana; H Girardota; I Barbosa; J Rionegro.

| Conexión en ambos sentidos | Minutos originales | Capacidad nueva, unidades de suministros por viaje |
|---|---:|---:|
| A-B | 20 | 45 |
| A-C | 15 | 20 |
| A-D | 30 | 70 |
| B-C | 30 | 30 |
| C-D | 10 | 25 |
| D-E | 12 | 60 |
| E-F | 20 | 55 |
| C-F | 35 | 15 |
| A-G | 35 | 40 |
| B-G | 20 | 35 |
| G-H | 15 | 30 |
| H-I | 20 | 25 |
| G-J | 40 | 20 |

Las capacidades son valores ficticios añadidos para comparar dos criterios: A-D-E-F puede transportar más aunque tarde más. No se obtienen de los minutos. `Grafo.matriz` guarda tiempos; `Grafo.capacidades` guarda capacidad. `Union` valida ambos antes de escribir.

| Información | De dónde viene | Uso |
|---|---|---|
| Municipios, conexiones y minutos | Talleres 1 y 2 | Red principal |
| Confirmados, recuperados y fallecidos | `REPORTES` del Taller 1 | Consulta; activos = confirmados − recuperados − fallecidos |
| COVID-19 y corte simulado | Taller 1 | Contexto; no es una medida real de riesgo |
| Capacidades | Añadidas al parcial | Reto 1 |
| Costos de 10 UM y bonos de 15/45 UM | Añadidos al parcial | Reto 4; nunca son minutos |

## 4. Reto 1 explicado fácil

**Función en `epired_taller2.py`:** `RutaMayorCapacidad(origen, destino, grafo=None)`. Devuelve `(ruta, cuello_de_botella)`; sin tercer argumento usa EpiRed.

Primero ponemos capacidad infinita en el origen y cero en los demás. Elegimos el pendiente con mayor capacidad conocida. Para llegar a un vecino, tomamos el mínimo entre la capacidad que llegaba y la del enlace nuevo. Si mejora, guardamos el valor y el predecesor. Al terminar reconstruimos la ruta.

Extracto real comentado:

```python
candidato = min(mejores[actual], capacidad)  # Límite de la ruta extendida.
if not visitados[vecino] and candidato > mejores[vecino]:
    mejores[vecino] = candidato  # Guardar una capacidad mejor.
    anteriores[vecino] = actual  # Recordar por dónde llegamos.
```

**Opción 1, A y F:** A-D-E-F, Medellín → Envigado → Sabaneta → Caldas. `min(70,60,55)=55` unidades por viaje. La más rápida es A-C-F, Medellín → Itagüí → Caldas: 50 minutos y capacidad 15. La de capacidad 55 tarda 62 minutos. Son resultados ejecutados y comprobados.

Sin ruta: `([], 0)`. Mismo origen/destino: `([origen], inf)`, convención sin traslado ni aristas; no significa capacidad física infinita. IDs inexistentes o capacidades no positivas se rechazan. Los empates siguen el orden de los IDs y solo se actualiza ante una mejora estricta; no se promete desempatar por tiempo.

**Para estudiar:** ¿Por qué cambiar Dijkstra? Porque ahora maximizamos un mínimo, no minimizamos una suma. ¿Se suman capacidades? No: el enlace menor limita todo. ¿De dónde salen? De la tabla ficticia nueva `CAPACIDADES`.

## 5. Reto 2 explicado fácil

**Funciones en `epired_taller2.py`:** `componentes` y `DetectarPuntosCriticosDeFalla(grafo)`.

BFS usa una cola y visitados para encontrar un grupo conectado. Si quedan nodos pendientes, inicia otra búsqueda. Primero contamos los grupos originales. Después repetimos excluyendo cada ID: no lo usamos como inicio ni como vecino, sin borrar nada.

```python
grupos = componentes(grafo, excluido=id)  # Buscar sin ese municipio.
aislados = [g[0] for g in grupos if len(g) == 1]  # Grupos de un nodo.
es_critico = len(grupos) > len(inicial)  # Comparar con el estado inicial.
```

Devuelve `criticos`, `componentes_iniciales` y `ensayos` con los grupos, aislados y nuevos aislados de cada retiro.

**Opción 2:** inicialmente hay una componente. Sin G, Copacabana, quedan **ABCDEF | HI | J**: Rionegro aislado. Sin H, Girardota, quedan **ABCDEFGJ | I**: Barbosa aislado. El resultado calculado es **G y H**.

Funciona con una red ya desconectada. Vacío, un nodo y aislados no producen falsos críticos. En dos nodos unidos, retirar uno deja un nuevo aislado pero no aumenta componentes: se informa sin marcar crítico. Se exige grafo no dirigido. La opción 7 comprueba que el original no cambió.

**Para estudiar:** ¿Por qué BFS? Interesa conectividad, no tiempo. ¿Por qué contar antes? La red podría estar partida desde el inicio. ¿Cómo restauramos? No hace falta: solo se ignora un ID al recorrer.

## 6. Reto 3 explicado fácil

**Función en `epired_taller2.py`:** `GenerarRutaConRespaldo(origen, destino, grafo=None)`.

Calcula la primaria con `Grafo.Dijkstra` y `RutaDijkstra`. Después:

```python
copia = grafo.copia()  # Filas independientes del original.
for a, b in zip(primaria, primaria[1:]):
    copia.BorrarArco(a, b)  # Retirar solo sus enlaces, en ambos sentidos.
segunda = copia.Dijkstra(origen)
respaldo = copia.RutaDijkstra(segunda, destino)
```

Devuelve ambas rutas, `costo_primario`, `costo_respaldo`, `porcentaje` y `alerta`. Se permite compartir municipios, pero ninguna arista, ni en sentido contrario.

**Opción 3, A y F:** primaria A-C-F, Medellín → Itagüí → Caldas, **50 min**. Respaldo A-D-E-F, pasando por Envigado y Sabaneta, **62 min**. `(62-50)/50*100 = 24 %`.

**Opción 3, A e I:** primaria A-G-H-I hasta Barbosa, 70 min; sin respaldo imprime exactamente:

```text
Red no redundante entre origen y destino
```

Si tampoco hay primaria se devuelve la misma alerta. Una ruta inexistente cuesta `inf`. Con costo primario cero, el porcentaje es `None`: no dividimos por cero. Con origen=destino, ambas rutas son `[origen]` y cuestan cero, sin traslado. Se rechazan IDs inválidos y redes dirigidas.

Seguimos la segunda ejecución tras retirar la primaria que exige el parcial. **No se optimiza globalmente el par de rutas disjuntas.** Las pruebas verifican que el original sigue igual con y sin respaldo.

**Para estudiar:** ¿Se borran nodos? No, solo aristas en una copia. ¿Pueden compartir un nodo interno? Sí. ¿Qué es el 24 %? Los 12 minutos extra respecto a los 50 originales.

## 7. Reto 4 explicado fácil

**En `epired_taller2.py`:** `crear_escenario_costos`, `Grafo.FloydWarshall` y `DetectarAnomaliaDeCicloNegativo(matriz_distancias, ids=None)`.

Creamos una copia económica dirigida: cada conexión original aporta dos arcos de **10 unidades monetarias ficticias (UM)**. Solo A→B recibe bono; B→A conserva +10. Así no ponemos automáticamente una arista negativa en ambos sentidos. Los municipios y conexiones sirven de referencia, pero los pesos ya son costos, no minutos.

- Control: bono de 15 UM; A→B=−5. Toda vuelta requiere al menos otro arco de +10: no hay ciclo negativo.
- Anomalía: bono de 45 UM; A→B=−35. A→B→C→A, Medellín → Bello → Itagüí → Medellín, suma **−15 UM**. A→B→A también es negativo, −25 UM.

Floyd prueba cada nodo como intermediario entre cada par y actualiza la matriz. Luego inspeccionamos **su matriz final**:

```python
diagnosticos = [ids[i] for i in range(n) if matriz_distancias[i][i] < 0]
return {"hay_anomalia": bool(diagnosticos), "ids_diagnosticos": diagnosticos}
```

La primera línea encuentra diagonales negativas; la segunda devuelve el booleano y los IDs. **Opción 4 comprobada:** control `False`, diagonal cero; anomalía `True`, IDs **A a J**, y alerta de inconsistencia operativa o beneficio infinito.

Esos IDs son evidencia de recorridos cerrados negativos detectados, **no necesariamente miembros del ciclo simple exacto**. La magnitud de las distancias finales ya no se interpreta como un mínimo finito. `RutaFloyd` bloquea reconstrucciones con ciclo negativo y Dijkstra rechaza pesos negativos. Floyd termina porque sus bucles son acotados.

La función valida matriz cuadrada numérica y correspondencia de IDs. Admite vacío, un nodo y +inf para ausencia; rechaza NaN, −inf y datos inválidos. Sin IDs asigna A, B, etc., hasta 26 filas; para otros nombres se pasan los IDs de Floyd. La matriz de minutos no se modifica.

**Para estudiar:** ¿Son tiempos negativos? No, dinero simulado. ¿Una arista negativa basta? No: la vuelta completa debe ser negativa. ¿Por qué la diagonal? Representa volver al mismo municipio.

## 8. Complejidad sin enredos

V es el número de municipios. Una matriz revisa V posiciones por fila. El grafo ya ocupa O(V²).

| Operación | Tiempo | Memoria adicional | Por qué |
|---|---|---|---|
| Dijkstra y reto 1 | O(V²) | O(V) | Selección lineal y revisión de filas |
| Un BFS completo | O(V²) | O(V) | Visita nodos y revisa sus filas |
| Reto 2 | O(V³) | O(V²) | V ensayos; guardamos todos sus grupos |
| Reto 3 | O(V²) | O(V²) | Dos Dijkstra y copia de las matrices |
| Reto 4 completo | O(V³) | O(V²) | Los tres bucles de Floyd |
| Auditoría de matriz final | O(V²) | O(V) | Validar toda la matriz; la diagonal sola es O(V) |

Dijkstra suma tiempos, la variante max-min compara capacidades, BFS determina conectividad y Floyd compara costos entre todos los pares. No hacen la misma pregunta.

## 9. Pruebas y orden de exposición

`python -m unittest discover -s tests -v` ejecuta **36 pruebas**. Revisan los ejemplos, errores, grafos pequeños, desconexión, costo cero, ciclos negativos, desbordamiento y estado intacto. Comparan Dijkstra/Floyd para los 100 pares y comprueban que el respaldo no repita ninguna arista. Las pruebas están aparte para no complicar el código que mostramos.

`resultados_pruebas.txt` contiene la salida real y `resultados_demo.txt` la demo ejecutada.

Introducción grupal: “Buenos días. Somos Juan, Sofía y Vanessa. Continuamos EpiRed con los mismos municipios y presentamos los cuatro retos del parcial. Todos los datos son ficticios”.

1. **Juan:** opción 6 y luego 1 con A,F. Explica el cuello de botella de 55.
2. **Sofía:** opción 2 y luego 7. Explica G y H y que la red sigue igual.
3. **Vanessa:** opción 3 con A,F; luego 3 con A,I; opción 4 y 7. Cierra con las pruebas.

Cada Word indica qué decir, qué código mostrar y qué hacer. Las copias Markdown tienen el mismo contenido. Todos deben conocer este resumen, aunque cada uno exponga su parte.

## 10. Archivos y GitHub

| Archivo | Para qué sirve |
|---|---|
| `epired_taller2.py` | Archivo existente actualizado: datos, Grafo y cuatro retos |
| `main.py` | Ficha, menú y demostraciones |
| `tests/test_reto1.py` a `test_reto4.py` | Pruebas de cada reto |
| `tests/test_integracion.py` | Datos, algoritmos base, menú y estado |
| `exposiciones/Juan_Reto1_e_Integracion.docx` y `.md` | Guion de Juan |
| `exposiciones/Sofia_Reto2.docx` y `.md` | Guion de Sofía |
| `exposiciones/Vanessa_Retos3_y_4.docx` y `.md` | Guion de Vanessa |
| `resultados_pruebas.txt`, `resultados_demo.txt` | Evidencia real |
| `Informe_Taller2_EpiRed.docx` | Informe anterior conservado |
| `.gitignore` | Excluye cachés y entornos |
| `README.md` | Esta guía |

**Descomprime el ZIP antes de subirlo.** Contiene el proyecto `EpiRed-main/` completo actualizado. No subas solo el ZIP: GitHub debe mostrar los archivos de código.

Desde la carpeta que contiene la entrega, en PowerShell:

```powershell
Expand-Archive -LiteralPath .\EpiRed_Actualizado_Corte2.zip -DestinationPath .\revision
Set-Location .\revision\EpiRed-main\EpiRed\EpiRed_Taller2
python main.py --demo
python -m unittest discover -s tests -v
```

En el mismo repositorio GitHub existente, copia el contenido actualizado de `EpiRed_Taller2` sobre esa carpeta y el README general actualizado sobre `EpiRed/README.md`. No reemplaces la carpeta `.git` ni borres los otros talleres. Desde la raíz del repositorio:

```powershell
git status --short
git add -- EpiRed/EpiRed_Taller2 EpiRed/README.md
git diff --cached --stat
git commit -m "Completa los cuatro retos del parcial EpiRed"
git push
```

Si la raíz ya es la carpeta `EpiRed`, omite `EpiRed/` en esas rutas. Revisa que no haya cambios ajenos preparados antes del commit. El push requiere tu cuenta y el remoto ya configurado; no se publica automáticamente.


## Grafo interactivo añadido

Ejecuta `python main.py` y elige **8**, o ejecuta `python grafo_interactivo.py`. Puedes mover municipios, consultar sus reportes, alternar tiempos/capacidades y resaltar rutas o puntos críticos. Cierra la ventana para regresar al menú. Usa Tkinter (incluido normalmente con Python en Windows), sin internet ni pip. Consulta [GRAFO_INTERACTIVO.md](GRAFO_INTERACTIVO.md) para ver los pasos y ejemplos de exposición.
