import numpy as np
import sys
import os

# Додаємо кореневу папку в sys.path, щоб імпорти працювали коректно
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.math.Quaternion import Quaternion
from src.math.Vec3 import Vec3

def solve_task_0():
    print("=== ЗАВДАННЯ 0 ===")
    
    # 1. Побудувати одиничний кватерніон
    # Кут 60 градусів переводимо в радіани
    theta = np.radians(60) 
    
    # Вісь u = (1, 1, 1). Метод rotation рушія сам її нормалізує до (1/√3, 1/√3, 1/√3)
    axis = Vec3(1, 1, 1) 
    
    q = Quaternion.rotation(theta, axis)
    print(f"1. Кватерніон q: {q}")
    
    # 2. Обчислити норму
    print(f"2. Норма |q|: {q.norm():.5f}")
    assert np.isclose(q.norm(), 1.0), "Норма не дорівнює 1!"
    
    # 3. Побудувати матрицю повороту
    R = q.toRotationMatrix()
    print("3. Матриця повороту R:")
    # Виводимо матрицю (викличе метод __str__ класу Mat4x4)
    print(R) 
    print()

def solve_task_1():
    print("=== ЗАВДАННЯ 1 ===")
    
    # Описуємо поворот навколо осі Z на 90 градусів
    theta = np.radians(90)
    q = Quaternion.rotation_z(theta)
    
    # 1. Записати точку p (1, 0, 0) як "чистий" кватерніон
    p = Vec3(1, 0, 0)
    v = Quaternion(p) # Твій конструктор автоматично зробить w=0
    print(f"1. Чистий кватерніон v: {v}")
    
    # 2. Виконати поворот: v' = q * v * q^-1
    # Використовуємо перевантажений оператор множення з твого класу
    v_prime = q * v * q.inverse()
    print(f"2. Кватерніон після повороту v': {v_prime}")
    
    # 3. Виділити векторну частину
    new_p = v_prime.toVec3()
    print(f"3. Нові координати вектора: ({new_p.x:.2f}, {new_p.y:.2f}, {new_p.z:.2f})")
    
    # Перевірка через готовий метод рушія
    check_p = q.rotate_vector(p)
    print(f"Перевірка вбудованим методом: ({check_p.x:.2f}, {check_p.y:.2f}, {check_p.z:.2f})")
    print()

def solve_task_2():
    print("=== ЗАВДАННЯ 2: Тетраедр ===")
    
    # 1. Створюємо кватерніони поворотів
    q1 = Quaternion.rotation_x(np.radians(45))
    q2 = Quaternion.rotation_y(np.radians(30))
    

    q_total = q2 * q1
    print(f"1. Результуючий кватерніон q_total: {q_total}")
    

    angle, axis = q_total.to_angle_axis()
    print(f"2. Сумарний кут повороту: {np.degrees(angle):.2f} градусів")
    print(f"   Сумарна вісь: ({axis.x:.3f}, {axis.y:.3f}, {axis.z:.3f})")
    

    vertices = [
        Vec3(0, 0, 0),
        Vec3(1, 0, 0),
        Vec3(0, 1, 0),
        Vec3(0, 0, 1)
    ]
    
    print("3. Нові координати вершин тетраедра:")
    for i, v in enumerate(vertices):
        # Використовуємо кватерніонну алгебру (метод rotate_vector робить q * v * q^-1)
        v_prime = q_total.rotate_vector(v)
        print(f"   Вершина {i} {v}: ({v_prime.x:.3f}, {v_prime.y:.3f}, {v_prime.z:.3f})")
    print()


