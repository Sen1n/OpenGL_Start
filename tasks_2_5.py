import os
import sys
import numpy as np
# ХАК ДЛЯ MICROSOFT STORE: Примусово вказуємо шляхи до Tcl/Tk
os.environ['TCL_LIBRARY'] = r'D:\python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\python\tcl\tk8.6'
os.environ['MPLBACKEND'] = 'Agg'

current_dir = os.path.dirname(os.path.abspath(__file__))
engine_src_path = os.path.join(current_dir, 'GraphicEngine2D')
if engine_src_path not in sys.path:
    sys.path.insert(0, engine_src_path)

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Vec3 import vertex

# Базові вершини квадрата (0,0) - (1,1)
vertices = np.array([
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 1, 1, 1]
], dtype=float)

def make_scene(title, rect, animations, filename):
    class CustomScene(AnimatedScene):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            poly = Polygon(0, 0, 1, 0, 1, 1, 0, 1)
            poly["color"] = "blue"
            poly.show_local_frame()
            self["square"] = poly

    scene = CustomScene(
        image_size=(6, 6), coordinate_rect=rect, title=title,
        axis_show=True, axis_color=("red", "green"), keep_aspect_ratio=True
    )
    for anim in animations:
        scene.add_animation(anim)
    
    scene.figure.savefig(os.path.join(current_dir, filename), dpi=200)
    print(f"[УСПІХ] Збережено графік: {filename}")

# --- ЗАВДАННЯ 2 ---
print("=== ЗАВДАННЯ 2 ===")
S2 = np.array([[2, 0, 0], [0, 1, 0], [0, 0, 1]]) # Розтяг по х в 2 рази
a2 = np.radians(45)
R2 = np.array([[np.cos(a2), -np.sin(a2), 0], [np.sin(a2), np.cos(a2), 0], [0, 0, 1]])
M2 = R2 @ S2
print("Матриця трансформації M2 (R * S):\n", np.round(M2, 3))
print("Фінальні координати:\n", np.round(M2 @ vertices, 3))

make_scene(
    "Task 2: Scale X (2) -> Rotate 45", (-2, -1, 4, 4),
    [ScaleAnimation(end=(2, 1), frames=1, channel="square"), RotationAnimation(end=np.radians(45), frames=1, channel="square")],
    "task_2_result.png"
)

# --- ЗАВДАННЯ 3 ---
print("\n=== ЗАВДАННЯ 3 ===")
a3 = np.radians(90)
R3 = np.array([[np.cos(a3), -np.sin(a3), 0], [np.sin(a3), np.cos(a3), 0], [0, 0, 1]])
T3 = np.array([[1, 0, 2], [0, 1, 3], [0, 0, 1]])
M3 = T3 @ R3
print("Матриця трансформації M3 (T * R):\n", np.round(M3, 3))
print("Фінальні координати:\n", np.round(M3 @ vertices, 3))

make_scene(
    "Task 3: Rotate 90 -> Translation (2,3)", (-2, -1, 5, 6),
    [RotationAnimation(end=np.radians(90), frames=1, channel="square"), TranslationAnimation(end=vertex(2, 3), frames=1, channel="square")],
    "task_3_result.png"
)

# --- ЗАВДАННЯ 4 ---
print("\n=== ЗАВДАННЯ 4 ===")
S4 = np.array([[1, 0, 0], [0, 3, 0], [0, 0, 1]]) # Розтяг по у в 3 рази
a4 = np.radians(60)
R4 = np.array([[np.cos(a4), -np.sin(a4), 0], [np.sin(a4), np.cos(a4), 0], [0, 0, 1]])
M4 = R4 @ S4
print("Матриця трансформації M4 (R * S):\n", np.round(M4, 3))
print("Фінальні координати:\n", np.round(M4 @ vertices, 3))

make_scene(
    "Task 4: Scale Y (3) -> Rotate 60", (-3, -1, 4, 5),
    [ScaleAnimation(end=(1, 3), frames=1, channel="square"), RotationAnimation(end=np.radians(60), frames=1, channel="square")],
    "task_4_result.png"
)

# --- ЗАВДАННЯ 5 ---
print("\n=== ЗАВДАННЯ 5 ===")
T5 = np.array([[1, 0, 1], [0, 1, -1], [0, 0, 1]])
S5 = np.array([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
M5 = S5 @ T5
print("Матриця трансформації M5 (S * T):\n", np.round(M5, 3))
print("Фінальні координати:\n", np.round(M5 @ vertices, 3))

make_scene(
    "Task 5: Translation (1,-1) -> Scale (2)", (-1, -3, 5, 3),
    [TranslationAnimation(end=vertex(1, -1), frames=1, channel="square"), ScaleAnimation(end=(2, 2), frames=1, channel="square")],
    "task_5_result.png"
)