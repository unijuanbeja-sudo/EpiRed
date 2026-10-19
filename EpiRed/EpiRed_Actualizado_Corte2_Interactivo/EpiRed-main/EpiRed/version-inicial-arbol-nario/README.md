# EpiRed - Versión Inicial

EpiRed es un proyecto académico desarrollado en Python para representar información epidemiológica de Colombia utilizando estructuras de datos no lineales.

En esta primera versión se utiliza un **árbol n-ario** para organizar la información de forma jerárquica.

El sistema representa:

- Departamentos.
- Municipios.
- Centros de salud.
- Enfermedades.

Además, cuenta con un menú por consola que permite visualizar, buscar, agregar y eliminar información dentro del árbol.

---

# Objetivo del proyecto

El objetivo de EpiRed es aplicar conceptos de estructuras de datos no lineales a un problema relacionado con salud y epidemiología.

Para representar la información se utiliza un árbol n-ario, ya que permite organizar datos en diferentes niveles jerárquicos.

La estructura general del sistema es:

```text
EpiRed Colombia
├── Departamento
│   ├── Municipio
│   │   ├── Centro de salud
│   │   │   ├── Enfermedad
│   │   │   └── Enfermedad
```

Un ejemplo más completo sería:

```text
EpiRed Colombia
├── Antioquia
│   ├── Medellín
│   │   ├── Hospital Central
│   │   │   ├── Dengue
│   │   │   └── Tuberculosis
│   │   └── Clínica Norte
│   │       └── Sarampión
│   │
│   └── Bello
│       └── Hospital Marco Fidel Suárez
│           └── Dengue
│
├── Cundinamarca
│   └── Bogotá
│       └── Hospital San José
│           ├── Tuberculosis
│           └── COVID-19
│
└── Valle del Cauca
    └── Cali
        └── Hospital Universitario
            ├── Dengue
            └── Malaria
```

---

# Estructura del proyecto

El proyecto está organizado de la siguiente manera:

```text
EPIRED/
│
├── estructuras/
│   └── arbol_nario.py
│
├── main.py
└── README.md
```

## Archivo `main.py`

Es el archivo principal del programa.

Contiene:

- La creación inicial del árbol.
- Los departamentos.
- Los municipios.
- Los centros de salud.
- Las enfermedades.
- El menú principal.
- La interacción con el usuario.

## Archivo `estructuras/arbol_nario.py`

Contiene la implementación de la estructura de datos utilizada.

Aquí se encuentran:

- La clase `Nodo`.
- La clase `ArbolNario`.
- La búsqueda de nodos.
- La inserción de nodos.
- La eliminación de nodos.
- La visualización del árbol.

---

# ¿Qué es un árbol n-ario?

Un árbol n-ario es una estructura de datos jerárquica donde cada nodo puede tener varios hijos.

A diferencia de un árbol binario, en el que cada nodo puede tener como máximo dos hijos, un árbol n-ario puede tener una cantidad variable de hijos.

Esto es útil para EpiRed porque, por ejemplo, un departamento puede tener varios municipios:

```text
Antioquia
├── Medellín
├── Bello
└── Envigado
```

De la misma forma, un municipio puede tener varios centros de salud y cada centro puede tener varias enfermedades.

---

# Funcionamiento del código

## Clase `Nodo`

La estructura comienza con la clase `Nodo`.

```python
class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.hijos = []
```

Cada nodo tiene dos elementos principales:

```python
self.nombre
```

y

```python
self.hijos
```

### `self.nombre`

Guarda el nombre del nodo.

Por ejemplo:

```python
Nodo("Antioquia")
Nodo("Medellín")
Nodo("Hospital Central")
Nodo("Dengue")
```

Cada uno representa un elemento dentro de la estructura epidemiológica.

### `self.hijos`

```python
self.hijos = []
```

Es una lista donde se almacenan los nodos hijos.

Por ejemplo, si Antioquia tiene dos municipios:

```text
Antioquia
├── Medellín
└── Bello
```

entonces `Medellín` y `Bello` serían hijos del nodo `Antioquia`.

---

