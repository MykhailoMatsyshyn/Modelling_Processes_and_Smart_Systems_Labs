import numpy as np
from tabulate import tabulate
from colorama import init, Fore, Style

# Ініціалізація кольорів
init()

# Вхідні параметри (варіант 12)
a = 0.52e-6  # коефіцієнт температуропровідності, м^2/с
L = 1.0      # товщина стінки, м
T = 240 * 3600  # час моделювання, с (240 годин)
N = 100      # кількість шарів
h = 1.0      # крок за часом, с
alpha = 12.0 # температура зліва, °C
beta = 31.0  # температура справа, °C
t0 = 0       # початковий час, с

# Обчислення параметрів
delta = L / N  # товщина одного шару
mu = a / (delta ** 2)  # коефіцієнт mu
num_steps = int((T - t0) / h) + 1  # кількість кроків за часом
t = np.linspace(t0, T, num_steps)  # масив часу

# Ініціалізація масиву температур
# u[i, t] — температура в точці i на момент часу t
u = np.zeros((N+1, num_steps))  # N+1 точок (включаючи межі), num_steps моментів часу

# Початкові умови
u[:, 0] = 0.0  # температура всередині = 0°C
# Граничні умови
u[0, :] = alpha  # ліва межа
u[N, :] = beta   # права межа

# Крок 1: Виведення вхідних даних у таблиці
print(f"{Fore.CYAN}\n\n=== Крок 1: Вхідні дані ===\n{Style.RESET_ALL}")
table_data = [
    ["Параметр", "Значення", "Опис"],
    ["a", f"{a:.2e}", "Коефіцієнт температуропровідності (м²/с)"],
    ["L", L, "Товщина стінки (м)"],
    ["T", T, "Час моделювання (с)"],
    ["T (години)", T/3600, "Час моделювання (год)"],
    ["N", N, "Кількість шарів"],
    ["δ", delta, "Товщина одного шару (м)"],
    ["μ", f"{mu:.4f}", "Коефіцієнт μ = a/δ²"],
    ["h", h, "Крок інтегрування (с)"],
    ["α", alpha, "Температура зліва (°C)"],
    ["β", beta, "Температура справа (°C)"],
    ["t0", t0, "Початковий час (с)"],
    ["Кількість кроків", num_steps, "Загальна кількість ітерацій"]
]
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
print("\n")

# Крок 2: Виведення моделі теплопровідності
print(f"{Fore.CYAN}=== Крок 2: Модель теплопровідності ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Рівняння теплопровідності:{Style.RESET_ALL}")
print("""
╭───────────────────────────────╮
│ ∂u(t,y)/∂t = a ∂²u(t,y)/∂y²   │
╰───────────────────────────────╯
""")
print(f"{Fore.YELLOW}Апроксимація другої похідної методом кінцевих різниць:{Style.RESET_ALL}")
print("""
╭─────────────────────────────────────────────────────────╮
│ ∂²u(t,y)/∂y² ≈ (u_{i+1}(t) - 2u_i(t) + u_{i-1}(t)) / δ² │
╰─────────────────────────────────────────────────────────╯
""")
print(f"{Style.BRIGHT}Отримана система звичайних диференціальних рівнянь:{Style.RESET_ALL}")
print(f"\ndu_i(t)/dt = (a/δ²) (u_{{i+1}}(t) - 2 u_i(t) + u_{{i-1}}(t))")
print(f"де a/δ² = μ = {mu:.4f}")
print(f"\nОтже:")
print(f"du_i(t)/dt = {mu:.4f} (u_{{i+1}}(t) - 2 u_i(t) + u_{{i-1}}(t))\n")

# Крок 3: Початкові та граничні умови
print(f"{Fore.CYAN}=== Крок 3: Початкові та граничні умови ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Граничні умови:{Style.RESET_ALL}")
print(f"u_1(t) = {alpha}°C (ліва межа)")
print(f"u_{N+1}(t) = {beta}°C (права межа)")
print(f"\n{Fore.YELLOW}Початкові умови:{Style.RESET_ALL}")
print(f"u_i(0) = 0°C для i = 2, 3, ..., {N}\n")

# Крок 4: Опис методу Рунге-Кутта
print(f"{Fore.CYAN}=== Крок 4: Метод Рунге-Кутта 4-го порядку ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Формули для обчислення на кожному кроці:{Style.RESET_ALL}")
print("""
╭────────────────────────────────────────────────╮
│ u_i^{n+1} = u_i^n + (h/6)(k₁ + 2k₂ + 2k₃ + k₄) │
│                                                │
│ де:                                            │
│ k₁ = f(u_i^n),                                 │
│ k₂ = f(u_i^n + (h/2)k₁),                       │
│ k₃ = f(u_i^n + (h/2)k₂),                       │
│ k₄ = f(u_i^n + h k₃)                           │
╰────────────────────────────────────────────────╯
""")
print(f"{Fore.YELLOW}Функція f (права частина рівняння):{Style.RESET_ALL}")
print(f"f(u_i) = {mu:.4f} (u_{{i+1}} - 2 u_i + u_{{i-1}})\n")

