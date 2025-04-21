import ast
import os
from IPython.display import Image, display

class SceneRunner:
    def __init__(self, scene_name, runner_func, filename):
        self.scene_name = scene_name
        self.runner_func = runner_func
        self.filename = filename  # e.g., 'circle_scene.py'

    def __call__(self):
        self.runner_func(self.scene_name)

    def runtime(self, seconds):
        print("Note: Partial runtime execution is not supported via CLI flags.")
        self.__call__()

    def save_image(self):
        self.runner_func(self.scene_name, save_image=True)
        image_path = os.path.join(
            'media', 'images',
            os.path.splitext(self.filename)[0],
            f"{self.scene_name}.png"
        )
        if os.path.exists(image_path):
            display(Image(image_path))
        else:
            print(f"Image not found at {image_path}. Make sure rendering succeeded.")

    def __repr__(self):
        return f"<SceneRunner scene='{self.scene_name}'>"


class RunManimScene:
    def __init__(self, filename, *, dirname='content', foldername='animations'):
        path_parts = [p for p in (dirname, foldername) if p]
        self.filename = filename
        self.base_path = os.path.join(*path_parts) if path_parts else '.'
        self.src_path = os.path.join(self.base_path, filename)
        self.scene_names = self._extract_classes()
        print(f"Executing {self.src_path}")

    def _extract_classes(self):
        with open(self.src_path, 'r') as f:
            tree = ast.parse(f.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    def _run_scene(self, scene_name, *, save_image=False):
        cmd = f"-qm -v WARNING {scene_name}"
        if save_image:
            cmd = f"-s -v WARNING {scene_name}"
        try:
            print(f"Running scene: {scene_name} {'(saving image)' if save_image else ''}")
            get_ipython().run_cell_magic('manim', cmd, '')
        except Exception as e:
            print(f"Error running scene {scene_name}: {e}")

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if index < 1 or index > len(self.scene_names):
            raise IndexError("Scene index out of range.")
        scene_name = self.scene_names[index - 1]
        return SceneRunner(scene_name, self._run_scene, self.filename)

    def __iter__(self):
        for scene_name in self.scene_names:
            yield SceneRunner(scene_name, self._run_scene, self.filename)

    def runtime(self, index, seconds):
        print("Manim CLI does not support runtime limiting via flags.")
        self[index]()
