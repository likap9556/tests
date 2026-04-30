# Решатель квадратных уравнений

Проект для решения квадратных уравнений с использованием TDD и настроенным CI/CD.

## Особенности
- Реализация решения квадратного уравнения ax² + bx + c = 0
- Модульные тесты с использованием pytest
- Настроенный CI/CD процесс
- Поддержка особых случаев (a=0, комплексные корни)

## Установка
```bash
pip install -r requirements.txt
```

## Запуск тестов
```bash
pytest tests/
```

## Использование
```python
from quadratic_solver.solver import QuadraticSolver

solver = QuadraticSolver()
roots = solver.solve(1, -5, 6)  # x² - 5x + 6 = 0
print(roots)  # [2.0, 3.0]