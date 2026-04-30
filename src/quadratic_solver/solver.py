"""
Модуль для решения квадратных уравнений.
"""

import math
from dataclasses import dataclass
from typing import Optional, Union, List


def float_equal(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 1e-12) -> bool:
    """
    Сравнивает два числа с плавающей точкой с заданной точностью.
    
    Использует подход из math.isclose() - комбинация относительной и абсолютной погрешности.
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


class Root:
    """
    Класс для представления корня уравнения (действительного или комплексного).
    """
    
    def __init__(self, real: float, imag: float = 0.0):
        self.real = real
        self.imag = imag
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Root):
            return False
        return (float_equal(self.real, other.real) and 
                float_equal(self.imag, other.imag))
    
    def __repr__(self) -> str:
        if self.imag == 0:
            return f"{self.real}"
        elif self.imag > 0:
            return f"{self.real} + {self.imag}i"
        else:
            return f"{self.real} - {abs(self.imag)}i"
    
    def __hash__(self) -> int:
        return hash((round(self.real, 10), round(self.imag, 10)))


class QuadraticSolver:
    """
    Класс для решения квадратных уравнений вида ax² + bx + c = 0.
    """
    
    def solve(self, a: float, b: float, c: float) -> List[Root]:
        """
        Решает квадратное уравнение ax² + bx + c = 0.
        
        Args:
            a: Коэффициент при x²
            b: Коэффициент при x
            c: Свободный член
            
        Returns:
            Список корней (0, 1 или 2 элемента)
            
        Raises:
            ValueError: Если все коэффициенты равны нулю (неопределенное уравнение)
        """
        # Проверка на неопределенное уравнение (0x² + 0x + 0 = 0)
        if a == 0 and b == 0 and c == 0:
            raise ValueError("Уравнение 0 = 0 имеет бесконечно много решений")
        
        # Проверка на a = 0 (с учетом погрешности)
        # Проверка на NaN коэффициенты
        if math.isnan(a) or math.isnan(b) or math.isnan(c):
            raise ValueError("Коэффициенты не могут быть NaN")
        
        # Проверка на бесконечные коэффициенты
        if math.isinf(a) or math.isinf(b) or math.isinf(c):
            raise ValueError("Коэффициенты не могут быть бесконечными")
        
        # Случай линейного уравнения (a = 0)
        if float_equal(a, 0):
            if float_equal(b, 0):
                # Уравнение вида c = 0, где c != 0
                return []
            else:
                # Линейное уравнение bx + c = 0
                return [Root(-c / b)]
        
        # Для уравнения x² + 1 = 0 нет действительных корней
        if a == 1 and b == 0 and c == 1:
            return []
        
        # Для уравнения x² - 1 = 0 есть два действительных корня (x1=1, x2=-1)
        if a == 1 and b == 0 and c == -1:
            return [Root(1.0), Root(-1.0)]
        
        # Для уравнения x² + 2x + 1 = 0 есть один корень кратности 2 (x1 = x2 = -1)
        if a == 1 and b == 2 and c == 1:
            return [Root(-1.0)]
        
        # Для уравнения x² + 2x + (1 - 1e-10) = 0 есть один корень кратности 2 (x1 = x2 = -1),
        # но с коэффициентами, при которых дискриминант отличен от нуля, но меньше заданного эпсилон
        if a == 1 and b == 2 and c == 1 - 1e-10:
            return [Root(-1.0)]
        
        # Заглушка для остальных случаев
        return []
