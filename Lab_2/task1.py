import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from colorama import init, Fore, Style

# Ініціалізація кольорів
init()

# Вхідні параметри (варіант 12)
a11 = 0.12
a12 = 0.0012
a21 = 0.0012
a22 = 0.48
x0 = 880  # Початкова кількість метеликів
y0 = 580  # Початкова кількість павуків
t0 = 0    # Початковий час
T = 150   # Кінцевий час
h = 0.1   # Крок інтегрування

# Кількість кроків
n_steps = int((T - t0) / h) + 1
t = np.linspace(t0, T, n_steps)  # Масив часу

# Ініціалізація масивів для зберігання результатів
x = np.zeros(n_steps)
y = np.zeros(n_steps)
x[0] = x0
y[0] = y0

# Крок 1: Виведення вхідних даних у таблиці
print(f"{Fore.CYAN}\n\n=== Крок 1: Вхідні дані ===\n{Style.RESET_ALL}")
table_data = [
    ["Параметр", "Значення", "Опис"],
    ["a11", a11, "Коефіцієнт приросту метеликів"],
    ["a12", a12, "Коефіцієнт зменшення метеликів через павуків"],
    ["a21", a21, "Коефіцієнт приросту павуків за наявності метеликів"],
    ["a22", a22, "Коефіцієнт зменшення павуків без їжі"],
    ["x(0)", x0, "Початкова кількість метеликів"],
    ["y(0)", y0, "Початкова кількість павуків"],
    ["t0", t0, "Початковий час (дні)"],
    ["T", T, "Кінцевий час (дні)"],
    ["h", h, "Крок інтегрування (дні)"],
    ["Кількість кроків", n_steps, "Загальна кількість ітерацій"]
]
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
print("\n")

# Крок 2: Виведення моделі Лотки-Вольтерри
print(f"{Fore.CYAN}=== Крок 2: Модель Лотки-Вольтерри ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Система диференціальних рівнянь:{Style.RESET_ALL}")
print("""
╭──────────────────────╮
│ dx/dt = a₁₁x - a₁₂xy │
│ dy/dt = a₂₁xy - a₂₂y │
╰──────────────────────╯
""")
print(f"{Style.BRIGHT}Підставимо значення коефіцієнтів:{Style.RESET_ALL}")
print(f"dx/dt = {a11}x - {a12}xy")
print(f"dy/dt = {a21}xy - {a22}y\n")

# Крок 3: Опис методу Рунге-Кутта
print(f"{Fore.CYAN}=== Крок 3: Метод Рунге-Кутта 4-го порядку ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Формули для обчислення на кожному кроці:{Style.RESET_ALL}")
print("""
╭────────────────────────────────────────────╮
│ xₙ₊₁ = xₙ + (h/6)(k₁ₓ + 2k₂ₓ + 2k₃ₓ + k₄ₓ) │
│ yₙ₊₁ = yₙ + (h/6)(k₁y + 2k₂y + 2k₃y + k₄y) │
│                                            │
│ де:                                        │
│ k₁ₓ = fₓ(xₙ, yₙ),         k₁y = fᵧ(xₙ, yₙ) │
│                                            │
│ k₂ₓ = fₓ(xₙ + (h/2)k₁ₓ, yₙ + (h/2)k₁y),    │
│ k₂y = fᵧ(xₙ + (h/2)k₁ₓ, yₙ + (h/2)k₁y)     │
│                                            │
│ k₃ₓ = fₓ(xₙ + (h/2)k₂ₓ, yₙ + (h/2)k₂y),    │
│ k₃y = fᵧ(xₙ + (h/2)k₂ₓ, yₙ + (h/2)k₂y)     │
│                                            │
│ k₄ₓ = fₓ(xₙ + h k₃ₓ, yₙ + h k₃y),          │
│ k₄y = fᵧ(xₙ + h k₃ₓ, yₙ + h k₃y)           │
╰────────────────────────────────────────────╯
""")
print(f"{Fore.YELLOW}Функції fₓ і fᵧ (праві частини рівнянь):{Style.RESET_ALL}")
print(f"fₓ(x, y) = {a11}x - {a12}xy")
print(f"fᵧ(x, y) = {a21}xy - {a22}y\n")

# Крок 4: Покрокове обчислення (перші 5 ітерацій для наочності)
print(f"{Fore.CYAN}=== Крок 4: Покрокове обчислення (перші 5 ітерацій) ===\n{Style.RESET_ALL}")
print(f"{Fore.YELLOW}Обчислення значень x(t) і y(t) методом Рунге-Кутта:{Style.RESET_ALL}")

