# AVL Tree Movie Dataset

## Descripción

Este proyecto implementa un **árbol AVL**, una estructura de datos auto-balanceada que garantiza operaciones de búsqueda, inserción y eliminación eficientes en tiempo O(log n). El árbol AVL se utiliza aquí para gestionar un conjunto de datos de películas, almacenando información relevante sobre cada película y permitiendo realizar diversas operaciones sobre los datos.

## Funcionalidades

1. **Inserción de nodos:** Permite agregar nuevas películas al árbol AVL, donde cada nodo representa una película y almacena datos asociados a ella.
   
2. **Eliminación de nodos:** Facilita la eliminación de películas del árbol, manteniendo el balance del árbol para garantizar la eficiencia en las operaciones.

3. **Búsqueda de nodos:** Permite buscar una película específica en el árbol AVL utilizando su título.

4. **Búsqueda por criterios:** Permite encontrar películas que cumplan con ciertos criterios, como el año de estreno, porcentaje de ingresos nacionales en comparación con internacionales, y los ingresos internacionales.

5. **Recorrido por niveles:** Proporciona un recorrido por niveles del árbol AVL, mostrando los nombres de las películas.

6. **Información sobre nodos:** Obtiene y muestra información sobre nodos específicos, incluyendo:
   - Nivel del nodo
   - Factor de balanceo (equilibrio) del nodo
   - Padre del nodo
   - Abuelo del nodo
   - Tío del nodo

7. **Visualización:** Genera una representación visual del árbol AVL en formato PNG, mostrando la estructura del árbol y los datos asociados a cada nodo.

## Tecnologías Utilizadas

- **Python:** Lenguaje de programación principal para la implementación.
- **Pandas:** Para la carga y manejo de datos desde un archivo CSV.
- **Graphviz:** Para la visualización gráfica del árbol AVL.

## Instalación

Para ejecutar este proyecto, necesitas instalar las siguientes dependencias:

```bash
pip install pandas graphviz
