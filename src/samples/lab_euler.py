import numpy as np
import sympy as sp

def get_scale_matrix(sx, sy, sz):
    return np.array([
        [sx, 0,  0,  0],
        [0,  sy, 0,  0],
        [0,  0,  sz, 0],
        [0,  0,  0,  1]
    ])

def get_translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def get_rotation_x(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [1, 0,  0, 0],
        [0, c, -s, 0],
        [0, s,  c, 0],
        [0, 0,  0, 1]
    ])

def get_rotation_y(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1]
    ])

def get_rotation_z(deg):
    rad = np.radians(deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1]
    ])

cube_vertices = np.array([
    [0, 1, 1, 0, 0, 1, 1, 0], # X
    [0, 0, 1, 1, 0, 0, 1, 1], # Y
    [0, 0, 0, 0, 1, 1, 1, 1], # Z
    [1, 1, 1, 1, 1, 1, 1, 1]  # W
])

def print_vertices(vertices_matrix, label):
    print(f"--- {label} ---")
    for i in range(8):
        v = vertices_matrix[:, i]
        print(f"Вершина {i+1}: ({v[0]:.2f}, {v[1]:.2f}, {v[2]:.2f})")
    print()

def solve_task_1():
    print("=== ЗАВДАННЯ 1: Розтяг, обертання (Euler XYZ) і зсув ===")
    S = get_scale_matrix(2, 0.5, 1)
    Rx = get_rotation_x(30)
    Ry = get_rotation_y(45)
    Rz = get_rotation_z(60)
    R = Rz @ Ry @ Rx
    T = get_translation_matrix(-3, 2, 5)
    M = T @ R @ S
    print("Фінальна матриця трансформації M:\n", np.round(M, 3))
    final_vertices = M @ cube_vertices
    print_vertices(final_vertices, "Фінальне положення куба (Завдання 1)")

def solve_task_2():
    print("=== ЗАВДАННЯ 2: Поворот у системі кутів Ейлера ZYX ===")
    Rz = get_rotation_z(20)
    Ry = get_rotation_y(35)
    Rx = get_rotation_x(50)
    R = Rx @ Ry @ Rz
    T = get_translation_matrix(1, 3, -2)
    M = T @ R
    print("Фінальна матриця трансформації M:\n", np.round(M, 3))
    final_vertices = M @ cube_vertices
    print_vertices(final_vertices, "Фінальне положення куба (Завдання 2)")


def solve_task_3():
    print("=== ЗАВДАННЯ 3: Конвенції та послідовність обертань ===")
    
    # Кути: alpha (X) = 45, beta (Y) = 30, gamma (Z) = 60
    Rx = get_rotation_x(45)
    Ry = get_rotation_y(30)
    Rz = get_rotation_z(60)
    
    # 1. Конвенція XYZ (зовнішні осі). Математично множення йде справа наліво:
    # v' = Rz * Ry * Rx * v
    R_xyz = Rz @ Ry @ Rx
    
    # 2. Конвенція ZYX (зовнішні осі).
    # v' = Rx * Ry * Rz * v
    R_zyx = Rx @ Ry @ Rz
    
    print("Матриця конвенції XYZ:")
    print(np.round(R_xyz, 3))
    print("\nМатриця конвенції ZYX:")
    print(np.round(R_zyx, 3))
    
    # Застосуємо до однієї вершини куба (наприклад, (1,1,1))
    v = np.array([1, 1, 1, 1])
    print(f"\nВершина (1,1,1) після XYZ: {np.round(R_xyz @ v, 3)[:3]}")
    print(f"Вершина (1,1,1) після ZYX: {np.round(R_zyx @ v, 3)[:3]}")
    
    print("\nВисновок: Матричне множення не є комутативним (A*B != B*A).")
    print("Тому послідовність застосування поворотів критично впливає на фінальну орієнтацію.")
    print("Обертання куба навколо X, потім Y, потім Z дасть інший результат, ніж Z, потім Y, потім X.\n")

def solve_task_4():
    print("=== ЗАВДАННЯ 4: Математичне виведення Gimbal Lock (через SymPy) ===")
    
    # Визначаємо символьні змінні для кутів
    alpha, beta, gamma = sp.symbols('alpha beta gamma')
    
    Rx = sp.Matrix([
        [1, 0, 0],
        [0, sp.cos(alpha), -sp.sin(alpha)],
        [0, sp.sin(alpha),  sp.cos(alpha)]
    ])
    
    Ry = sp.Matrix([
        [sp.cos(beta), 0, sp.sin(beta)],
        [0, 1, 0],
        [-sp.sin(beta), 0, sp.cos(beta)]
    ])
    
    Rz = sp.Matrix([
        [sp.cos(gamma), -sp.sin(gamma), 0],
        [sp.sin(gamma),  sp.cos(gamma), 0],
        [0, 0, 1]
    ])
    
    R = Rz * Ry * Rx
    print("\n1. Загальна матриця R (до підстановки):")
    print("Матриця занадто велика для виводу, але вона містить добутки sin та cos усіх трьох кутів.")
    
    # 2. Підставляємо beta = 90 градусів (pi/2)
    R_gimbal = R.subs(beta, sp.pi / 2)
    

    R_simplified = sp.simplify(R_gimbal)
    
    print("\n2-3. Фінальна спрощена матриця після підстановки beta = 90° (pi/2):")
    # pprint виводить матрицю у красивому математичному (псевдографічному) вигляді
    sp.pprint(R_simplified)

    print("\n4. Математичний висновок:")
    print("Як бачимо з отриманої матриці, кути alpha та gamma згрупувалися у єдиний аргумент (alpha - gamma).")
    print("Це математично доводить, що при beta = 90° система втрачає один ступінь вільності,")
    print("оскільки зміна кута alpha дає абсолютно той самий ефект, що й протилежна зміна кута gamma.")

