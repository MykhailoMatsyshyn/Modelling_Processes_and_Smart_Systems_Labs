import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from colorama import init, Fore, Style

# Ініціалізація кольорів
init()

# Вхідні параметри
H = 1000 - 12  # Загальна кількість людей
beta = 25 - 12  # Інтенсивність розмноження епідемії
gamma = 12  # Коефіцієнт одужання
x0 = 900 - 12  # Початкова кількість здорових людей
y0 = 90 - 12   # Початкова кількість хворих
z0 = H - x0 - y0  # Початкова кількість одужалих
t0 = 0    # Початковий час
T = 40    # Кінцевий час
h = 0.1   # Крок інтегрування

# Кількість кроків
n_steps = int((T - t0) / h) + 1
t = np.linspace(t0, T, n_steps)  # Масив часу

# Ініціалізація масивів для зберігання результатів
x = np.zeros(n_steps)
y = np.zeros(n_steps)
z = np.zeros(n_steps)
x[0] = x0
y[0] = y0
z[0] = z0

# Крок 1: Виведення вхідних даних у таблиці
print(f"{Fore.CYAN}\n\n=== Крок 1: Вхідні дані ===\n{Style.RESET_ALL}")
table_data = [
    ["Параметр", "Значення", "Опис"],
    ["H", H, "Загальна кількість людей"],
    ["β", beta, "Інтенсивність розмноження епідемії"],
    ["γ", gamma, "Коефіцієнт одужання"],
    ["x(0)", x0, "Початкова кількість здорових людей"],
    ["y(0)", y0, "Початкова кількість хворих"],
    ["z(0)", z0, "Початкова кількість одужалих"],
    ["t0", t0, "Початковий час (дні)"],
    ["T", T, "Кінцевий час (дні)"],
    ["h", h, "Крок інтегрування (дні)"],
    ["Кількість кроків", n_steps, "Загальна кількість ітерацій"]
]
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
print("\n")

# Крок 2: Виведення моделі епідемії
print(f"{Fore.CYAN}=== Крок 2: Модель епідемії ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Система диференціальних рівнянь:{Style.RESET_ALL}")
print("""
╭───────────────────────────────╮
│ dx/dt = -(β/H)xy              │
│ dy/dt = (β/H)xy - (1/γ)y      │
│ dz/dt = (1/γ)y                │
╰───────────────────────────────╯
""")
print(f"{Style.BRIGHT}Підставимо значення коефіцієнтів (β/H = {beta/H:.6f}, 1/γ = {1/gamma:.6f}):{Style.RESET_ALL}")
print(f"dx/dt = -{beta/H:.6f}xy")
print(f"dy/dt = {beta/H:.6f}xy - {1/gamma:.6f}y")
print(f"dz/dt = {1/gamma:.6f}y\n")

# Крок 3: Опис методу Рунге-Кутта
print(f"{Fore.CYAN}=== Крок 3: Метод Рунге-Кутта 4-го порядку ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Формули для обчислення на кожному кроці:{Style.RESET_ALL}")
print("""
╭────────────────────────────────────────────╮
│ xₙ₊₁ = xₙ + (h/6)(k₁ₓ + 2k₂ₓ + 2k₃ₓ + k₄ₓ) │
│ yₙ₊₁ = yₙ + (h/6)(k₁y + 2k₂y + 2k₃y + k₄y) │
│ zₙ₊₁ = zₙ + (h/6)(k₁z + 2k₂z + 2k₃z + k₄z) │
│                                            │
│ де:                                        │
│ k₁ₓ = fₓ(xₙ, yₙ),         k₁y = fᵧ(xₙ, yₙ) │
│ k₁z = f_z(xₙ, yₙ)                         │
│                                            │
│ k₂ₓ = fₓ(xₙ + (h/2)k₁ₓ, yₙ + (h/2)k₁y),    │
│ k₂y = fᵧ(xₙ + (h/2)k₁ₓ, yₙ + (h/2)k₁y),    │
│ k₂z = f_z(xₙ + (h/2)k₁ₓ, yₙ + (h/2)k₁y)    │
│                                            │
│ k₃ₓ = fₓ(xₙ + (h/2)k₂ₓ, yₙ + (h/2)k₂y),    │
│ k₃y = fᵧ(xₙ + (h/2)k₂ₓ, yₙ + (h/2)k₂y),    │
│ k₃z = f_z(xₙ + (h/2)k₂ₓ, yₙ + (h/2)k₂y)    │
│                                            │
│ k₄ₓ = fₓ(xₙ + h k₃ₓ, yₙ + h k₃y),          │
│ k₄y = fᵧ(xₙ + h k₃ₓ, yₙ + h k₃y),          │
│ k₄z = f_z(xₙ + h k₃ₓ, yₙ + h k₃y)          │
╰────────────────────────────────────────────╯
""")
print(f"{Fore.YELLOW}Функції fₓ, fᵧ і f_z (праві частини рівнянь):{Style.RESET_ALL}")
print(f"fₓ(x, y) = -{beta/H:.6f}xy")
print(f"fᵧ(x, y) = {beta/H:.6f}xy - {1/gamma:.6f}y")
print(f"f_z(x, y) = {1/gamma:.6f}y\n")

