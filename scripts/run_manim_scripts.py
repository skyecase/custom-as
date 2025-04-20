import ast
import os

def return_classes(filename, dst_path=None, year=2021):
  #this code is garbage but it works
  src_path = os.path.join('content', str('animations') , filename)
  with open(src_path, 'r') as f:
        code = f.read()

  tree = ast.parse(code)
  classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
  return classes

def run_manim_scene(filename):
   
   src_path = os.path.join('content', str('animations') , filename)   
   print(f"Running Scene from {src_path}...")   
   for class_ in return_classes(filename):
       try : 
          print(f"Executing Scene {class_}")
          get_ipython().run_cell_magic('manim', f'-qm -v WARNING {class_}', '')

       except Exception as e:    
         print(f"Exception occurred {e}  with Scene {class_} in {src_path}")
         print("Skipping this class")
         print()
