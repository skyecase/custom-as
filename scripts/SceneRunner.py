import ast
import os

class SceneRunner:
    def __init__(self, scene_name, runner_func):
        self.scene_name = scene_name
        self.runner_func = runner_func

    def __call__(self):
        self.runner_func(self.scene_name)

    def runtime(self, seconds):
        self.runner_func(self.scene_name, seconds)

    def __repr__(self):
        return f"<SceneRunner scene='{self.scene_name}'>"


class RunManim:
    def __init__(self, filename, *, dirname='content', foldername='animations'):
        path_parts = [p for p in (dirname, foldername) if p]
        self.filename = filename
        self.base_path = os.path.join(*path_parts) if path_parts else '.'
        self.src_path = os.path.join(self.base_path, filename)
        self.scene_names = self._extract_classes()

    def _extract_classes(self):
        with open(self.src_path, 'r') as f:
            tree = ast.parse(f.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]

    def _run_scene(self, scene_name, seconds=None):
        cmd = f"-qm -v WARNING {scene_name}"
        if seconds is not None:
            cmd += f" --disable_caching --from_animation_number 0 --to_time {seconds}"
        try:
            print(f"Running scene: {scene_name}")
            get_ipython().run_cell_magic('manim', cmd, '')
        except Exception as e:
            print(f"Error running scene {scene_name}: {e}")

    def __getitem__(self, index):
        if not isinstance(index, int):
            raise TypeError("Index must be an integer.")
        if index < 1 or index > len(self.scene_names):
            raise IndexError("Scene index out of range.")

        scene_name = self.scene_names[index - 1]
        return SceneRunner(scene_name, self._run_scene)

    def __iter__(self):
        for scene_name in self.scene_names:
            yield SceneRunner(scene_name, self._run_scene)

    def runtime(self, index, seconds):
        if index < 1 or index > len(self.scene_names):
            raise IndexError("Scene index out of range.")
        scene_name = self.scene_names[index - 1]
        self._run_scene(scene_name, seconds)
