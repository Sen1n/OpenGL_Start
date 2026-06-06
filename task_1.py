import os
import sys

# ХАК ДЛЯ MICROSOFT STORE: Примусово вказуємо шляхи до Tcl/Tk, які Windows не може знайти
os.environ['TCL_LIBRARY'] = r'D:\python\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\python\tcl\tk8.6'

# Про всяк випадок повністю відрізаємо створення інтерактивних вікон
os.environ['MPLBACKEND'] = 'Agg'

import numpy as np

# Автоматично знаходимо шлях до папки GraphicEngine2D та її підпапки src
current_dir = os.path.dirname(os.path.abspath(__file__))
engine_src_path = os.path.join(current_dir, 'GraphicEngine2D')

if engine_src_path not in sys.path:
    sys.path.insert(0, engine_src_path)

# Імпорти з рушія
from src.engine.animation.RotationAnimation import RotationAnimation
from src.engine.animation.TranslationAnimation import TranslationAnimation
from src.engine.model.Polygon import Polygon
from src.engine.scene.AnimatedScene import AnimatedScene
from src.math.Vec3 import vertex

FIGURE_KEY = "square"

def calculate_matrices_and_print():
    """Аналітична частина для звіту."""
    print("\n" + "="*40)
    print("=== ЗАВДАННЯ 1: Математичні розрахунки ===")
    print("="*40)
    
    vertices = np.array([
        [0, 1, 1, 0], # X
        [0, 0, 1, 1], # Y
        [1, 1, 1, 1]  # W
    ])
    print("Початкові координати квадрата:")
    print(vertices[:2, :])
    print("-" * 40)

    angle = np.radians(30)
    c, s = np.cos(angle), np.sin(angle)
    R = np.array([
        [c, -s, 0],
        [s,  c, 0],
        [0,  0, 1]
    ])
    print("Матриця повороту на 30°:")
    print(np.round(R, 3))
    
    T = np.array([
        [1, 0, 2],
        [0, 1, 3],
        [0, 0, 1]
    ])
    print("-" * 40)
    print("Матриця переміщення на (2, 3):")
    print(T)
    
    M_composite = T @ R
    final_vertices = M_composite @ vertices
    
    print("-" * 40)
    print("Композитна матриця трансформації (T * R):")
    print(np.round(M_composite, 3))
    print("\nФінальні координати квадрата:")
    print(np.round(final_vertices[:2, :], 3))
    print("="*40 + "\n")

class Task1Scene(AnimatedScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Створюємо квадрат із діагоналлю (0,0) - (1,1)
        polygon = Polygon(
            0, 0,
            1, 0,
            1, 1,
            0, 1
        )
        
        polygon["color"] = "blue"
        polygon.show_local_frame()
        polygon.set_local_frame_parameters(line_style=":", color=("gray", "gray"), line_width=1)
        
        self[FIGURE_KEY] = polygon

def run_visualization():
    """Генерація графічного результату."""
    scene = Task1Scene(
        image_size=(8, 8),
        coordinate_rect=(-1, -1, 5, 6), 
        title="Завдання 1: Поворот на 30° -> Переміщення (2, 3)",
        axis_show=True,
        axis_color=("red", "green"),
        keep_aspect_ratio=True,
    )

    rotation = RotationAnimation(end=np.radians(30), frames=20, channel=FIGURE_KEY)
    translation = TranslationAnimation(end=vertex(2, 3), frames=20, channel=FIGURE_KEY)

    scene.add_animation(rotation)
    scene.add_animation(translation)

    # Зберігаємо результат у картинку в поточну папку
    output_path = os.path.join(current_dir, "task_1_result.png")
    scene.figure.savefig(output_path, dpi=300)
    print(f"[УСПІХ] Візуалізацію збережено у файл: {output_path}")

if __name__ == '__main__':
    calculate_matrices_and_print()
    run_visualization()