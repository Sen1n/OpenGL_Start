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

from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.animation.ScaleAnimation import ScaleAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Vec3 import vertex

vertices = np.array([[0,1,1,0],[0,0,1,1],[1,1,1,1]], dtype=float)

# Матриці компонент
S = np.array([[1, 0, 0], [0, 3, 0], [0, 0, 1]])
a = np.radians(60)
R = np.array([[np.cos(a), -np.sin(a), 0], [np.sin(a), np.cos(a), 0], [0, 0, 1]])
T = np.array([[1, 0, 2], [0, 1, 3], [0, 0, 1]])

print("=== ЗАВДАННЯ 6 ===")
# Порядок 1: S -> R -> T (Матриця: T * R * S)
M_order1 = T @ R @ S
print("Порядок 1 (S -> R -> T) Матриця:\n", np.round(M_order1, 3))
print("Порядок 1 Фінальні координати:\n", np.round(M_order1 @ vertices, 3))

# Порядок 2: T -> S -> R (Матриця: R * S * T)
M_order2 = R @ S @ T
print("\nПорядок 2 (T -> S -> R) Матриця:\n", np.round(M_order2, 3))
print("Порядок 2 Фінальні координати:\n", np.round(M_order2 @ vertices, 3))

# Візуалізуємо Порядок 1
class Scene6(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        poly = Polygon(0,0, 1,0, 1,1, 0,1)
        poly["color"] = "purple"
        self["square"] = poly

scene = Scene6(image_size=(6,6), coordinate_rect=(-3,-1,6,7), title="Task 6: Order S->R->T", axis_show=True)
scene.add_animation(ScaleAnimation(end=(1,3), frames=1, channel="square"))
scene.add_animation(RotationAnimation(end=np.radians(60), frames=1, channel="square"))
scene.add_animation(TranslationAnimation(end=vertex(2,3), frames=1, channel="square"))
scene.figure.savefig(os.path.join(current_dir, "task_6_result.png"), dpi=200)
print("[УСПІХ] Збережено графік порядку 1 для Завдання 6")