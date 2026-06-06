import numpy as np

print("\n=== ЗАВДАННЯ 11 ===")
T11 = np.array([
    [2.934, -0.416, 2.000],
    [0.624,  1.956, 3.400],
    [0.000,  0.000, 1.000]
])

T11_inv = np.linalg.inv(T11)
print("Матриця зворотної трансформації T^(-1):\n", np.round(T11_inv, 3))

transformed_points = np.array([
    [2, 4.9, 4.5, 1.6],
    [3.4, 4, 6, 5.4],
    [1, 1, 1, 1]
])
original_points = T11_inv @ transformed_points
print("Відновлені початкові координати в ЛСК:\n", np.round(original_points[:2, :], 3))


print("\n=== ЗАВДАННЯ 12 ===")
T12 = np.array([
    [0.866, 0.5,   4.0],
    [-0.5,  0.866, 3.0],
    [0.0,   0.0,   1.0]
])
tx12, ty12 = T12[0,2], T12[1,2]
sx12 = np.sqrt(T12[0,0]**2 + T12[1,0]**2)
sy12 = np.sqrt(T12[0,1]**2 + T12[1,1]**2)
angle12 = np.degrees(np.arctan2(T12[1,0]/sx12, T12[0,0]/sx12))

print(f"Компоненти розкладу TRS:\nПереміщення: tx={tx12}, ty={ty12}")
print(f"Масштабування: sx={round(sx12, 1)}, sy={round(sy12, 1)}")
print(f"Кут повороту: {round(angle12, 1)} градусів")


print("\n=== ЗАВДАННЯ 13 ===")
T13 = np.array([
    [1.414, -2.121, 1.0],
    [1.414,  2.121, 1.0],
    [0.0,    0.0,   1.0]
])
tx13, ty13 = T13[0,2], T13[1,2]
sx13 = np.sqrt(T13[0,0]**2 + T13[1,0]**2)
sy13 = np.sqrt(T13[0,1]**2 + T13[1,1]**2)
angle13 = np.degrees(np.arctan2(T13[1,0]/sx13, T13[0,0]/sx13))

print(f"Компоненти розкладу TRS:\nПереміщення: tx={tx13}, ty={ty13}")
print(f"Масштабування: sx={round(sx13, 1)}, sy={round(sy13, 1)}")
print(f"Кут повороту: {round(angle13, 1)} градусів")


print("\n=== ЗАВДАННЯ 14 (Опорна точка (1,1)) ===")
T14_pivot = np.array([
    [1.732, -1.0,   5.0],
    [1.0,    1.732, -3.0],
    [0.0,    0.0,   1.0]
])
px, py = 1.0, 1.0

T_minus = np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
T_plus = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]])

TRS_pure = T_minus @ T14_pivot @ T_plus
print("Ізольована TRS матриця без впливу pivot:\n", np.round(TRS_pure, 3))

tx14, ty14 = TRS_pure[0,2], TRS_pure[1,2]
sx14 = np.sqrt(TRS_pure[0,0]**2 + TRS_pure[1,0]**2)
sy14 = np.sqrt(TRS_pure[0,1]**2 + TRS_pure[1,1]**2)
angle14 = np.degrees(np.arctan2(TRS_pure[1,0]/sx14, TRS_pure[0,0]/sx14))

print(f"\nКомпоненти внутрішнього розкладу TRS:")
print(f"Переміщення: tx={round(tx14,1)}, ty={round(ty14,1)}")
print(f"Масштабування: sx={round(sx14,1)}, sy={round(sy14,1)}")
print(f"Кут повороту: {round(angle14,1)} градусів навколо опорної точки")