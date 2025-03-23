import numpy as np
import matplotlib.pyplot as plt

# Вхідні дані для варіанту 12 (n = 12)
x1 = np.array([0, 0, 0, 1, 1, 2, 2, 2])
x2 = np.array([1.5, 2.5, 3.5, 1.5, 3.5, 1.5, 2.5, 2.5])
n = 12
y = np.array([
    2.3, 
    4 + 0.3 * n, 
    2 - 0.1 * n, 
    5 - 0.2 * n, 
    4 - 0.2 * n, 
    6.1 + 0.2 * n, 
    6.5 - 0.1 * n, 
    7.2
])

# Обчислення значень y для n = 12
y = np.array([2.3, 7.6, 0.8, 2.6, 1.6, 8.5, 5.3, 7.2])

# Формуємо матрицю для методу найменших квадратів
A = np.vstack([np.ones(len(x1)), x1, x2]).T  # Матриця [1, x1, x2]
coeffs = np.linalg.lstsq(A, y, rcond=None)[0]  # Розв'язок системи
a0, a1, a2 = coeffs

# Виведення коефіцієнтів
print(f"Знайдені коефіцієнти: a0 = {a0:.4f}, a1 = {a1:.4f}, a2 = {a2:.4f}")
print(f"Рівняння: y = {a0:.4f} + {a1:.4f}x1 + {a2:.4f}x2")

# Обчислення значення функції в точці (x1 = 1.5, x2 = 3)
x1_test, x2_test = 1.5, 3
y_test = a0 + a1 * x1_test + a2 * x2_test
print(f"Значення функції в точці (x1 = {x1_test}, x2 = {x2_test}): y = {y_test:.4f}")

# Передбачені значення y
y_pred = a0 + a1 * x1 + a2 * x2

# Обчислення коефіцієнта детермінації R²
y_mean = np.mean(y)
ss_tot = np.sum((y - y_mean) ** 2)
ss_res = np.sum((y - y_pred) ** 2)
R2 = 1 - ss_res / ss_tot
print(f"Коефіцієнт детермінації R² = {R2:.4f}")

# Побудова графіка
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x1, x2, y, color='blue', label='Експериментальні дані')

# Створення сітки для поверхні
x1_range = np.linspace(min(x1), max(x1), 10)
x2_range = np.linspace(min(x2), max(x2), 10)
X1, X2 = np.meshgrid(x1_range, x2_range)
Y = a0 + a1 * X1 + a2 * X2
ax.plot_surface(X1, X2, Y, color='red', alpha=0.5, label='Апроксимація')

ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('y')
plt.title('Залежність y від x1 та x2')
plt.show()