# Método `agregar_hijo`

Dentro de la clase `Nodo` se encuentra:

```python
def agregar_hijo(self, nodo):
    self.hijos.append(nodo)
```

Este método permite agregar un nuevo nodo a la lista de hijos.

Por ejemplo:

```python
antioquia.agregar_hijo(medellin)
```

Esto crea una relación padre-hijo:

```text
Antioquia
└── Medellín
```

---

# Clase `ArbolNario`

La clase `ArbolNario` representa la estructura completa.

```python
class ArbolNario:
    def __init__(self, nombre_raiz):
        self.raiz = Nodo(nombre_raiz)
```

Cuando se crea el árbol también se crea su nodo raíz.

En EpiRed se utiliza:

```python
arbol = ArbolNario("EpiRed Colombia")
```

Por lo tanto, el primer nodo del árbol es:

```text
EpiRed Colombia
```

Todos los demás nodos dependen directa o indirectamente de esta raíz.

---

# Método `agregar_nodo`

Para agregar información al árbol se utiliza:

```python
def agregar_nodo(self, nombre_padre, nombre_hijo):
    padre = self.buscar_nodo(self.raiz, nombre_padre)

    if padre is not None:
        padre.agregar_hijo(Nodo(nombre_hijo))
        return True

    return False
```

Este método recibe dos datos:

```text
nombre_padre
nombre_hijo
```

Primero busca el nodo padre.

Por ejemplo:

```python
arbol.agregar_nodo("Antioquia", "Medellín")
```

El programa busca el nodo:

```text
Antioquia
```

y luego agrega:

```text
Medellín
```

como hijo.

El resultado es:

```text
Antioquia
└── Medellín
```

Otro ejemplo:

```python
arbol.agregar_nodo("Medellín", "Hospital Central")
```

produce:

```text
Medellín
└── Hospital Central
```

Y posteriormente:

```python
arbol.agregar_nodo("Hospital Central", "Dengue")
```

produce:

```text
Hospital Central
└── Dengue
```

---

# Método `buscar_nodo`

La búsqueda se realiza utilizando recursividad.

```python
def buscar_nodo(self, nodo_actual, nombre):
    if nodo_actual.nombre.lower() == nombre.lower():
        return nodo_actual

    for hijo in nodo_actual.hijos:
        encontrado = self.buscar_nodo(hijo, nombre)

        if encontrado is not None:
            return encontrado

    return None
```

Primero se compara el nodo actual con el nombre que se está buscando.

```python
if nodo_actual.nombre.lower() == nombre.lower():
```

Si coincide, devuelve el nodo.

Si no coincide, se recorren sus hijos:

```python
for hijo in nodo_actual.hijos:
```

y la función vuelve a llamarse a sí misma:

```python
encontrado = self.buscar_nodo(hijo, nombre)
```

Esto se conoce como **recursividad**.

---

# ¿Qué es la recursividad?

La recursividad ocurre cuando una función se llama a sí misma para resolver un problema.

En este proyecto se utiliza porque el árbol puede tener muchos niveles.

Por ejemplo:

```text
EpiRed Colombia
↓
Antioquia
↓
Medellín
↓
Hospital Central
↓
Dengue
```

Para encontrar `Dengue`, el programa debe ir recorriendo los diferentes niveles.

La función revisa:

```text
EpiRed Colombia
```

Luego sus hijos.

Después los hijos de esos hijos.

Y continúa hasta encontrar el elemento buscado.

---

# Uso de `.lower()`

En la búsqueda se utiliza:

```python
nodo_actual.nombre.lower() == nombre.lower()
```

El método `.lower()` convierte temporalmente los textos a minúsculas.

Esto permite que las siguientes búsquedas sean equivalentes:

```text
Dengue
dengue
DENGUE
DeNgUe
```

Así el usuario no tiene que escribir exactamente las mismas mayúsculas y minúsculas que aparecen en el árbol.

---

# Método `mostrar_arbol`

Para visualizar la estructura completa se utiliza:

