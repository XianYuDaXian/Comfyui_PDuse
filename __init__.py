from .json_groupfontsize import PD_node  # 从当前模块引入名为 MyNode 的类
from .jsonbach import BatchJsonIncremental
from .RemoveColorWords import PD_RemoveColorWords
from .PDimage import PD_Image_Crop_Location
from .PDimage import PD_ImageConcanate
from .namefixer import FileName_refixer


NODE_CLASS_MAPPINGS = {
    "PD_node": PD_node,
    "BatchJsonIncremental": BatchJsonIncremental, 
    "PD_RemoveColorWords": PD_RemoveColorWords,
    "PD_Image_Crop_Location": PD_Image_Crop_Location,
    "PD_ImageConcanate": PD_ImageConcanate, 
    "FileName_refixer": FileName_refixer,
    # 新添加的节点
    }  

# 节点类映射，定义了节点的名称与类之间的映射关系
NODE_DISPLAY_NAME_MAPPINGS = {
                            "PD_node": "PD_group字体大小统一" ,
                            "BatchJsonIncremental": "PD_批量JSON递增编号排序JSON", 
                            "PD_RemoveColorWords": "PD_removeword",  # 新添加的节点
                            "PD_Image_Crop_Location": "PD Image Crop Location",
                            "PD_ImageConcanate": "PD ImageConcanate", 
                            "FileName_refixer": "FileName_refixer"
                               }  
# 节点显示名称映射，定义了节点的显示名称与其内部名称之间的映射关系
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']