# Крок 4: Покрокове обчислення (перші 5 ітерацій для наочності)
print(f"{Fore.CYAN}=== Крок 4: Покрокове обчислення (перші 5 ітерацій) ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Обчислення значень x(t), y(t) і z(t) методом Рунге-Кутта:{Style.RESET_ALL}")

# Таблиця для покрокового виведення
table_steps = [["Крок", "Час (t)", "Здорові (x)", "Хворі (y)", "Одужалі (z)", "k1x", "k1y", "k1z", "k2x", "k2y", "k2z", "k3x", "k3y", "k3z", "k4x", "k4y", "k4z"]]
for i in range(min(5, n_steps - 1)):
    # Обчислення коефіцієнтів k
    k1x = -(beta/H) * x[i] * y[i]
    k1y = (beta/H) * x[i] * y[i] - (1/gamma) * y[i]
    k1z = (1/gamma) * y[i]
    
    k2x = -(beta/H) * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y)
    k2y = (beta/H) * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y) - (1/gamma) * (y[i] + h/2 * k1y)
    k2z = (1/gamma) * (y[i] + h/2 * k1y)
    
    k3x = -(beta/H) * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y)
    k3y = (beta/H) * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y) - (1/gamma) * (y[i] + h/2 * k2y)
    k3z = (1/gamma) * (y[i] + h/2 * k2y)
    
    k4x = -(beta/H) * (x[i] + h * k3x) * (y[i] + h * k3y)
    k4y = (beta/H) * (x[i] + h * k3x) * (y[i] + h * k3y) - (1/gamma) * (y[i] + h * k3y)
    k4z = (1/gamma) * (y[i] + h * k3y)
    
    # Оновлення значень x, y, z
    x[i+1] = x[i] + (h/6) * (k1x + 2*k2x + 2*k3x + k4x)
    y[i+1] = y[i] + (h/6) * (k1y + 2*k2y + 2*k3y + k4y)
    z[i+1] = z[i] + (h/6) * (k1z + 2*k2z + 2*k3z + k4z)
    
    # Додаємо дані до таблиці
    table_steps.append([i+1, f"{t[i]:.1f}", f"{x[i]:.2f}", f"{y[i]:.2f}", f"{z[i]:.2f}", 
                        f"{k1x:.2f}", f"{k1y:.2f}", f"{k1z:.2f}", 
                        f"{k2x:.2f}", f"{k2y:.2f}", f"{k2z:.2f}", 
                        f"{k3x:.2f}", f"{k3y:.2f}", f"{k3z:.2f}", 
                        f"{k4x:.2f}", f"{k4y:.2f}", f"{k4z:.2f}"])

# Виводимо таблицю покрокового обчислення
print(tabulate(table_steps, headers="firstrow", tablefmt="grid"))
print("\n")

# Завершуємо обчислення для всіх кроків
for i in range(5, n_steps - 1):
    k1x = -(beta/H) * x[i] * y[i]
    k1y = (beta/H) * x[i] * y[i] - (1/gamma) * y[i]
    k1z = (1/gamma) * y[i]
    
    k2x = -(beta/H) * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y)
    k2y = (beta/H) * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y) - (1/gamma) * (y[i] + h/2 * k1y)
    k2z = (1/gamma) * (y[i] + h/2 * k1y)
    
    k3x = -(beta/H) * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y)
    k3y = (beta/H) * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y) - (1/gamma) * (y[i] + h/2 * k2y)
    k3z = (1/gamma) * (y[i] + h/2 * k2y)
    
    k4x = -(beta/H) * (x[i] + h * k3x) * (y[i] + h * k3y)
    k4y = (beta/H) * (x[i] + h * k3x) * (y[i] + h * k3y) - (1/gamma) * (y[i] + h * k3y)
    k4z = (1/gamma) * (y[i] + h * k3y)
    
    x[i+1] = x[i] + (h/6) * (k1x + 2*k2x + 2*k3x + k4x)
    y[i+1] = y[i] + (h/6) * (k1y + 2*k2y + 2*k3y + k4y)
    z[i+1] = z[i] + (h/6) * (k1z + 2*k2z + 2*k3z + k4z)

# Крок 5: Виведення результатів (таблиця перших 10 значень)
print(f"{Fore.CYAN}=== Крок 5: Результати обчислень (перші 10 значень) ===\n{Style.RESET_ALL}")
table_results = [["Час (t)", "Здорові (x)", "Хворі (y)", "Одужалі (z)"]]
for i in range(min(10, n_steps)):
    table_results.append([f"{t[i]:.1f}", f"{x[i]:.2f}", f"{y[i]:.2f}", f"{z[i]:.2f}"])
print(tabulate(table_results, headers="firstrow", tablefmt="grid"))
print("\n")

# Крок 6: Побудова графіка
print(f"{Fore.CYAN}=== Крок 6: Побудова графіка ===\n{Style.RESET_ALL}")
plt.figure(figsize=(12, 6))  # Зменшуємо розмір, оскільки лише один графік

# Графік x(t), y(t), z(t)
plt.plot(t, x, label='Здорові (x(t))', color='blue')
plt.plot(t, y, label='Хворі (y(t))', color='red')
plt.plot(t, z, label='Одужалі (z(t))', color='green')
plt.title('Динаміка чисельності здорових, хворих і одужалих з часом')
plt.xlabel('Час (дні)')
plt.ylabel('Чисельність')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print(f"{Fore.GREEN}Готово! Графік відображений для аналізу!{Style.RESET_ALL}")