```python
def mostrar_arbol(self, nodo=None, nivel=0):
    if nodo is None:
        nodo = self.raiz

    print("   " * nivel + "└── " + nodo.nombre)

    for hijo in nodo.hijos:
        self.mostrar_arbol(hijo, nivel + 1)
```

Este método también utiliza recursividad.

El parámetro:

```python
nivel
```

indica la profundidad del nodo dentro del árbol.

Por ejemplo:

```text
nivel 0 → EpiRed Colombia
nivel 1 → Antioquia
nivel 2 → Medellín
nivel 3 → Hospital Central
nivel 4 → Dengue
```

La expresión:

```python
"   " * nivel
```

crea espacios antes del nombre para representar visualmente la jerarquía.

Por ejemplo:

```text
EpiRed Colombia
   Antioquia
      Medellín
         Hospital Central
            Dengue
```

Después se recorren todos los hijos:

```python
for hijo in nodo.hijos:
```

y se llama nuevamente al método:

```python
self.mostrar_arbol(hijo, nivel + 1)
```

Así se muestra todo el árbol.

---

# Método `eliminar_nodo`

Para eliminar información se utiliza:

```python
def eliminar_nodo(self, nodo_actual, nombre):
    for hijo in nodo_actual.hijos:
        if hijo.nombre.lower() == nombre.lower():
            nodo_actual.hijos.remove(hijo)
            return True

        eliminado = self.eliminar_nodo(hijo, nombre)

        if eliminado:
            return True

    return False
```

El método recorre los hijos del nodo actual.

Si encuentra el nombre buscado:

```python
if hijo.nombre.lower() == nombre.lower():
```

se ejecuta:

```python
nodo_actual.hijos.remove(hijo)
```

Esto elimina el nodo de la lista de hijos del padre.

Por ejemplo:

```text
Hospital Central
├── Dengue
└── Tuberculosis
```

Si se elimina:

```text
Tuberculosis
```

el resultado sería:

```text
Hospital Central
└── Dengue
```

---

# Eliminación de una rama completa

Es importante tener en cuenta que si se elimina un nodo que contiene hijos, también desaparecen todos los nodos que dependen de él.

Por ejemplo:

```text
Medellín
└── Hospital Central
    ├── Dengue
    └── Tuberculosis
```

Si se elimina:

```text
Hospital Central
```

también se eliminan:

```text
Dengue
Tuberculosis
```

porque pertenecen a esa rama del árbol.

---

# Construcción inicial del árbol

En `main.py` se comienza creando la raíz:

```python
arbol = ArbolNario("EpiRed Colombia")
```

Después se agregan los departamentos:

```python
arbol.agregar_nodo("EpiRed Colombia", "Antioquia")
arbol.agregar_nodo("EpiRed Colombia", "Cundinamarca")
arbol.agregar_nodo("EpiRed Colombia", "Valle del Cauca")
```

La estructura en ese punto sería:

```text
EpiRed Colombia
├── Antioquia
├── Cundinamarca
└── Valle del Cauca
```

---

# Agregar municipios

Posteriormente se agregan municipios.

```python
arbol.agregar_nodo("Antioquia", "Medellín")
arbol.agregar_nodo("Antioquia", "Bello")

arbol.agregar_nodo("Cundinamarca", "Bogotá")

arbol.agregar_nodo("Valle del Cauca", "Cali")
```

La estructura empieza a crecer:

```text
EpiRed Colombia
├── Antioquia
│   ├── Medellín
│   └── Bello
├── Cundinamarca
│   └── Bogotá
└── Valle del Cauca
    └── Cali
```

---

# Agregar centros de salud

Después se agregan diferentes centros de salud.

```python
arbol.agregar_nodo("Medellín", "Hospital Central")
arbol.agregar_nodo("Medellín", "Clínica Norte")

arbol.agregar_nodo("Bello", "Hospital Marco Fidel Suárez")

arbol.agregar_nodo("Bogotá", "Hospital San José")

arbol.agregar_nodo("Cali", "Hospital Universitario")
```

Cada centro queda asociado a su municipio.

---

# Agregar enfermedades

Finalmente se agregan enfermedades.

