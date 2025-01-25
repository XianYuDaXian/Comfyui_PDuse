from .json_groupfontsize import PD_node  # 从当前模块引入名为 MyNode 的类
from .jsonbach import BatchJsonIncremental
from .txtjson import PD_RemoveColorWords
from .PDimage import PD_Image_Crop_Location
from .PDimage import PD_Image_centerCrop 
from .PDimage import PD_GetImageSize # 导入 PD_Image_centerCrop 类
# 节点类映射，定义了节点的名称与类之间的映射关系
NODE_CLASS_MAPPINGS = {
    "PD_node": PD_node,
    "BatchJsonIncremental": BatchJsonIncremental, 
    "PD_RemoveColorWords": PD_RemoveColorWords,
    "PD_Image_Crop_Location": PD_Image_Crop_Location,
    "PD_Image_centerCrop": PD_Image_centerCrop,
    "PD_GetImageSize": PD_GetImageSize, 
    # 新添加的节点
    }  

# 节点类映射，定义了节点的名称与类之间的映射关系
NODE_DISPLAY_NAME_MAPPINGS = {
                            "PD_node": "PD_groupfontsize unnify" ,
                            "BatchJsonIncremental": "PD_grownumber-JSON", 
                            "PD_RemoveColorWords": "PD_add or delete words",  # 新添加的节点
                            "PD_Image_Crop_Location": "PD_Image Crop Location",
                            "PD_Image_centerCrop": "PD_Image centerCrop",
                            "PD_GetImageSize": "PD_GetImageSize", 
                               }  
# 节点显示名称映射，定义了节点的显示名称与其内部名称之间的映射关系
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']