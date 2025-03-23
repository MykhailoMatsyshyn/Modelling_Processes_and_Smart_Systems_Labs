import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Крок 1: Вводимо дані для 12-го варіанту
print("Крок 1: Вводимо дані")
x1 = np.array([0, 0, 0, 1, 1, 2, 2, 2])  # Значення x1
x2 = np.array([1.5, 2.5, 3.5, 1.5, 3.5, 1.5, 2.5, 2.5])  # Значення x2
y = np.array([2.3, 7.6, 0.8, 2.6, 1.6, 8.5, 5.3, 7.2])  # Значення y
n = len(x1)  # Кількість точок
print(f"x1: {x1}")
print(f"x2: {x2}")
print(f"y: {y}")
print(f"Кількість точок (n): {n}\n")

# Крок 2: Обчислюємо необхідні суми для системи рівнянь
print("Крок 2: Обчислюємо суми")
sum_x1 = np.sum(x1)  # Сума x1
sum_x2 = np.sum(x2)  # Сума x2
sum_y = np.sum(y)    # Сума y
sum_x1_sq = np.sum(x1**2)  # Сума квадратів x1
sum_x2_sq = np.sum(x2**2)  # Сума квадратів x2
sum_x1_x2 = np.sum(x1 * x2)  # Сума добутків x1 і x2
sum_x1_y = np.sum(x1 * y)    # Сума добутків x1 і y
sum_x2_y = np.sum(x2 * y)    # Сума добутків x2 і y

print(f"Сума x1: {sum_x1}")
print(f"Сума x2: {sum_x2}")
print(f"Сума y: {sum_y}")
print(f"Сума x1^2: {sum_x1_sq}")
print(f"Сума x2^2: {sum_x2_sq}")
print(f"Сума x1*x2: {sum_x1_x2}")
print(f"Сума x1*y: {sum_x1_y}")
print(f"Сума x2*y: {sum_x2_y}\n")

# Крок 3: Складаємо систему рівнянь (з методички)
print("Крок 3: Складаємо систему рівнянь")
# 1: n*a0 + sum_x1*a1 + sum_x2*a2 = sum_y
# 2: sum_x1*a0 + sum_x1_sq*a1 + sum_x1_x2*a2 = sum_x1_y
# 3: sum_x2*a0 + sum_x1_x2*a1 + sum_x2_sq*a2 = sum_x2_y
print(f"Рівняння 1: {n}a0 + {sum_x1}a1 + {sum_x2}a2 = {sum_y}")
print(f"Рівняння 2: {sum_x1}a0 + {sum_x1_sq}a1 + {sum_x1_x2}a2 = {sum_x1_y}")
print(f"Рівняння 3: {sum_x2}a0 + {sum_x1_x2}a1 + {sum_x2_sq}a2 = {sum_x2_y}\n")

# Крок 4: Розв’язуємо систему рівнянь за допомогою NumPy
print("Крок 4: Розв’язуємо систему")
# Матриця коефіцієнтів
A = np.array([
    [n, sum_x1, sum_x2],
    [sum_x1, sum_x1_sq, sum_x1_x2],
    [sum_x2, sum_x1_x2, sum_x2_sq]
])
# Вектор правих частин
b = np.array([sum_y, sum_x1_y, sum_x2_y])
# Розв’язок (a0, a1, a2)
coeffs = np.linalg.solve(A, b)
a0, a1, a2 = coeffs
print(f"a0 = {a0:.2f}")
print(f"a1 = {a1:.2f}")
print(f"a2 = {a2:.2f}")
print(f"Залежність: y = {a0:.2f} + {a1:.2f}x1 + {a2:.2f}x2\n")

# Крок 5: Обчислюємо y у точці (x1 = 1.5, x2 = 3)
print("Крок 5: Обчислюємо y у точці (1.5, 3)")
x1_test = 1.5
x2_test = 3
y_test = a0 + a1 * x1_test + a2 * x2_test
print(f"y({x1_test}, {x2_test}) = {a0:.2f} + {a1:.2f}*{x1_test} + {a2:.2f}*{x2_test} = {y_test:.2f}\n")

# Крок 6: Обчислюємо коефіцієнт детермінації R^2
print("Крок 6: Обчислюємо R^2")
# Передбачені значення y
y_pred = a0 + a1 * x1 + a2 * x2
print(f"Передбачені y: {y_pred}")
# Середнє значення y
y_mean = np.mean(y)
print(f"Середнє y: {y_mean:.2f}")
# Сума квадратів відхилень від передбачених значень (SS_res)
ss_res = np.sum((y - y_pred)**2)
# Сума квадратів відхилень від середнього (SS_tot)
ss_tot = np.sum((y - y_mean)**2)
# R^2
R2 = 1 - ss_res / ss_tot
print(f"SS_res = {ss_res:.2f}")
print(f"SS_tot = {ss_tot:.2f}")
print(f"R^2 = {R2:.3f}\n")

# Крок 7: Будуємо 3D-графік
print("Крок 7: Будуємо графік")
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Точки даних
ax.scatter(x1, x2, y, color='red', label='Дані', s=100)

# Площина регресії
x1_range = np.linspace(min(x1), max(x1), 20)
x2_range = np.linspace(min(x2), max(x2), 20)
X1, X2 = np.meshgrid(x1_range, x2_range)
Y = a0 + a1 * X1 + a2 * X2
ax.plot_surface(X1, X2, Y, alpha=0.5, color='blue', label='Площина регресії')

# Налаштування графіка
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('y')
ax.set_title('Метод найменших квадратів: y = {:.2f} + {:.2f}x1 + {:.2f}x2'.format(a0, a1, a2))
plt.legend()
plt.show()

print("Готово! Усе показано на графіку.")