```python
arbol.agregar_nodo("Hospital Central", "Dengue")
arbol.agregar_nodo("Hospital Central", "Tuberculosis")

arbol.agregar_nodo("Clínica Norte", "Sarampión")

arbol.agregar_nodo("Hospital Marco Fidel Suárez", "Dengue")

arbol.agregar_nodo("Hospital San José", "Tuberculosis")
arbol.agregar_nodo("Hospital San José", "COVID-19")

arbol.agregar_nodo("Hospital Universitario", "Dengue")
arbol.agregar_nodo("Hospital Universitario", "Malaria")
```

De esta forma se obtiene una estructura epidemiológica completa.

---

# Menú principal

El programa cuenta con un menú por consola.

```text
==============================
            EPIRED
==============================

1. Mostrar estructura
2. Buscar enfermedad
3. Agregar enfermedad
4. Eliminar enfermedad
5. Salir
```

El menú se mantiene activo mediante:

```python
while True:
```

Esto significa que el programa continuará mostrando las opciones hasta que el usuario decida salir.

---

# Opción 1 - Mostrar estructura

Cuando el usuario selecciona:

```text
1
```

se ejecuta:

```python
arbol.mostrar_arbol()
```

Esto permite visualizar la estructura completa del árbol.

---

# Opción 2 - Buscar enfermedad

El usuario escribe el nombre:

```python
nombre = input("Ingrese el nombre de la enfermedad: ")
```

Después se realiza la búsqueda:

```python
resultado = arbol.buscar_nodo(arbol.raiz, nombre)
```

Si el nodo existe:

```python
if resultado is not None:
```

el programa muestra:

```text
Enfermedad encontrada
```

En caso contrario muestra que no fue encontrada.

---

# Opción 3 - Agregar enfermedad

Para agregar una enfermedad, primero se solicita el centro de salud.

```python
centro_salud = input("Ingrese el centro de salud: ")
```

Después se solicita la enfermedad:

```python
enfermedad = input("Ingrese la enfermedad: ")
```

Finalmente se agrega:

```python
agregado = arbol.agregar_nodo(centro_salud, enfermedad)
```

Si el centro de salud existe, la enfermedad se agrega como hijo.

Por ejemplo:

```text
Hospital Central
├── Dengue
├── Tuberculosis
└── Influenza
```

---

# Opción 4 - Eliminar enfermedad

El usuario escribe:

```python
enfermedad = input("Ingrese la enfermedad que desea eliminar: ")
```

Después se llama al método:

```python
eliminado = arbol.eliminar_nodo(arbol.raiz, enfermedad)
```

Si encuentra la enfermedad, se elimina.

Si no la encuentra, el programa informa al usuario.

---

# Opción 5 - Salir

Cuando el usuario selecciona:

```text
5
```

se ejecuta:

```python
break
```

`break` termina el ciclo:

```python
while True:
```

y finaliza el programa.

---

# Ejemplo de funcionamiento

Al ejecutar el programa aparece:

```text
==============================
            EPIRED
==============================
1. Mostrar estructura
2. Buscar enfermedad
3. Agregar enfermedad
4. Eliminar enfermedad
5. Salir

Seleccione una opción:
```

Si el usuario selecciona:

```text
2
```

y escribe:

```text
Dengue
```

el sistema puede mostrar:

```text
Enfermedad encontrada: Dengue
```

---

# Ejemplo de agregar una enfermedad

El usuario selecciona:

```text
3
```

Después escribe:

```text
Ingrese el centro de salud: Hospital Central
Ingrese la enfermedad: Influenza
```

El sistema muestra:

```text
Enfermedad agregada correctamente.
```

Ahora la estructura sería:

```text
Hospital Central
├── Dengue
├── Tuberculosis
└── Influenza
```

---

# Ejemplo de eliminar una enfermedad

El usuario selecciona:

```text
4
```

Después escribe:

```text
Influenza
```

El sistema elimina el nodo y vuelve a quedar:

```text
Hospital Central
├── Dengue
└── Tuberculosis
```

---

# Conceptos utilizados en el proyecto

