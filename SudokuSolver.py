import numpy as np
import time

class SolucionadorSudoku:
    """
    Clase para resolver sudokus utilizando el método de backtracking con optimizaciones.
    """

    def __init__(self, sudoku):
        """
        Inicializa el solucionador con un sudoku dado.

        :param sudoku: Una matriz 9x9 que representa el sudoku. Los valores deben estar en el rango [0, 9],
                       donde 0 indica una casilla vacía.
        """
        self.bitmap = np.ones((9, 9, 9), dtype=bool)
        self.sudoku = np.zeros((9, 9), dtype=int)
        for i in range(9):
            for j in range(9):
                if sudoku[i][j] != 0:
                    self.colocar_numero(i, j, sudoku[i][j])

    def resolver(self):
        """
        Resuelve el sudoku utilizando el método de backtracking con optimizaciones.

        :return: Una matriz 9x9 que representa el sudoku resuelto, o None si no se encuentra solución.
        """
        start = time.time()
        self.backtrack()
        end = time.time()
        self.tiempo_resolucion = end - start
        return self.sudoku
    
    def backtrack(self):
        """
        Función recursiva para realizar el backtracking y resolver el sudoku.

        :return: Una matriz 9x9 que representa el sudoku resuelto, o None si no se encuentra solución.
        """
        if self.esta_resuelto():
            return self.sudoku
        i, j = self.celda_menos_opciones()
        for numero in range(1, 10):
            if self.puede_colocar_numero(i, j, numero):
                curr_bitmap = self.bitmap.copy()
                curr_sudoku = self.sudoku.copy()
                self.colocar_numero(i, j, numero)
                self.movimientos_triviales()
                if self.backtrack() is not None:
                    return self.sudoku
                self.bitmap = curr_bitmap
                self.sudoku = curr_sudoku
        return None
    
    def esta_resuelto(self):
        """
        Verifica si el sudoku ha sido resuelto.

        :return: True si el sudoku está resuelto, False en caso contrario.
        """
        return np.sum(self.sudoku == 0) == 0
    
    def celda_menos_opciones(self):
        """
        Encuentra las coordenadas de la celda vacía con la menor cantidad de opciones posibles.

        :return: Un par de índices (fila, columna) de la celda.
        """
        sumas_celdas = np.sum(self.bitmap, axis=2)
        sumas_celdas[sumas_celdas == 0] = 10
        indices_min_suma = np.unravel_index(np.argmin(sumas_celdas), sumas_celdas.shape)
        return indices_min_suma
    
    def puede_colocar_numero(self, i, j, numero):
        """
        Verifica si es posible colocar un número en una celda específica.

        :param i: Fila de la celda.
        :param j: Columna de la celda.
        :param numero: Número que se desea colocar.

        :return: True si es posible colocar el número, False en caso contrario.
        """
        return self.bitmap[i][j][numero-1]

    def colocar_numero(self, i, j, numero):
        """
        Coloca un número en una celda específica y actualiza el estado interno.

        :param i: Fila de la celda.
        :param j: Columna de la celda.
        :param numero: Número que se desea colocar.
        """
        self.sudoku[i][j] = numero
        self.bitmap[i][j] = np.zeros(9, dtype=bool)
        for k in range(9):
            self.bitmap[i][k][numero-1] = False
            self.bitmap[k][j][numero-1] = False
        for k in range(3):
            for l in range(3):
                self.bitmap[i//3*3+k][j//3*3+l][numero-1] = False
    
    def movimientos_triviales(self):
        """
        Realiza movimientos triviales de colocación de números basados en las celdas con una única opción posible.
        """
        cambiado = True
        while cambiado:
            cambiado = False
            for i in range(9):
                for j in range(9):
                    if self.es_celda_trivial(i, j):
                        cambiado = True
                        self.colocar_numero(i, j, np.argmax(self.bitmap[i][j]) + 1)

    def es_celda_trivial(self, i, j):
        """
        Verifica si una celda es trivial, es decir, no contiene un número y solo tiene una opción válida.

        :param i: Fila de la celda.
        :param j: Columna de la celda.

        :return: True si la celda es trivial, False en caso contrario.
        """
        return self.sudoku[i][j] == 0 and np.sum(self.bitmap[i][j]) == 1
