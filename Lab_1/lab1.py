from colorama import init, Fore, Style
from tabulate import tabulate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Ініціалізація кольорів
init()

# Дані для 12-го варіанту
x1 = [0, 0, 0, 1, 1, 2, 2, 2]  # Вхід x1
x2 = [1.5, 2.5, 3.5, 1.5, 3.5, 1.5, 2.5, 2.5]  # Вхід x2
y = [2.3, 7.6, 0.8, 2.6, 1.6, 8.5, 5.3, 7.2]  # Вихід y
n = len(x1)  # Кількість точок

# Функція для обчислення суми списку
def my_sum(lst):
    total = 0
    for num in lst:
        total += num
    return total

# Функція для обчислення суми добутків двох списків
def my_sum_product(lst1, lst2):
    total = 0
    for i in range(len(lst1)):
        total += lst1[i] * lst2[i]
    return total

# Функція для обчислення суми квадратів списку
def my_sum_squares(lst):
    total = 0
    for num in lst:
        total += num ** 2
    return total

# Крок 1: Виводимо вхідні дані у таблиці
print(f"{Fore.CYAN}\n\n=== Крок 1: Вхідні дані ===\n{Style.RESET_ALL}")
table_data = [["#", "x1", "x2", "y"]]
for i in range(n):
    table_data.append([i+1, x1[i], x2[i], y[i]])
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
print(f"\nКількість точок (n): {n}\n")

# Крок 2: Обчислюємо всі суми "вручну"
print(f"{Fore.CYAN}\n=== Крок 2: Обчислюємо суми для методу найменших квадратів ===\n{Style.RESET_ALL}")
sum_x1 = my_sum(x1)
sum_x2 = my_sum(x2)
sum_y = my_sum(y)
sum_x1_sq = my_sum_squares(x1)
sum_x2_sq = my_sum_squares(x2)
sum_x1_x2 = my_sum_product(x1, x2)
sum_x1_y = round(my_sum_product(x1, y), 2)
sum_x2_y = round(my_sum_product(x2, y), 2)

# Виводимо суми з поясненнями
print(f"{Fore.YELLOW}Суми:{Style.RESET_ALL}\n")
print(f"(сума всіх x1) {Style.BRIGHT}Σx1 = {sum_x1}{Style.RESET_ALL}")
print(f"(сума всіх x2) {Style.BRIGHT}Σx2 = {sum_x2}{Style.RESET_ALL}")
print(f"(сума всіх y)  {Style.BRIGHT}Σy = {sum_y}{Style.RESET_ALL}\n")
print(f"(сума квадратів x1) {Style.BRIGHT}Σx1² = {sum_x1_sq}{Style.RESET_ALL}")
print(f"(сума квадратів x2) {Style.BRIGHT}Σx2² = {sum_x2_sq}{Style.RESET_ALL}\n")
print(f"(сума добутків x1 і x2) {Style.BRIGHT}Σx1*x2 = {sum_x1_x2}{Style.RESET_ALL}")
print(f"(сума добутків x1 і y)  {Style.BRIGHT}Σx1*y = {sum_x1_y}{Style.RESET_ALL}")
print(f"(сума добутків x2 і y)  {Style.BRIGHT}Σx2*y = {sum_x2_y}{Style.RESET_ALL}\n")

# Крок 3: Складаємо систему рівнянь
print(f"\n{Fore.CYAN}=== Крок 3: Складаємо систему рівнянь ==={Style.RESET_ALL}\n")

# Виведення загальної системи рівнянь
print(f"{Fore.YELLOW}Загальна система рівнянь (згідно методу найменших квадратів):{Style.RESET_ALL}")
print(f"""
╭──────────────────────────────────────────────────╮
│   ∂S      n                                      │
│   ─── = 2∑ (a₀ + a₁·x₁ᵢ + a₂·x₂ᵢ - yᵢ)·1   = 0   │
│   ∂a₀     i=1                                    │
│                                                  │
│   ∂S      n                                      │
│   ─── = 2∑ (a₀ + a₁·x₁ᵢ + a₂·x₂ᵢ - yᵢ)·x₁ᵢ = 0   │
│   ∂a₁     i=1                                    │
│                                                  │
│   ∂S       n                                     │
│   ─── = 2∑ (a₀ + a₁·x₁ᵢ + a₂·x₂ᵢ - yᵢ)·x₂ᵢ = 0   │
│   ∂a₂     i=1                                    │
╰──────────────────────────────────────────────────╯
""")