def solve_task_5():
    print("=== ЗАВДАННЯ 5: Практичний експеримент «Втрачена вісь» ===")
    
    # 1. Базові кути: X = 30, Y = 90, Z = 45
    Rx1 = get_rotation_x(30)
    Ry1 = get_rotation_y(90)
    Rz1 = get_rotation_z(45)
    R1 = Rz1 @ Ry1 @ Rx1  # Конвенція XYZ
    
    v1 = R1 @ cube_vertices
    
    # 2. Змінюємо кути: X + 10 (стає 40), Z - 10 (стає 35). Y залишається 90.
    Rx2 = get_rotation_x(40)
    Ry2 = get_rotation_y(90)
    Rz2 = get_rotation_z(35)
    R2 = Rz2 @ Ry2 @ Rx2
    
    v2 = R2 @ cube_vertices
    
    print("Матриця повороту 1 (X=30, Y=90, Z=45):")
    print(np.round(R1, 3))
    print("\nМатриця повороту 2 (X=40, Y=90, Z=35):")
    print(np.round(R2, 3))
    
    # 3. Доведення незмінності положення
    diff = np.max(np.abs(v1 - v2))
    print(f"\nМаксимальна різниця між координатами вершин куба: {diff:.5f}")
    if diff < 1e-6:
        print("Висновок: Фінальне положення куба в просторі залишилося абсолютно незмінним!")
        print("Це наочно демонструє «склеювання» осей X та Z при Y=90 (Gimbal Lock).")
        print("Зміна по осі X була повністю компенсована зворотною зміною по осі Z.\n")


def solve_task_6():
    print("=== ЗАВДАННЯ 6: Проблема інтерполяції в зоні сингулярності ===")
    
    start_angles = np.array([0.0, 0.0, 0.0])
    end_angles = np.array([90.0, 90.0, 90.0])
    steps = 10
    
    # Вектор, який дивиться "вперед"
    v_forward = np.array([0, 0, 1, 1])
    
    print("Траєкторія вектора погляду (0, 0, 1) при лінійній інтерполяції кутів:")
    for i in range(steps + 1):
        t = i / steps

        angles = start_angles + t * (end_angles - start_angles)
        
        Rx = get_rotation_x(angles[0])
        Ry = get_rotation_y(angles[1])
        Rz = get_rotation_z(angles[2])
        R = Rz @ Ry @ Rx
        
        v_out = R @ v_forward
        print(f"Крок {i:2d} (t={t:.1f}): Кути ({angles[0]:.0f}, {angles[1]:.0f}, {angles[2]:.0f}) -> "
              f"Вектор ({v_out[0]:5.2f}, {v_out[1]:5.2f}, {v_out[2]:5.2f})")



def solve_task_7():
    print("=== ЗАВДАННЯ 7: Декомпозиція та неоднозначність розв'язку ===")
    

    R_target = get_rotation_z(45) @ get_rotation_y(90) @ get_rotation_x(30)
    
    print("Вхідна матриця R (з Gimbal Lock):")
    print(np.round(R_target, 3))
    

    sy = R_target[0, 2] 
    
    if np.isclose(sy, 1.0):
        print("\nАлгоритм виявив Gimbal Lock (sin(Y) = 1, отже Y = 90°).")
        print("Через склеювання осей існує нескінченна кількість комбінацій (X, Z).")
        

        x_angle_stable = 0.0
        y_angle_stable = 90.0
        

        z_rad = np.arctan2(R_target[1, 0], R_target[1, 1])
        z_angle_stable = np.degrees(z_rad)
        
        print(f"Стабільний розв'язок (X примусово 0): X={x_angle_stable:.1f}°, Y={y_angle_stable:.1f}°, Z={z_angle_stable:.1f}°")
        
        # Перевіримо, чи дають ці нові кути ту саму матрицю
        R_check = get_rotation_z(z_angle_stable) @ get_rotation_y(y_angle_stable) @ get_rotation_x(x_angle_stable)
        
        diff = np.max(np.abs(R_target - R_check))
        print(f"Похибка між вихідною та новою матрицею: {diff:.5e}")
        if diff < 1e-6:
            print("знайшли інший набір кутів, який дає абсолютно ідентичний поворот")


if __name__ == "__main__":
    solve_task_1()
    solve_task_2()
    solve_task_3()
    solve_task_4()
    solve_task_6()
    solve_task_5()
    solve_task_7()