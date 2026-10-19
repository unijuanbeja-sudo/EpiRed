# EpiRed - Versión 2: Árbol B+

Esta versión de EpiRed parte de la versión inicial con árbol n-ario y agrega un **Árbol B+** para indexar registros epidemiológicos.

La idea es separar dos problemas:

```text
Árbol n-ario
→ organización jerárquica
→ departamentos, municipios, centros de salud y enfermedades

Árbol B+
→ indexación
→ búsqueda rápida de casos epidemiológicos
```

---

## 1. Estructura del proyecto

```text
version-2-arbol-bplus/
├── estructuras/
│   ├── arbol_nario.py
│   └── arbol_bplus.py
├── casos_epidemiologicos.py
├── main.py
└── README.md
```

---

# 2. Caso crítico del taller

La colección seleccionada como la de mayor volumen es:

```text
Registros de casos epidemiológicos
```

Esto tiene sentido porque EpiRed puede tener pocos tipos de enfermedades, pero miles o millones de reportes asociados a fechas, municipios y centros de salud.

Un registro contiene:

```text
ID
Fecha
Enfermedad
Municipio
Centro de salud
Cantidad
Nivel de riesgo
```

Ejemplo:

```text
CASO0001
2026-09-01
Dengue
Medellín
Hospital Central
18 casos
Riesgo alto
```

---

# 3. Clase CasoEpidemiologico

```python
class CasoEpidemiologico:
    def __init__(
        self,
        id_caso,
        fecha,
        enfermedad,
        municipio,
        centro_salud,
        cantidad,
        nivel_riesgo
    ):
        self.id_caso = id_caso
        self.fecha = fecha
        self.enfermedad = enfermedad
        self.municipio = municipio
        self.centro_salud = centro_salud
        self.cantidad = cantidad
        self.nivel_riesgo = nivel_riesgo
```

### ¿Qué hace?

Representa un registro epidemiológico completo.

Por ejemplo:

```python
CasoEpidemiologico(
    "CASO0001",
    "2026-09-01",
    "Dengue",
    "Medellin",
    "Hospital Central",
    18,
    "Alto"
)
```

---

# 4. Nodo del Árbol B+

```python
class NodoBPlus:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None
```

### ¿Qué representa cada parte?

```python
self.es_hoja
```

Indica si el nodo es una hoja.

```python
self.claves
```

Guarda las claves del índice, por ejemplo:

```text
CASO0001
CASO0002
CASO0003
```

```python
self.hijos
```

En nodos internos apunta a otros nodos.

En hojas guarda los registros asociados.

```python
self.siguiente
```

Conecta una hoja con la siguiente.

Ejemplo:

```text
[CASO0001 CASO0002]
          ↓
[CASO0003 CASO0004]
          ↓
[CASO0005 CASO0006]
```

Esta conexión hace que las consultas por rango sean eficientes.

---

# 5. Creación del Árbol B+

```python
class ArbolBPlus:
    def __init__(self, orden=4):
        self.orden = orden
        self.raiz = NodoBPlus(es_hoja=True)
```

El árbol inicia con una sola raíz.

Como todavía no hay más nodos, la raíz comienza siendo una hoja.

En la demostración usamos:

```python
orden=4
```

para poder ver las divisiones rápidamente.

---

# 6. Inserción

```python
def insertar(self, clave, registro):
    raiz = self.raiz

    if len(raiz.claves) >= self.orden - 1:
        nueva_raiz = NodoBPlus(es_hoja=False)
        nueva_raiz.hijos.append(raiz)

        self._dividir_hijo(nueva_raiz, 0)

        self.raiz = nueva_raiz
        self._insertar_no_lleno(
            nueva_raiz,
            clave,
            registro
        )
    else:
        self._insertar_no_lleno(
            raiz,
            clave,
            registro
        )
```

### ¿Qué hace?

Si el nodo tiene espacio, inserta normalmente.

Si está lleno:

```text
Nodo lleno
↓
Se divide
↓
Se crea una nueva estructura
↓
El árbol sigue balanceado
```

---

# 7. División de hojas

Una parte importante del código es:

```python
nuevo.siguiente = nodo.siguiente
nodo.siguiente = nuevo
```

Esto enlaza las hojas.

Ejemplo:

```text
Antes:

[1 2 3]

Después:

[1] → [2 3]
```

La clave del nuevo nodo también se usa para actualizar al nodo padre.

---

# 8. Búsqueda exacta

```python
def buscar(self, clave):
    nodo = self.raiz

    while not nodo.es_hoja:
        indice = 0

        while (
            indice < len(nodo.claves)
            and clave >= nodo.claves[indice]
        ):
            indice += 1

        nodo = nodo.hijos[indice]
```

### ¿Qué hace?

Empieza desde la raíz y va bajando por el hijo adecuado hasta llegar a una hoja.

Después compara las claves y devuelve el registro.

Ejemplo:

```text
Buscar CASO0005
```

Complejidad:

