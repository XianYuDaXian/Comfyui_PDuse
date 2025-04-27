import importlib
import os

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def get_ext_dir(subpath=None, mkdir=False):
    dir = os.path.dirname(__file__)
    if subpath is not None:
        dir = os.path.join(dir, subpath)
    return os.path.abspath(dir)

# 动态扫描 py/目录
py_dir = get_ext_dir("py")
files = os.listdir(py_dir)

for file in files:
    if not file.endswith(".py") or file.startswith("_"):
        continue

    module_name = os.path.splitext(file)[0]

    try:
        imported_module = importlib.import_module(f".py.{module_name}", __name__)
        
        NODE_CLASS_MAPPINGS.update(imported_module.NODE_CLASS_MAPPINGS)
        NODE_DISPLAY_NAME_MAPPINGS.update(imported_module.NODE_DISPLAY_NAME_MAPPINGS)
        
    except Exception as e:
        print(f"加载模块 {file} 出错了：{e}")

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
