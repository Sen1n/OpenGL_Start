import os
import sys
import numpy as np
# ХАК ДЛЯ MICROSOFT STORE: Примусово вказуємо шляхи до Tcl/Tk
os.environ['TCL_LIBRARY'] = r'D:\python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\python\tcl\tk8.6'
os.environ['MPLBACKEND'] = 'Agg'

current_dir = os.path.dirname(os.path.abspath(__file__))
engine_src_path = os.path.join(current_dir, 'GraphicEngine2D')
sys.path.insert(0, engine_src_path)

from src.engine.model.Polygon import Polygon
from src.engine.scene.Scene import Scene # використовуємо статичну сцену без анімацій

vertices = np.array([[0,1,1,0],[0,0,1,1],[1,1,1,1]], dtype=float)

def get_pivot_sandwich(matrix_local, px, py):
    T_to_origin = np.array([[1, 0, -px], [0, 1, -py], [0, 0, 1]])
    T_back = np.array([[1, 0, px], [0, 1, py], [0, 0, 1]])
    return T_back @ matrix_local @ T_to_origin

# --- ЗАВДАННЯ 7 ---
print("=== ЗАВДАННЯ 7 (Поворот навколо різних Pivot) ===")
pivots_7 = [(0.5, 0.5), (0.0, 1.0), (1.0, 1.0), (2.0, 2.0)]
a7 = np.radians(60)
R7_local = np.array([[np.cos(a7), -np.sin(a7), 0], [np.sin(a7), np.cos(a7), 0], [0, 0, 1]])

for idx, (px, py) in enumerate(pivots_7):
    M7 = get_pivot_sandwich(R7_local, px, py)
    res = M7 @ vertices
    print(f"Pivot ({px}, {py}) - Фінальні точки:\n", np.round(res[:2, :], 3))

# --- ЗАВДАННЯ 8 ---
print("\n=== ЗАВДАННЯ 8 (Розтяг навколо різних Pivot) ===")
S8_local = np.array([[2, 0, 0], [0, 3, 0], [0, 0, 1]])

for idx, (px, py) in enumerate(pivots_7):
    M8 = get_pivot_sandwich(S8_local, px, py)
    res = M8 @ vertices
    print(f"Pivot ({px}, {py}) - Фінальні точки:\n", np.round(res[:2, :], 3))

# --- ЗАВДАННЯ 10 (Складне масштабування, обертання та зсув) ---
print("\n=== ЗАВДАННЯ 10 ===")
px, py = 0.5, 0.5
S10 = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
a10 = np.radians(30)
R10 = np.array([[np.cos(a10), -np.sin(a10), 0], [np.sin(a10), np.cos(a10), 0], [0, 0, 1]])
# Матриця зсув (Shear) на вектор (1, -1)
H10 = np.array([[1, 1, 0], [-1, 1, 0], [0, 0, 1]])

# Порядок: Масштабування -> Обертання -> Зсув відносно центру
M10_local = H10 @ R10 @ S10
M10_final = get_pivot_sandwich(M10_local, px, py)
print("Загальна матриця Завдання 10:\n", np.round(M10_final, 3))
print("Координати вершин:\n", np.round(M10_final @ vertices, 3))

# Створюємо статичний графік для демонстрації Завдання 10
scene = Scene(image_size=(6,6), coordinate_rect=(-3,-3,5,5), title="Task 10 Final Result", axis_show=True)
poly_orig = Polygon(0,0, 1,0, 1,1, 0,1)
poly_orig["color"] = "gray"
scene["orig"] = poly_orig

# Застосовуємо трансформацію вручну до вершин для відображення результату
fv = M10_final @ vertices
poly_trans = Polygon(fv[0,0], fv[1,0], fv[0,1], fv[1,1], fv[0,2], fv[1,2], fv[0,3], fv[1,3])
poly_trans["color"] = "red"
scene["transformed"] = poly_trans

scene.figure.savefig(os.path.join(current_dir, "task_10_result.png"), dpi=200)
print("[УСПІХ] Збережено статичний графік для Завдання 10")