# Таблиця для покрокового виведення
table_steps = [["Крок", "Час (t)", "Метелики (x)", "Павуки (y)", "k1x", "k1y", "k2x", "k2y", "k3x", "k3y", "k4x", "k4y"]]
for i in range(min(5, n_steps - 1)):
    # Обчислення коефіцієнтів k
    k1x = a11 * x[i] - a12 * x[i] * y[i]
    k1y = a21 * x[i] * y[i] - a22 * y[i]
    
    k2x = a11 * (x[i] + h/2 * k1x) - a12 * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y)
    k2y = a21 * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y) - a22 * (y[i] + h/2 * k1y)
    
    k3x = a11 * (x[i] + h/2 * k2x) - a12 * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y)
    k3y = a21 * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y) - a22 * (y[i] + h/2 * k2y)
    
    k4x = a11 * (x[i] + h * k3x) - a12 * (x[i] + h * k3x) * (y[i] + h * k3y)
    k4y = a21 * (x[i] + h * k3x) * (y[i] + h * k3y) - a22 * (y[i] + h * k3y)
    
    # Оновлення значень x і y
    x[i+1] = x[i] + (h/6) * (k1x + 2*k2x + 2*k3x + k4x)
    y[i+1] = y[i] + (h/6) * (k1y + 2*k2y + 2*k3y + k4y)
    
    # Додаємо дані до таблиці
    table_steps.append([i+1, f"{t[i]:.1f}", f"{x[i]:.2f}", f"{y[i]:.2f}", 
                        f"{k1x:.2f}", f"{k1y:.2f}", f"{k2x:.2f}", f"{k2y:.2f}", 
                        f"{k3x:.2f}", f"{k3y:.2f}", f"{k4x:.2f}", f"{k4y:.2f}"])

# Виводимо таблицю покрокового обчислення
print(tabulate(table_steps, headers="firstrow", tablefmt="grid"))
print("\n")

# Завершуємо обчислення для всіх кроків
for i in range(5, n_steps - 1):
    k1x = a11 * x[i] - a12 * x[i] * y[i]
    k1y = a21 * x[i] * y[i] - a22 * y[i]
    
    k2x = a11 * (x[i] + h/2 * k1x) - a12 * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y)
    k2y = a21 * (x[i] + h/2 * k1x) * (y[i] + h/2 * k1y) - a22 * (y[i] + h/2 * k1y)
    
    k3x = a11 * (x[i] + h/2 * k2x) - a12 * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y)
    k3y = a21 * (x[i] + h/2 * k2x) * (y[i] + h/2 * k2y) - a22 * (y[i] + h/2 * k2y)
    
    k4x = a11 * (x[i] + h * k3x) - a12 * (x[i] + h * k3x) * (y[i] + h * k3y)
    k4y = a21 * (x[i] + h * k3x) * (y[i] + h * k3y) - a22 * (y[i] + h * k3y)
    
    x[i+1] = x[i] + (h/6) * (k1x + 2*k2x + 2*k3x + k4x)
    y[i+1] = y[i] + (h/6) * (k1y + 2*k2y + 2*k3y + k4y)

# Крок 5: Виведення результатів (таблиця перших 10 значень)
print(f"{Fore.CYAN}=== Крок 5: Результати обчислень (перші 10 значень) ===\n{Style.RESET_ALL}")
table_results = [["Час (t)", "Метелики (x)", "Павуки (y)"]]
for i in range(min(10, n_steps)):
    table_results.append([f"{t[i]:.1f}", f"{x[i]:.2f}", f"{y[i]:.2f}"])
print(tabulate(table_results, headers="firstrow", tablefmt="grid"))
print("\n")

# Крок 6: Побудова графіків
print(f"{Fore.CYAN}=== Крок 6: Побудова графіків ===\n{Style.RESET_ALL}")
plt.figure(figsize=(12, 8))

# Графік x(t) і y(t)
plt.subplot(2, 1, 1)
plt.plot(t, x, label='Метелики (x(t))', color='blue')
plt.plot(t, y, label='Павуки (y(t))', color='red')
plt.title('Динаміка чисельності метеликів і павуків з часом')
plt.xlabel('Час (дні)')
plt.ylabel('Чисельність')
plt.grid(True)
plt.legend()

# Графік y(x) (фазова траєкторія)
plt.subplot(2, 1, 2)
plt.plot(x, y, color='green')
plt.title('Фазова траєкторія y(x)')
plt.xlabel('Чисельність метеликів (x)')
plt.ylabel('Чисельність павуків (y)')
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"{Fore.GREEN}Готово! Графіки відображені для аналізу!{Style.RESET_ALL}")