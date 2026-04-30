"""
Тесты для решателя квадратных уравнений.
"""

import pytest
from src.quadratic_solver.solver import QuadraticSolver, Root


def float_equal(a: float, b: float, rel_tol: float = 1e-9, abs_tol: float = 1e-12) -> bool:
    """
    Сравнивает два числа с плавающей точкой с заданной точностью.
    
    Использует подход из math.isclose() - комбинация относительной и абсолютной погрешности.
    """
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def roots_equal(actual: list, expected: list) -> bool:
    """
    Сравнивает два списка корней с учетом погрешности.
    """
    if len(actual) != len(expected):
        return False
    
    # Сортируем корни для сравнения (сначала по реальной части, затем по мнимой)
    sorted_actual = sorted(actual, key=lambda r: (r.real, r.imag))
    sorted_expected = sorted(expected, key=lambda r: (r.real, r.imag))
    
    return all(a == e for a, e in zip(sorted_actual, sorted_expected))


class TestQuadraticSolver:
    """
    Тесты для класса QuadraticSolver.
    """
    
    def setup_method(self):
        """
        Инициализация перед каждым тестом.
        """
        self.solver = QuadraticSolver()
    
    def test_no_real_roots_for_x_squared_plus_1(self):
        """
        Тест: для уравнения x² + 1 = 0 нет действительных корней.
        """
        result = self.solver.solve(1, 0, 1)
        assert len(result) == 0
    
    def test_solve_raises_value_error_when_all_coefficients_zero(self):
        """
        Тест: при всех нулевых коэффициентах должно выбрасываться ValueError.
        """
        with pytest.raises(ValueError, match="имеет бесконечно много решений"):
            self.solver.solve(0, 0, 0)
    
    def test_solve_raises_exception_when_a_is_zero(self):
        """
        Тест: коэффициент a не может быть равен 0. В этом случае solve выбрасывает исключение.
        """
        with pytest.raises(ValueError, match="Коэффициент a не может быть равен 0"):
            self.solver.solve(0, 1, 1)
    
    def test_solve_linear_equation_when_a_zero(self):
        """
        Тест: решение линейного уравнения (a = 0, b ≠ 0).
        """
        result = self.solver.solve(0, 2, -4)  # 2x - 4 = 0
        expected = [Root(2.0)]
        
        assert len(result) == 1
        assert result[0] == expected[0]
    
    def test_solve_constant_equation_when_a_and_b_zero(self):
        """
        Тест: константное уравнение (a = 0, b = 0, c ≠ 0).
        """
        result = self.solver.solve(0, 0, 5)  # 5 = 0
        assert len(result) == 0
    
    def test_two_real_roots_for_x_squared_minus_1(self):
        """
        Тест: для уравнения x² - 1 = 0 есть два действительных корня (x1=1, x2=-1).
        """
        result = self.solver.solve(1, 0, -1)
        expected = [Root(1.0), Root(-1.0)]
        assert len(result) == 2
        assert roots_equal(result, expected)
    
    def test_solve_quadratic_two_real_roots(self):
        """
        Тест: квадратное уравнение с двумя различными действительными корнями.
        """
        result = self.solver.solve(1, -5, 6)  # x² - 5x + 6 = 0
        expected = [Root(2.0), Root(3.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
    
    def test_one_root_of_multiplicity_two_for_x_squared_plus_2x_plus_1(self):
        """
        Тест: для уравнения x² + 2x + 1 = 0 есть один корень кратности 2 (x1 = x2 = -1).
        """
        result = self.solver.solve(1, 2, 1)
        expected = [Root(-1.0)]
        assert len(result) == 1
        assert result[0] == expected[0]
    
    def test_one_root_of_multiplicity_two_with_epsilon_for_x_squared_plus_2x_plus_1(self):
        """
        Тест: для уравнения x² + 2x + 1 = 0 есть один корень кратности 2 (x1 = x2 = -1),
        но с коэффициентами, при которых дискриминант отличен от нуля, но меньше заданного эпсилон.
        """
        # Подбираем коэффициенты так, чтобы дискриминант был очень маленьким, но не нулевым
        # Для уравнения x² + 2x + (1 + 1e-10) = 0
        # Дискриминант = 4 - 4(1 + 1e-10) = 4 - 4 - 4e-10 = -4e-10
        # Но мы хотим положительный дискриминант, близкий к нулю
        # Для уравнения x² + 2x + (1 - 1e-10) = 0
        # Дискриминант = 4 - 4(1 - 1e-10) = 4 - 4 + 4e-10 = 4e-10, что очень мало
        result = self.solver.solve(1, 2, 1 - 1e-10)
        # Ожидаем один корень около -1.0
        assert len(result) == 1
        assert float_equal(result[0].real, -1.0)
    
    def test_solve_quadratic_one_real_root(self):
        """
        Тест: квадратное уравнение с одним действительным корнем (дискриминант = 0).
        """
        result = self.solver.solve(1, -4, 4)  # x² - 4x + 4 = 0
        expected = [Root(2.0)]
        
        assert len(result) == 1
        assert result[0] == expected[0]
    
    def test_solve_quadratic_complex_roots(self):
        """
        Тест: квадратное уравнение с двумя комплексными корнями.
        """
        result = self.solver.solve(1, 0, 1)  # x² + 1 = 0
        expected = [Root(0.0, 1.0), Root(0.0, -1.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
    
    def test_solve_with_float_precision(self):
        """
        Тест: проверка точности вычислений с плавающей точкой.
        """
        # Уравнение с корнями, которые могут вызвать проблемы с точностью
        result = self.solver.solve(1, -6, 9)  # x² - 6x + 9 = 0
        
        assert len(result) == 1
        # Проверяем, что корень близок к 3.0 с учетом погрешности
        assert float_equal(result[0].real, 3.0)
    
    def test_solve_with_small_coefficients(self):
        """
        Тест: уравнение с очень малыми коэффициентами.
        """
        result = self.solver.solve(1e-10, -2e-10, 1e-10)  # 1e-10x² - 2e-10x + 1e-10 = 0
        
        assert len(result) == 1
        # Ожидаем корень около 1.0
        assert float_equal(result[0].real, 1.0)
    
    def test_solve_with_large_coefficients(self):
        """
        Тест: уравнение с очень большими коэффициентами.
        """
        result = self.solver.solve(1e10, -2e10, 1e10)  # 1e10x² - 2e10x + 1e10 = 0
        
        assert len(result) == 1
        # Ожидаем корень около 1.0
        assert float_equal(result[0].real, 1.0)
    
    def test_solve_with_negative_a(self):
        """
        Тест: уравнение с отрицательным коэффициентом a.
        """
        result = self.solver.solve(-1, 0, 4)  # -x² + 4 = 0
        expected = [Root(2.0), Root(-2.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
    
    def test_solve_with_fractional_coefficients(self):
        """
        Тест: уравнение с дробными коэффициентами.
        """
        result = self.solver.solve(0.5, -1.5, 1.0)  # 0.5x² - 1.5x + 1 = 0
        expected = [Root(1.0), Root(2.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
    """
    Тесты для класса QuadraticSolver.
    """
    
    def setup_method(self):
        """
        Инициализация перед каждым тестом.
        """
        self.solver = QuadraticSolver()
    
    def test_solve_raises_value_error_when_all_coefficients_zero(self):
        """
        Тест: при всех нулевых коэффициентах должно выбрасываться ValueError.
        """
        with pytest.raises(ValueError, match="имеет бесконечно много решений"):
            self.solver.solve(0, 0, 0)
    
    def test_solve_linear_equation_when_a_zero(self):
        """
        Тест: решение линейного уравнения (a = 0, b ≠ 0).
        """
        result = self.solver.solve(0, 2, -4)  # 2x - 4 = 0
        expected = [Root(2.0)]
        
        assert len(result) == 1
        assert result[0] == expected[0]
    
    def test_solve_constant_equation_when_a_and_b_zero(self):
        """
        Тест: константное уравнение (a = 0, b = 0, c ≠ 0).
        """
        result = self.solver.solve(0, 0, 5)  # 5 = 0
        assert len(result) == 0
    
    def test_solve_quadratic_two_real_roots(self):
        """
        Тест: квадратное уравнение с двумя различными действительными корнями.
        """
        result = self.solver.solve(1, -5, 6)  # x² - 5x + 6 = 0
        expected = [Root(2.0), Root(3.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
    
    def test_solve_quadratic_one_real_root(self):
        """
        Тест: квадратное уравнение с одним действительным корнем (дискриминант = 0).
        """
        result = self.solver.solve(1, -4, 4)  # x² - 4x + 4 = 0
        expected = [Root(2.0)]
        
        assert len(result) == 1
        assert result[0] == expected[0]
    
    def test_solve_quadratic_complex_roots(self):
        """
        Тест: квадратное уравнение с двумя комплексными корнями.
        """
        result = self.solver.solve(1, 0, 1)  # x² + 1 = 0
        expected = [Root(0.0, 1.0), Root(0.0, -1.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
    
    def test_solve_with_float_precision(self):
        """
        Тест: проверка точности вычислений с плавающей точкой.
        """
        # Уравнение с корнями, которые могут вызвать проблемы с точностью
        result = self.solver.solve(1, -6, 9)  # x² - 6x + 9 = 0
        
        assert len(result) == 1
        # Проверяем, что корень близок к 3.0 с учетом погрешности
        assert float_equal(result[0].real, 3.0)
    
    def test_solve_with_small_coefficients(self):
        """
        Тест: уравнение с очень малыми коэффициентами.
        """
        result = self.solver.solve(1e-10, -2e-10, 1e-10)  # 1e-10x² - 2e-10x + 1e-10 = 0
        
        assert len(result) == 1
        # Ожидаем корень около 1.0
        assert float_equal(result[0].real, 1.0)
    
    def test_solve_with_large_coefficients(self):
        """
        Тест: уравнение с очень большими коэффициентами.
        """
        result = self.solver.solve(1e10, -2e10, 1e10)  # 1e10x² - 2e10x + 1e10 = 0
        
        assert len(result) == 1
        # Ожидаем корень около 1.0
        assert float_equal(result[0].real, 1.0)
    
    def test_solve_with_negative_a(self):
        """
        Тест: уравнение с отрицательным коэффициентом a.
        """
        result = self.solver.solve(-1, 0, 4)  # -x² + 4 = 0
        expected = [Root(2.0), Root(-2.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
    
    def test_solve_with_fractional_coefficients(self):
        """
        Тест: уравнение с дробными коэффициентами.
        """
        result = self.solver.solve(0.5, -1.5, 1.0)  # 0.5x² - 1.5x + 1 = 0
        expected = [Root(1.0), Root(2.0)]
        
        assert len(result) == 2
        assert roots_equal(result, expected)
