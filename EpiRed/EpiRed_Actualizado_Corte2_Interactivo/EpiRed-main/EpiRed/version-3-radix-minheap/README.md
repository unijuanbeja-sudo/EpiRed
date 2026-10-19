# EpiRed - Versión 3: Radix Tree y Min-Heap

Esta versión de EpiRed continúa lo que ya se había hecho en las versiones anteriores.

Antes se trabajó con:

- Árbol n-ario para organizar departamentos, municipios, centros de salud y enfermedades.
- Árbol B+ para indexar casos epidemiológicos.

En esta nueva versión se agregan dos estructuras nuevas:

- **Radix Tree**, para hacer búsquedas por prefijo y autocompletado.
- **Min-Heap**, para manejar alertas epidemiológicas según prioridad.

La idea es que EpiRed no solo guarde información, sino que también pueda encontrar datos más rápido y atender primero las alertas más importantes.

---

## ¿Qué se agregó?

### 1. Radix Tree

El Radix Tree se usa para buscar palabras escribiendo solo una parte del nombre.

Por ejemplo:

```text
med
```

puede encontrar:

```text
Medellin
```

También:

```text
den
```

puede encontrar:

```text
Dengue
```

Y:

```text
hos
```

puede mostrar varios hospitales.

En esta versión se cargan datos como:

```text
Medellin
Bogota
Bello
Cali

Hospital Central
Clinica Norte
Hospital San Jose
Hospital Universitario
Hospital Marco Fidel Suarez

Dengue
Tuberculosis
Malaria
Sarampion
COVID-19
```

---

## ¿Cómo funciona el Radix Tree?

El Radix Tree guarda partes de palabras en lugar de guardar siempre letra por letra.

Por ejemplo, si se guardan:

```text
Dengue
Dental
```

se puede aprovechar la parte que tienen en común:

```text
Den
├── gue
└── tal
```

Eso hace que los caminos repetidos se puedan compartir.

La clase principal comienza así:

```python
class NodoRadix:
    def __init__(self):
        self.hijos = {}
        self.es_fin = False
```

`hijos` guarda las diferentes ramas que salen del nodo.

`es_fin` indica si en ese punto termina una palabra registrada.

La búsqueda por prefijo se hace con:

```python
radix.autocompletar(prefijo)
```

Por ejemplo:

```python
radix.autocompletar("den")
```

devuelve:

```text
dengue
```

---

## 2. Min-Heap

El Min-Heap se usa para manejar alertas epidemiológicas.

Cada alerta tiene una prioridad:

```text
1 = Critica
2 = Alta
3 = Media
4 = Baja
```

Mientras menor sea el número, más urgente es la alerta.

Ejemplo:

```text
Prioridad 1
Brote critico de dengue
```

debe atenderse antes que:

```text
Prioridad 3
Seguimiento de casos de malaria
```

---

## ¿Cómo funciona el Min-Heap?

El Min-Heap mantiene la alerta de mayor urgencia en la primera posición.

Se almacena internamente usando una lista.

Las posiciones se calculan con estas fórmulas:

```text
Hijo izquierdo = 2i + 1

Hijo derecho = 2i + 2

Padre = (i - 1) // 2
```

Por ejemplo:

```text
        indice 0
        /      \
   indice 1   indice 2
    /   \
   3     4
```

Cuando se inserta una nueva alerta:

```python
min_heap.insertar(alerta)
```

se agrega al final y puede ir subiendo hasta quedar en la posición correcta.

Esto se conoce como:

```text
swim
o
percolate up
```

Cuando se procesa la alerta más importante:

```python
min_heap.extraer_minimo()
```

sale la alerta que está en la raíz.

Después el árbol se reorganiza.

Esto se conoce como:

```text
sink
o
percolate down
```

---

# Ejemplo sencillo

Supongamos que se insertan estas prioridades:

```text
3
1
2
```

El Min-Heap las organiza para que arriba quede:

```text
1
```

Entonces al procesar una alerta:

```text
sale primero prioridad 1
```

Después:

```text
prioridad 2
```

y finalmente:

```text
prioridad 3
```

---

# Archivos principales

```text
version-3-radix-minheap/
├── estructuras/
│   ├── arbol_nario.py
│   ├── arbol_bplus.py
│   ├── radix_tree.py
│   └── min_heap.py
├── casos_epidemiologicos.py
├── main.py
└── README.md
```

### `radix_tree.py`

Contiene el Radix Tree.

Se encarga de:

- Insertar palabras.
- Buscar palabras.
- Autocompletar por prefijo.
- Mostrar la estructura.

### `min_heap.py`

Contiene el Min-Heap.

Se encarga de:

- Registrar alertas.
- Ordenarlas por prioridad.
- Consultar la siguiente alerta.
- Procesar la alerta más urgente.

### `main.py`

Une las dos estructuras y permite utilizarlas desde un menú.

---

# Parte del taller: Radix Tree

Para EpiRed se eligió usar el Radix Tree en:

```text
Municipios
Centros de salud
Enfermedades
```

porque son datos que un usuario puede buscar muchas veces escribiendo solo el comienzo del nombre.

Ejemplos:

```text
med → Medellin
den → Dengue
hos → Hospital Central, Hospital San Jose...
```

El taller también plantea analizar una colección de:

```text
50.000 cadenas
```

con una longitud promedio de:

```text
10 caracteres
```

Eso significa que, sin tener en cuenta coincidencias entre palabras, se podrían llegar a manejar aproximadamente:

```text
50.000 × 10 = 500.000 caracteres
```

La ventaja de un Radix Tree es que puede comprimir partes repetidas de las palabras y reducir la cantidad de nodos necesarios.

---

# Parte del taller: Min-Heap

