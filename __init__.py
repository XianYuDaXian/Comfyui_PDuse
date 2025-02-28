from .json_groupfontsize import json_group_fontsize  # 从当前模块引入名为 MyNode 的类
from .jsonbach import BatchJsonIncremental
from .RemoveColorWords import PD_RemoveColorWords
from .image import PD_Image_Crop_Location
from .image import PD_ImageConcanate
<<<<<<< HEAD
from .fix_name import FileName_refixer
from .node_lora import ReadTxtFiles
=======
from .namefixer import FileName_refixer

>>>>>>> 4bc9fea61864564727a259369c4064818e9702a8

NODE_CLASS_MAPPINGS = {
    "json_group_fontsize": json_group_fontsize,
    "BatchJsonIncremental": BatchJsonIncremental, 
    "PD_RemoveColorWords": PD_RemoveColorWords,
    "PD_Image_Crop_Location": PD_Image_Crop_Location,
    "PD_ImageConcanate": PD_ImageConcanate, 
    "FileName_refixer": FileName_refixer,
    "ReadTxtFiles": ReadTxtFiles,
    # 新添加的节点
    }  

# 节点类映射，定义了节点的名称与类之间的映射关系
NODE_DISPLAY_NAME_MAPPINGS = {
                            "json_group_fontsize": "PD_json_group_fontsize" ,
                            "BatchJsonIncremental": "PD_Incremental_JSON", 
                            "PD_RemoveColorWords": "PD_removeword",  # 新添加的节点
                            "PD_Image_Crop_Location": "PD_Image Crop Location",
                            "PD_ImageConcanate": "PD_ImageConcanate", 
<<<<<<< HEAD
                            "FileName_refixer": "PD_FileName_refixer",
                            "ReadTxtFiles": "PD_ReadTxtFiles"
=======
                            "FileName_refixer": "PD_FileName_refixer"
>>>>>>> 4bc9fea61864564727a259369c4064818e9702a8
                               }  
# 节点显示名称映射，定义了节点的显示名称与其内部名称之间的映射关系
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']