Durante el desarrollo de esta versión se aplicaron los siguientes conceptos:

- Python.
- Programación orientada a objetos.
- Clases.
- Objetos.
- Métodos.
- Árboles n-arios.
- Nodos.
- Nodo raíz.
- Nodos padre.
- Nodos hijo.
- Listas.
- Recursividad.
- Recorrido de árboles.
- Búsqueda.
- Inserción.
- Eliminación.
- Ciclos.
- Condicionales.
- Entrada de datos por consola.

---

# Cómo ejecutar el proyecto

Se requiere tener instalado Python 3.

Desde una terminal ubicada dentro de la carpeta principal del proyecto ejecutar:

```bash
python main.py
```

También puede ejecutarse desde Visual Studio Code.

---

# Explicación rápida de los archivos

## `main.py`

Este archivo se encarga de:

- Crear la estructura inicial.
- Agregar departamentos.
- Agregar municipios.
- Agregar centros de salud.
- Agregar enfermedades.
- Mostrar el menú.
- Recibir las opciones del usuario.
- Llamar a los métodos del árbol.

## `arbol_nario.py`

Este archivo se encarga de la estructura de datos.

Aquí se encuentran las clases y métodos necesarios para:

- Crear nodos.
- Crear el árbol.
- Agregar hijos.
- Buscar nodos.
- Mostrar el árbol.
- Eliminar nodos.

---

# Limitaciones de esta versión

Esta es una versión inicial del proyecto, por lo tanto existen algunas limitaciones.

## Nombres repetidos

Puede existir una misma enfermedad en diferentes centros de salud.

Por ejemplo:

```text
Hospital Central
└── Dengue

Hospital Universitario
└── Dengue
```

Actualmente, la búsqueda devuelve la primera coincidencia que encuentra durante el recorrido.

Esto significa que:

```python
arbol.buscar_nodo(arbol.raiz, "Dengue")
```

no diferencia entre el Dengue registrado en un hospital y el registrado en otro.

---

# Limitación al eliminar enfermedades

La misma situación ocurre con la eliminación.

Si existen varios nodos llamados:

```text
Dengue
```

el método elimina la primera coincidencia que encuentra.

Esto podrá mejorarse posteriormente utilizando estructuras de datos y mecanismos de búsqueda más avanzados.

---

# Posibles mejoras futuras

A partir de esta versión se pueden incorporar nuevas funcionalidades y estructuras.

Entre ellas:

- Árbol Radix para búsquedas por prefijo.
- Autocompletado.
- Min-Heap para manejo de prioridades.
- Búsquedas más eficientes.
- Identificación de enfermedades según su centro de salud.
- Registro de casos.
- Prioridad según nivel de riesgo epidemiológico.
- Nuevos departamentos y municipios.
- Nuevos centros de salud.
- Mayor cantidad de enfermedades.
- Separación del proyecto en diferentes módulos.

---

# ¿Por qué esta versión es importante?

Esta versión funciona como base del proyecto.

Permite comprender primero conceptos como:

- Nodo.
- Árbol.
- Padre.
- Hijo.
- Raíz.
- Recorrido.
- Recursividad.
- Búsqueda.
- Inserción.
- Eliminación.

A partir de esta base se podrán implementar posteriormente estructuras más avanzadas sin perder el funcionamiento original del sistema.

---

# Resumen del funcionamiento

De forma general, EpiRed funciona así:

```text
Usuario
   ↓
Menú de EpiRed
   ↓
Selecciona una operación
   ↓
main.py
   ↓
ArbolNario
   ↓
Busca / agrega / elimina / muestra
   ↓
Resultado en consola
```

La estructura principal de información es:

```text
EpiRed Colombia
      ↓
Departamento
      ↓
Municipio
      ↓
Centro de salud
      ↓
Enfermedad
```

---

# Proyecto académico

EpiRed fue desarrollado como proyecto académico para aplicar conceptos de la asignatura de **Estructuras de Datos No Lineales** en un contexto relacionado con salud y epidemiología.

Esta versión corresponde a la implementación inicial del sistema utilizando un **árbol n-ario**.