Para EpiRed se eligió el Min-Heap para manejar:

```text
Alertas epidemiológicas
```

El objetivo es que una alerta crítica sea atendida antes que una alerta de menor urgencia.

Cada elemento del Heap puede entenderse como:

```text
Prioridad + información de la alerta
```

El taller plantea un tamaño de:

```text
8 bytes para la prioridad
8 bytes para el ID o referencia del dato
```

Total:

```text
16 bytes por elemento
```

---

# Manual de uso del programa

Para ejecutar EpiRed:

```bash
python main.py
```

Al iniciar aparece:

```text
==============================================
              MENU EPIRED
==============================================
1. Autocompletar municipio
2. Autocompletar centro de salud
3. Autocompletar enfermedad
4. Mostrar Radix Tree
5. Registrar alerta epidemiologica
6. Procesar alerta mas prioritaria
7. Mostrar Min-Heap
8. Ver siguiente alerta
9. Salir
```

---

## Opción 1 - Autocompletar municipio

Permite escribir solo el comienzo del municipio.

Ejemplo:

```text
Ingrese el inicio del municipio: med
```

Resultado:

```text
Medellin
```

También se puede probar:

```text
bo
```

para buscar:

```text
Bogota
```

---

## Opción 2 - Autocompletar centro de salud

Permite buscar centros de salud por prefijo.

Ejemplo:

```text
Ingrese el inicio del centro de salud: hos
```

Puede mostrar:

```text
Hospital Central
Hospital San Jose
Hospital Universitario
Hospital Marco Fidel Suarez
```

Otro ejemplo:

```text
cli
```

Resultado:

```text
Clinica Norte
```

---

## Opción 3 - Autocompletar enfermedad

Permite buscar enfermedades escribiendo solo una parte inicial.

Ejemplo:

```text
den
```

Resultado:

```text
Dengue
```

Otro ejemplo:

```text
tu
```

Resultado:

```text
Tuberculosis
```

Si no existe ninguna coincidencia:

```text
zzz
```

el programa muestra:

```text
No se encontraron coincidencias.
```

---

## Opción 4 - Mostrar Radix Tree

Muestra cómo quedaron organizadas internamente las palabras.

Esta opción sirve principalmente para observar la estructura.

Puede mostrar ramas como:

```text
└── medellin *
└── hospital
   └── central *
```

El símbolo:

```text
*
```

indica que en ese punto termina una palabra registrada.

---

## Opción 5 - Registrar alerta epidemiológica

Permite crear una nueva alerta.

Primero muestra:

```text
1 = Critica
2 = Alta
3 = Media
4 = Baja
```

Después solicita:

```text
Prioridad
Descripcion
Municipio
Enfermedad
```

Ejemplo:

```text
Prioridad: 1
Descripcion: Brote grave de sarampion
Municipio: Bogota
Enfermedad: Sarampion
```

La alerta se inserta en el Min-Heap automáticamente.

---

## Opción 6 - Procesar alerta más prioritaria

Extrae y procesa la alerta de mayor urgencia.

Ejemplo:

Si existen:

```text
Prioridad 3
Prioridad 1
Prioridad 2
```

esta opción procesará primero:

```text
Prioridad 1
```

Después el Min-Heap se reorganiza automáticamente.

---

## Opción 7 - Mostrar Min-Heap

Muestra las alertas tal como están guardadas dentro del arreglo del Heap.

Ejemplo:

```text
[0] Prioridad: 1
[1] Prioridad: 2
[2] Prioridad: 3
```

Lo más importante es que la posición:

```text
[0]
```

siempre debe contener una de las alertas con menor número de prioridad.

---

## Opción 8 - Ver siguiente alerta

Permite consultar cuál sería la próxima alerta a procesar sin eliminarla.

Por ejemplo:

```text
Siguiente alerta a procesar:

Prioridad: 1
Municipio: Medellin
Enfermedad: Dengue
```

Esta opción solo consulta la raíz del Min-Heap.

---

## Opción 9 - Salir

Finaliza el programa.

```text
Saliendo de EpiRed...
```

---

# Pruebas rápidas recomendadas

Para probar el Radix:

```text
med
den
hos
cli
zzz
```

Para probar el Min-Heap:

1. Mostrar el Heap.
2. Ver la siguiente alerta.
3. Registrar una alerta con prioridad 1.
4. Volver a ver la siguiente alerta.
5. Procesarla.
6. Ver qué alerta queda ahora primero.

---

# Resumen rápido para estudiar

### ¿Qué se agregó?

```text
Radix Tree
+
Min-Heap
```

### ¿Para qué sirve Radix?

```text
Autocompletado y búsqueda por prefijo.
```

### ¿Qué datos busca?

```text
Municipios
Centros de salud
Enfermedades
```

### ¿Para qué sirve Min-Heap?

```text
Procesar alertas según prioridad.
```

### ¿Qué sale primero?

```text
La prioridad con el número más pequeño.
```

### Fórmulas del Heap

```text
Izquierdo = 2i + 1
Derecho = 2i + 2
Padre = (i - 1) // 2
```

### Inserción en Heap

```text
Se agrega al final
→ sube si tiene mayor prioridad
→ swim
```

### Extracción en Heap

```text
Se elimina la raíz
→ se mueve el último elemento
→ baja hasta su posición correcta
→ sink
```

---

# Conclusión

Esta versión mejora EpiRed agregando dos funciones nuevas.

El **Radix Tree** permite encontrar municipios, centros de salud y enfermedades escribiendo solo el comienzo del nombre.

El **Min-Heap** permite organizar alertas epidemiológicas y procesar primero las más urgentes.

De esta manera, EpiRed continúa creciendo usando diferentes estructuras de datos para resolver problemas específicos del sistema.