# Виведення числової системи рівнянь з округленням і форматуванням
print(f"{Fore.YELLOW}Числова система рівнянь:{Style.RESET_ALL}\n")
print(f"{Style.BRIGHT}1){Style.RESET_ALL}  {n:>4}*a₀ + {sum_x1:>4}*a₁ + {sum_x2:>5.1f}*a₂  = {sum_y:.2f}")
print(f"{Style.BRIGHT}2){Style.RESET_ALL}  {sum_x1:>4}*a₀ + {sum_x1_sq:>4}*a₁ + {sum_x1_x2:>5.1f}*a₂  = {sum_x1_y:.2f}")
print(f"{Style.BRIGHT}3){Style.RESET_ALL}  {sum_x2:>5.1f}*a₀ + {sum_x1_x2:>5.1f}*a₁ + {sum_x2_sq:>5.1f}*a₂  = {sum_x2_y:.2f}\n")

# Крок 4: Розв’язуємо систему "вручну" (метод Гаусса спрощений)
print(f"\n{Fore.CYAN}=== Крок 4: Розв’язуємо систему вручну ==={Style.RESET_ALL}\n")
print(f"{Fore.YELLOW}Система:{Style.RESET_ALL}")
print(f"{Style.BRIGHT}1){Style.RESET_ALL} 8a₀ + 8a₁ + 19a₂ = 35.9")
print(f"{Style.BRIGHT}2){Style.RESET_ALL} 8a₀ + 14a₁ + 18a₂ = 46.2")
print(f"{Style.BRIGHT}3){Style.RESET_ALL} 19a₀ + 18a₁ + 50.25a₂ = 78.75\n")

# Виключаємо a0 із 2-го і 1-го
print(f"{Fore.YELLOW}Виключаємо a₀ з рівнянь 2 і 1:{Style.RESET_ALL}")
print("Рівняння 2 - Рівняння 1:")
print(f"(8a₀ + 14a₁ + 18a₂) - (8a₀ + 8a₁ + 19a₂) = 46.2 - 35.9")
print(f"{Style.BRIGHT}6a₁ - a₂ = 10.3  (Рівняння A){Style.RESET_ALL}\n")

# Виключаємо a0 із 3-го і 1-го
print(f"{Fore.YELLOW}Виключаємо a₀ з рівнянь 3 і 1:{Style.RESET_ALL}")
print("Рівняння 1 * 19: 152a₀ + 152a₁ + 361a₂ = 682.1")
print("Рівняння 3 * 8: 152a₀ + 144a₁ + 402a₂ = 630.0")
print("Рівняння 1*19 - Рівняння 3*8:")
print(f"(152a₀ + 152a₁ + 361a₂) - (152a₀ + 144a₁ + 402a₂) = 682.1 - 630.0")
print(f"{Style.BRIGHT}8a₁ - 41a₂ = 52.1  (Рівняння B){Style.RESET_ALL}\n")

# Розв’язуємо два рівняння
print(f"{Fore.YELLOW}Розв’язуємо систему з двох рівнянь:{Style.RESET_ALL}")
print(f"{Style.BRIGHT}A){Style.RESET_ALL} 6a₁ - a₂ = 10.3")
print(f"{Style.BRIGHT}B){Style.RESET_ALL} 8a₁ - 41a₂ = 52.1")
print("З (A): a₂ = 6a₁ - 10.3")
print("Підставимо в (B): 8a₁ - 41(6a₁ - 10.3) = 52.1")
print("8a₁ - 246a₁ + 422.3 = 52.1")
print("-238a₁ + 422.3 = 52.1")
print("-238a₁ = 52.1 - 422.3")
print("-238a₁ = -370.2")
a1 = 370.2 / 238
print(f"a₁ = 370.2 / 238 = {a1:.4f}")
a2 = 6 * a1 - 10.3
print(f"a₂ = 6 * {a1:.4f} - 10.3 = {a2:.4f}")

# Знаходимо a0
print(f"\n{Fore.YELLOW}Знаходимо a₀:{Style.RESET_ALL}")
print(f"Підставимо a₁ і a₂ в перше рівняння:")
print(f"8a₀ + 12.444 + 19 * {a2:.4f} = 35.9")
a0_temp = 8 * a1 + 19 * a2
print(f"8a₀ + {a0_temp:.4f} = 35.9")
a0 = (35.9 - a0_temp) / 8
print(f"8a₀ = {35.9 - a0_temp:.4f}")
print(f"a₀ = {35.9 - a0_temp:.4f} / 8 = {a0:.4f}")

print(f"\n{Fore.GREEN}Знайдені коефіцієнти:{Style.RESET_ALL}")
print(f"a₀ = {a0:.4f} (базове значення)")
print(f"a₁ = {a1:.4f} (вплив x₁)")
print(f"a₂ = {a2:.4f} (вплив x₂)")
print(f"\n{Style.BRIGHT}Формула: y = {a0:.4f} + {a1:.4f}x₁ + {a2:.4f}x₂{Style.RESET_ALL}\n")

