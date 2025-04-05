import os
import shutil
import ast
import textwrap

def move_file_and_return_classes(filename, dst_path=None, year=2021):
    """
    Moves a file from manim-projects/year/ to dst_path and returns list of class names in the file.
    """
    if dst_path is None:
        dst_path = os.getcwd()  # Default to current working directory

    try:
        # Replace dash with underscore in filename
        filename = filename.replace('-', '_')
        src_path = os.path.join('manim-projects', str(year), filename)

        # Move the file
        shutil.move(src_path, dst_path)

        # Read the file content
        moved_file_path = os.path.join(dst_path, filename)
        with open(moved_file_path, 'r') as f:
            code = f.read()

        # Parse the code and extract class names
        tree = ast.parse(code)
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        return classes

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_class_code(filepath, class_name):
    """
    Extracts the source code of a specific class from a Python file.
    """
    try:
        with open(filepath, "r") as file:
            source_code = file.read()

        tree = ast.parse(source_code)
        target_class = None

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                target_class = node
                break

        if not target_class:
            return None

        start_line = target_class.lineno
        end_line = max(
            (getattr(child, 'end_lineno', start_line) for child in ast.walk(target_class)),
            default=start_line
        )

        lines = source_code.splitlines()
        class_lines = lines[start_line - 1:end_line]
        class_code = textwrap.dedent('\n'.join(class_lines))
        return class_code

    except Exception as e:
        return f"Error extracting class code: {e}"

def find_all_files(directory):
    """
    Recursively finds all files in the given directory.
    Returns a list of full file paths.
    """
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            all_files.append(full_path)
    return all_files
  