# Функція для обчислення правої частини системи ОДР
def compute_derivatives(u_t):
    du_dt = np.zeros(N-1)  # для u_2, u_3, ..., u_100
    for i in range(1, N):
        du_dt[i-1] = mu * (u_t[i+1] - 2 * u_t[i] + u_t[i-1])
    return du_dt

# Метод Рунге-Кутта 4-го порядку
def runge_kutta_step(u_t, h):
    u_inner = u_t[1:N]  # внутрішні точки (u_2, ..., u_100)
    k1 = compute_derivatives(u_t)
    k2 = compute_derivatives(u_t + (h/2) * np.concatenate(([0], k1, [0])))
    k3 = compute_derivatives(u_t + (h/2) * np.concatenate(([0], k2, [0])))
    k4 = compute_derivatives(u_t + h * np.concatenate(([0], k3, [0])))
    u_inner_new = u_inner + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
    return np.concatenate(([u_t[0]], u_inner_new, [u_t[N]]))

# Крок 5: Покрокове обчислення (перші 5 ітерацій для наочності)
print(f"{Fore.CYAN}=== Крок 5: Покрокове обчислення (перші 5 ітерацій) ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Обчислення значень u_i(t) методом Рунге-Кутта:{Style.RESET_ALL}")

# Таблиця для покрокового виведення (виберемо кілька точок для наочності)
table_steps = [["Крок", "Час (с)", "u_1 (°C)", "u_2 (°C)", "u_3 (°C)", "u_51 (°C)", "u_100 (°C)", "u_101 (°C)"]]
for step in range(min(5, num_steps - 1)):
    # Зберігаємо значення для виведення
    u_current = u[:, step]
    # Обчислюємо k для другої точки (i=2) для прикладу
    k1 = compute_derivatives(u_current)
    k2 = compute_derivatives(u_current + (h/2) * np.concatenate(([0], k1, [0])))
    k3 = compute_derivatives(u_current + (h/2) * np.concatenate(([0], k2, [0])))
    k4 = compute_derivatives(u_current + h * np.concatenate(([0], k3, [0])))
    
    # Оновлюємо температури
    u[:, step+1] = runge_kutta_step(u[:, step], h)
    
    # Додаємо дані до таблиці (вибираємо точки i=1, 2, 3, 51, 100, 101)
    table_steps.append([step+1, f"{t[step]:.1f}", 
                        f"{u[0, step]:.2f}", f"{u[1, step]:.2f}", f"{u[2, step]:.2f}", 
                        f"{u[50, step]:.2f}", f"{u[99, step]:.2f}", f"{u[100, step]:.2f}"])

# Виводимо таблицю покрокового обчислення
print(tabulate(table_steps, headers="firstrow", tablefmt="grid"))
print("\n")

# Завершуємо обчислення для всіх кроків
print(f"{Fore.CYAN}=== Крок 6: Завершення обчислень ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Виконуємо інтегрування для всіх {num_steps} кроків...{Style.RESET_ALL}")
for step in range(5, num_steps - 1):
    u[:, step+1] = runge_kutta_step(u[:, step], h)
print(f"{Fore.GREEN}Обчислення завершено!{Style.RESET_ALL}\n")

# Крок 7: Виведення результатів (температура в кількох точках на кількох моментах часу)
print(f"{Fore.CYAN}=== Крок 7: Результати обчислень ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Температура в кількох точках на різних моментах часу:{Style.RESET_ALL}")

# Вибираємо кілька моментів часу для виведення (наприклад, кожні 24 години)
time_points = [0, 24*3600, 48*3600, 120*3600, 240*3600]  # 0, 24 год, 48 год, 120 год, 240 год
table_results = [["Час (год)", "y=0 (u_1)", "y=0.01 (u_2)", "y=0.02 (u_3)", "y=0.5 (u_51)", "y=0.99 (u_100)", "y=1.0 (u_101)"]]
for time in time_points:
    step = int(time / h)
    if step < num_steps:
        table_results.append([f"{time/3600:.1f}", 
                              f"{u[0, step]:.2f}", f"{u[1, step]:.2f}", f"{u[2, step]:.2f}", 
                              f"{u[50, step]:.2f}", f"{u[99, step]:.2f}", f"{u[100, step]:.2f}"])
print(tabulate(table_results, headers="firstrow", tablefmt="grid"))
print("\n")

# Зберігаємо результати для завдання 2
np.save("temperature_data.npy", u)

print(f"{Fore.GREEN}Готово! Дані збережено у файл temperature_data.npy для подальшого використання!{Style.RESET_ALL}")