```text
O(log_m N)
```

---

# 9. Búsqueda por rango

```python
def buscar_rango(self, clave_inicio, clave_fin):
```

Primero busca la hoja donde comienza el rango.

Después usa:

```python
nodo = nodo.siguiente
```

para recorrer las hojas conectadas.

Ejemplo:

```text
CASO0003
hasta
CASO0006
```

Resultado:

```text
CASO0003
CASO0004
CASO0005
CASO0006
```

Complejidad indicada en el taller:

```text
O(log_m N + K/B)
```

---

# 10. Cálculo del orden m

Datos del taller:

```text
Bloque = 4096 bytes
Clave = 16 bytes
Puntero = 8 bytes
```

Fórmula:

```text
(m - 1)(16) + m(8) <= 4096
```

Desarrollo:

```text
16m - 16 + 8m <= 4096

24m - 16 <= 4096

24m <= 4112

m <= 171.33
```

Por lo tanto:

```text
m = 171
```

Un nodo interno puede tener como máximo:

```text
170 claves
171 punteros
```

Comprobación:

```text
170(16) + 171(8)

2720 + 1368

4088 bytes
```

Sí cabe en un bloque de 4096 bytes.

---

# 11. Capacidad con altura h = 3

Con orden:

```text
m = 171
```

la ramificación máxima por nivel es:

```text
Nivel 0:
1 nodo

Nivel 1:
171

Nivel 2:
171² = 29,241

Nivel 3:
171³ = 5,000,211
```

Esto muestra por qué los árboles B/B+ pueden manejar grandes cantidades de información manteniendo poca altura.

---

# 12. Taller 2 - Consultas del dominio

## Consulta A: búsqueda exacta

```text
Buscar un caso por ID
```

Ejemplo:

```text
CASO0005
```

Complejidad:

```text
O(log_m N)
```

---

## Consulta B: búsqueda por rango

```text
Obtener registros entre dos IDs
```

Ejemplo:

```text
CASO0003 → CASO0006
```

Complejidad:

```text
O(log_m N + K/B)
```

---

# 13. B vs. B+

| Característica | Árbol B | Árbol B+ |
|---|---|---|
| Búsqueda exacta | Buena | Buena |
| Consultas por rango | Buena | Mejor adaptada |
| Hojas enlazadas | No necesariamente | Sí |
| Recorrido secuencial | Menos directo | Directo |

## Veredicto

Para EpiRed se selecciona:

```text
Árbol B+
```

porque necesitamos tanto búsquedas exactas como consultas por rango.

Las hojas enlazadas permiten encontrar el inicio del rango y después recorrer los siguientes registros sin regresar a la raíz.

---

# 14. Orden real vs. orden de demostración

Según el cálculo del taller:

```text
Orden teórico = 171
```

En Python usamos:

```text
Orden = 4
```

solo para poder observar las divisiones con pocos registros.

Con orden 171 habría que insertar una gran cantidad de registros antes de visualizar una división.

---

# 15. Menú del programa

```text
1. Mostrar Arbol B+
2. Buscar caso por ID
3. Buscar casos por rango de ID
4. Mostrar todos los casos
5. Salir
```

### Opción 1

Muestra los nodos internos y las hojas.

### Opción 2

Demuestra la búsqueda exacta.

### Opción 3

Demuestra la búsqueda por rango.

### Opción 4

Muestra los datos de prueba.

---

# 16. Cómo ejecutar

Desde la carpeta:

```text
version-2-arbol-bplus
```

ejecutar:

```bash
python main.py
```

---

# 17. Qué debo saber para explicar esta versión

## ¿Por qué conservar el árbol n-ario?

Porque representa una jerarquía territorial.

```text
Departamento
→ Municipio
→ Centro de salud
→ Enfermedad
```

## ¿Para qué usamos B+?

Para indexar muchos registros epidemiológicos.

## ¿Cuál es el caso crítico?

```text
Casos epidemiológicos
```

## ¿Cuál es el orden calculado?

```text
m = 171
```

## ¿Por qué el código usa orden 4?

Para poder visualizar fácilmente las divisiones.

## ¿Qué ventaja tiene B+?

Las hojas están enlazadas, lo cual facilita las búsquedas por rango.

## ¿Consulta exacta?

```text
Buscar CASO0005
```

## ¿Consulta por rango?

```text
CASO0003 hasta CASO0006
```

## ¿Complejidades?

```text
Búsqueda exacta:
O(log_m N)

Rango:
O(log_m N + K/B)
```

---

# Conclusión

Esta versión amplía EpiRed incorporando un Árbol B+ para indexar casos epidemiológicos.

El árbol n-ario continúa siendo útil para la organización territorial, mientras que el B+ permite trabajar con grandes volúmenes de registros y realizar búsquedas exactas y por rango.

Según los parámetros del taller:

```text
m = 171
```

y se selecciona el Árbol B+ por su buen comportamiento en consultas por rango gracias al enlace entre sus hojas.