# Крок 5: Значення в точці (1.5, 3)
print(f"\n{Fore.CYAN}=== Крок 5: Рахуємо y для (x1 = 1.5, x2 = 3) ==={Style.RESET_ALL}\n")
x1_test = 1.5
x2_test = 3
y_test = a0 + a1 * x1_test + a2 * x2_test
print(f"y({x1_test}, {x2_test}) = {a0:.2f} + {a1:.2f}*{x1_test} + {a2:.2f}*{x2_test} = {Style.BRIGHT}{y_test:.2f}{Style.RESET_ALL}\n")

# Крок 6: Коефіцієнт детермінації R^2
print(f"\n{Fore.CYAN}=== Крок 6: Рахуємо коефіцієнт детермінації R² ==={Style.RESET_ALL}\n")
y_pred = []
for i in range(n):
    pred = a0 + a1 * x1[i] + a2 * x2[i]
    y_pred.append(pred)

# Таблиця порівняння реальних і передбачених y
table_pred = [["#", "x1", "x2", "Реальне y", "Передбачене y"]]
for i in range(n):
    table_pred.append([i+1, x1[i], x2[i], y[i], round(y_pred[i], 2)])
print(f"{Fore.YELLOW}Порівняння реальних і передбачених значень:{Style.RESET_ALL}")
print(tabulate(table_pred, headers="firstrow", tablefmt="grid"))

# Обчислення R^2
y_mean = sum_y / n

# Обчислення SS_res
ss_res = 0
for i in range(n):
    diff = y_pred[i] - y[i]
    ss_res += diff ** 2

# Обчислення SS_tot
ss_tot = 0
for i in range(n):
    diff = y_mean - y[i]
    ss_tot += diff ** 2

# Середнє значення y
print(f"\n{Fore.YELLOW}Середнє значення y:{Style.RESET_ALL}")
print(f"  Сума всіх y: Σy = {sum_y}")
print(f"  Кількість точок: n = {n}")
print(f"  Середнє значення y = Σy / n = {sum_y} / {n} = {y_mean:.2f}\n")

# Сума квадратів залишків (SS_res)
print(f"{Fore.YELLOW}Сума квадратів залишків (SS_res):{Style.RESET_ALL}")
for i in range(n):
    print(f"  (y_pred_{i+1} - y_{i+1})² = ({y_pred[i]:.2f} - {y[i]:.2f})² = {(y_pred[i] - y[i])**2:.4f}")
print(f"\n  SS_res = {ss_res:.4f}\n")

# Сума квадратів загальної варіації (SS_tot)
print(f"{Fore.YELLOW}Сума квадратів загальної варіації (SS_tot):{Style.RESET_ALL}")
for i in range(n):
    print(f"  (y_mean - y_{i+1})² = ({y_mean:.2f} - {y[i]:.2f})² = {(y_mean - y[i])**2:.4f}")
print(f"\n  SS_tot = {ss_tot:.4f}\n")

# Обчислення R^2
R2 = 1 - ss_res / ss_tot

print(f"""
╭──────────────────────────────╮
│         𝑛                    │
│        ∑  (ŷᵢ - yᵢ)²         |
│         i=1                  |
│   1 -  ────────────────      │
│         𝑛                    │
│        ∑  (ȳ - yᵢ)²          |
│         i=1                  │
│                              │
│   {Style.BRIGHT}Формула для обчислення R²{Style.RESET_ALL}  │
╰──────────────────────────────╯
""")

print(f"R² = 1 - ({ss_res:.4f} / {ss_tot:.4f}) = {R2:.3f}")
print(f"\n{Fore.GREEN}{Style.BRIGHT}Коефіцієнт детермінації R² = {R2:.3f}{Style.RESET_ALL} \n(чим ближче до 1, то краще формула описує дані)\n")

# Крок 7: Виведення інтерактивних графіків
print(f"\n{Fore.CYAN}=== Крок 7: Виведення інтерактивних графіків ==={Style.RESET_ALL}\n")

# 3D-графік
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x1, x2, y, color='red', label='Експериментальні дані', s=100)

# Створюємо сітку для апроксимаційної поверхні
x1_range = [0, 1, 2]
x2_range = [1.5, 2.5, 3.5]
X1, X2 = [], []
Y = []
for x1_val in x1_range:
    for x2_val in x2_range:
        X1.append(x1_val)
        X2.append(x2_val)
        Y.append(a0 + a1 * x1_val + a2 * x2_val)
ax.plot_trisurf(X1, X2, Y, color='blue', alpha=0.5, label='Апроксимаційна поверхня')

ax.set_xlabel('x₁')
ax.set_ylabel('x₂')
ax.set_zlabel('y')
ax.set_title(f'y = {a0:.2f} + {a1:.2f}x₁ + {a2:.2f}x₂')
ax.legend()

plt.show()

print(f"{Fore.GREEN}Готово! Графіки відображені для інтерактивного аналізу!{Style.RESET_ALL}")