def solve_task_3():
    print("=== ЗАВДАННЯ 3: Кути Ойлера та Gimbal Lock ===")
    
    # Кути переводимо в радіани
    yaw_z = np.radians(20)
    pitch_y = np.radians(90)
    roll_x = np.radians(50)
    
    # 1. Перетворюємо кожен поворот у кватерніон
    q_z = Quaternion.rotation_z(yaw_z)
    q_y = Quaternion.rotation_y(pitch_y)
    q_x = Quaternion.rotation_x(roll_x)
    
    print("1. Кватерніони осей:")
    print(f"   q_z (Yaw 20):   {q_z}")
    print(f"   q_y (Pitch 90): {q_y}")
    print(f"   q_x (Roll 50):  {q_x}")
    
    # 2. Обчислюємо фінальний кватерніон (порядок: Z * Y * X)
    q_final = q_z * q_y * q_x
    print(f"\n2. Фінальний кватерніон q = q_z * q_y * q_x:\n   {q_final}")
    
    # 3. Демонстрація відсутності Gimbal Lock
    angle, axis = q_final.to_angle_axis()
    print(f"\n3. Норма фінального кватерніона: {q_final.norm():.5f} (немає втрати точності)")
    print(f"   Орієнтація однозначно визначається поворотом на {np.degrees(angle):.2f} градусів")
    print(f"   навколо осі ({axis.x:.3f}, {axis.y:.3f}, {axis.z:.3f}).")
    print("   Сингулярності (ділення на нуль чи втрати ступеня свободи) не відбулося!\n")


def solve_task_4():
    print("=== ЗАВДАННЯ 4: Декомпозиція матриці в кватерніон ===")
    
    # Задана матриця повороту R
    R = np.array([
        [0, -1,  0],
        [1,  0,  0],
        [0,  0,  1]
    ])
    
    # Формула конвертації матриці 3x3 у кватерніон (коли слід матриці > 0)
    # Слід (Trace) - це сума діагональних елементів
    trace = R[0, 0] + R[1, 1] + R[2, 2]
    
    w = np.sqrt(1.0 + trace) / 2.0
    x = (R[2, 1] - R[1, 2]) / (4.0 * w)
    y = (R[0, 2] - R[2, 0]) / (4.0 * w)
    z = (R[1, 0] - R[0, 1]) / (4.0 * w)
    
    q = Quaternion(w, x, y, z)
    
    print("1. Компоненти кватерніона, вилучені з матриці R:")
    print(f"   {q}")
    print(f"   Норма: {q.norm():.5f}\n")


def solve_task_5():
    print("=== ЗАВДАННЯ 5: Повна декомпозиція афінної матриці ===")

    M = np.array([
        [0, -2,  0,   10],
        [1,  0,  0,  -5],
        [0,  0,  1.5,  3],
        [0,  0,  0,   1]
    ])
    

    T = M[0:3, 3]
    print(f"1. Вектор перенесення T (Трансляція): ({T[0]:.1f}, {T[1]:.1f}, {T[2]:.1f})")
    

    M3x3 = M[0:3, 0:3]

    s_x = np.linalg.norm(M3x3[:, 0])
    s_y = np.linalg.norm(M3x3[:, 1])
    s_z = np.linalg.norm(M3x3[:, 2])
    
    print(f"2. Коефіцієнти масштабування S: ({s_x:.1f}, {s_y:.1f}, {s_z:.1f})")
    
    R = np.zeros((3, 3))
    R[:, 0] = M3x3[:, 0] / s_x
    R[:, 1] = M3x3[:, 1] / s_y
    R[:, 2] = M3x3[:, 2] / s_z
    
    print("3. Чиста матриця обертання R:")
    print(R)
    
    I_check = np.dot(R, R.T)
    is_orthogonal = np.allclose(I_check, np.eye(3))
    print(f"   [Перевірка] Матриця R строго ортогональна? {'Так' if is_orthogonal else 'Ні'}")

    trace = R[0, 0] + R[1, 1] + R[2, 2]
    
    w = np.sqrt(1.0 + trace) / 2.0
    x = (R[2, 1] - R[1, 2]) / (4.0 * w)
    y = (R[0, 2] - R[2, 0]) / (4.0 * w)
    z = (R[1, 0] - R[0, 1]) / (4.0 * w)
    
    q = Quaternion(w, x, y, z)
    
    print("4. Результуючий одиничний кватерніон q:")
    print(f"   {q}")
    print(f"   Норма: {q.norm():.5f}\n")

if __name__ == "__main__":
    solve_task_0()
    solve_task_1()
    solve_task_2()
    solve_task_3()
    solve_task_4()
    solve_task_5()