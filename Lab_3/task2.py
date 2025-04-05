import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tabulate import tabulate
from colorama import init, Fore, Style

# Ініціалізація кольорів
init()

# Вхідні параметри (з завдання 1)
a = 0.52e-6  # коефіцієнт температуропровідності, м^2/с
L = 1.0      # товщина стінки, м
T = 240 * 3600  # час моделювання, с (240 годин)
N = 100      # кількість шарів
h = 1.0      # крок за часом, с
alpha = 12.0 # температура зліва, °C
beta = 31.0  # температура справа, °C
t0 = 0       # початковий час, с

# Обчислення параметрів
num_steps = int((T - t0) / h) + 1  # кількість кроків за часом
y = np.linspace(0, L, N+1)  # масив координат y (від 0 до 1, 101 точка)
t = np.linspace(t0, T, num_steps)  # масив часу в секундах (від 0 до 864000 с)
t_hours = t / 3600  # масив часу в годинах (від 0 до 240 год)

# Завантажуємо числовий розв’язок із завдання 1
u_numerical = np.load("temperature_data.npy")  # розмір: (N+1) x num_steps

# Крок 1: Виведення вхідних даних
print(f"{Fore.CYAN}\n\n=== Крок 1: Вхідні дані ===\n{Style.RESET_ALL}")
table_data = [
    ["Параметр", "Значення", "Опис"],
    ["a", f"{a:.2e}", "Коефіцієнт температуропровідності (м²/с)"],
    ["L", L, "Товщина стінки (м)"],
    ["T", T, "Час моделювання (с)"],
    ["T (години)", T/3600, "Час моделювання (год)"],
    ["N", N, "Кількість шарів"],
    ["h", h, "Крок інтегрування (с)"],
    ["α", alpha, "Температура зліва (°C)"],
    ["β", beta, "Температура справа (°C)"],
    ["t0", t0, "Початковий час (с)"],
    ["Кількість кроків", num_steps, "Загальна кількість ітерацій"]
]
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
print("\n")

# Крок 2: Обчислення аналітичного розв’язку за формулою (17)
print(f"{Fore.CYAN}=== Крок 2: Аналітичний розв’язок ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Формула аналітичного розв’язку (обмежуємося 30 доданками):{Style.RESET_ALL}")
print("""
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ u(t,y) = (β-α)/L * y + α + (2/π) Σ_{n=1}^{30} (1/n) (β(-1)^n - α) e^{-a t (πn/L)^2} sin(πn y / L) │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
""")

# Функція для аналітичного розв’язку (векторизована)
def analytical_solution(t, y, a, L, alpha, beta, terms=30):
    # Створюємо сітку для t і y
    T, Y = np.meshgrid(t, y)
    U = (beta - alpha) / L * Y + alpha  # стаціонарна частина

    # Обчислюємо нестаціонарну частину (ряд)
    for n in range(1, terms + 1):
        U += (2 / np.pi) * (1 / n) * (beta * (-1)**n - alpha) * \
             np.exp(-a * T * (np.pi * n / L)**2) * \
             np.sin(np.pi * n * Y / L)
    return U

# Обчислюємо аналітичний розв’язок для всіх точок
print(f"{Fore.YELLOW}Обчислюємо аналітичний розв’язок для всіх {num_steps} моментів часу...{Style.RESET_ALL}")
u_analytical = analytical_solution(t, y, a, L, alpha, beta, terms=30)
print(f"{Fore.GREEN}Аналітичний розв’язок обчислено!{Style.RESET_ALL}\n")

# Крок 3: Побудова двох 3D-графіків
print(f"{Fore.CYAN}=== Крок 3: Побудова 3D-графіків ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Візуалізація числового та аналітичного розв’язків (усі точки):{Style.RESET_ALL}")

# Створюємо сітку для 3D-графіка
T_hours, Y = np.meshgrid(t_hours, y)

# Створюємо два графіки поруч
fig = plt.figure(figsize=(15, 6))

# Графік 1: Числовий розв’язок
ax1 = fig.add_subplot(121, projection='3d')
surf1 = ax1.plot_surface(T_hours, Y, u_numerical, cmap='viridis') 
ax1.set_xlabel('Час (години)')
ax1.set_ylabel('Положення y (м)')
ax1.set_zlabel('Температура (°C)')
ax1.set_title('Числовий розв’язок')
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)

# Графік 2: Аналітичний розв’язок
ax2 = fig.add_subplot(122, projection='3d')
surf2 = ax2.plot_surface(T_hours, Y, u_analytical, cmap='viridis')
ax2.set_xlabel('Час (години)')
ax2.set_ylabel('Положення y (м)')
ax2.set_zlabel('Температура (°C)')
ax2.set_title('Аналітичний розв’язок')
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=5)

plt.tight_layout()
plt.show()
print(f"{Fore.GREEN}Графіки побудовано!{Style.RESET_ALL}\n")

# Крок 4: Обчислення похибок MAE і MSE
print(f"{Fore.CYAN}=== Крок 4: Обчислення похибок MAE і MSE ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Формули для похибок:{Style.RESET_ALL}")
print("""
╭───────────────────────────────────────────────────────────────╮
│ MAE = max_{1≤i≤M, 1≤j≤N} |u(t_i,y_j) - û(t_i,y_j)|            │
│ MSE = 1/(M N) Σ_{i=1}^M Σ_{j=1}^N (u(t_i,y_j) - û(t_i,y_j))^2 │
╰───────────────────────────────────────────────────────────────╯
""")
print(f"де M = T/h - 1 = {num_steps - 1}")

# Обчислюємо різницю між числовим і аналітичним розв’язками
diff = np.abs(u_numerical - u_analytical)

# MAE — максимальна абсолютна похибка
mae = np.max(diff)

# MSE — середньоквадратична похибка
mse = np.sum(diff**2) / (num_steps * (N+1))

print(f"{Fore.YELLOW}Результати обчислення похибок:{Style.RESET_ALL}")
table_errors = [
    ["Похибка", "Значення", "Опис"],
    ["MAE", f"{mae:.6f}", "Максимальна абсолютна похибка (°C)"],
    ["MSE", f"{mse:.6f}", "Середньоквадратична похибка (°C²)"]
]
print(tabulate(table_errors, headers="firstrow", tablefmt="grid"))
print("\n")

print(f"{Fore.GREEN}Завдання 2 виконано!{Style.RESET_ALL}")