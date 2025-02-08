import torch
from PIL import Image
import numpy as np
from comfy.utils import common_upscale

class PD_Image_Crop_Location:
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {  # 必须的输入参数
                "image": ("IMAGE",),  # 输入的图像
                "x": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域左上角 X 坐标
                "y": ("INT", {"default": 0, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域左上角 Y 坐标
                "width": ("INT", {"default": 256, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域宽度
                "height": ("INT", {"default": 256, "min": 0, "max": 10000000, "step": 1}),  # 裁剪区域高度
            }
        }

    # 返回类型：裁切后的图像
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Result",)  # 返回值的名称
    FUNCTION = "image_crop_location"  # 指定执行的方法名称
    CATEGORY = "PD Suite/Image/Process"  # 定义节点的类别，便于分类

import asyncio
import torch
import torch.nn.functional as F

class PD_ImageConcanate:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {  # 定义输入参数及其类型
            "image1": ("IMAGE",),  # 第一幅输入图像
            "image2": ("IMAGE",),  # 第二幅输入图像
            "direction": (  # 拼接方向，有四个选项
                ['right', 'down', 'left', 'up'],
                {"default": 'right'}  # 默认为向右拼接
            ),
            "match_image_size": ("BOOLEAN", {"default": True}),  # 是否调整图像大小，默认为是
        }}
    
    RETURN_TYPES = ("IMAGE",)  # 定义输出类型
    FUNCTION = "concanate"  # 定义函数名
    CATEGORY = "PDNodes/image"  # 定义节点分类
    DESCRIPTION = """Concatenates the image2 to image1 in the specified direction."""  # 功能描述

    import torch
    import torch.nn.functional as F

    def concanate(self, image1, image2, direction, match_image_size, first_image_shape=None):
        # 获取两张图像的尺寸信息
        batch_size1, channels1, height1, width1 = image1.shape
        batch_size2, channels2, height2, width2 = image2.shape

        # 如果需要调整图像大小
        if match_image_size:
            # 目标尺寸：如果传入了first_image_shape则使用，否则使用image1的尺寸
            target_shape = first_image_shape if first_image_shape is not None else image1.shape
            target_height = target_shape[2]
            target_width = target_shape[3]

            # 调整image2的大小以匹配目标尺寸
            image2_resized = F.interpolate(image2, size=(target_height, target_width), mode='bilinear', align_corners=False)
        else:
            image2_resized = image2  # 不调整大小，直接使用原图

        # 确保两张图片的通道数一致
        channels_image1 = image1.shape[1]
        channels_image2 = image2_resized.shape[1]

        if channels_image1 != channels_image2:
            if channels_image1 < channels_image2:
                # 给image1添加透明alpha通道
                alpha_channel = torch.ones(
                    (*image1.shape[:-1], channels_image2 - channels_image1),
                    device=image1.device
                )
                image1 = torch.cat((image1, alpha_channel), dim=1)
            else:
                # 给image2_resized添加透明alpha通道
                alpha_channel = torch.ones(
                    (*image2_resized.shape[:-1], channels_image1 - channels_image2),
                    device=image2_resized.device
                )
                image2_resized = torch.cat((image2_resized, alpha_channel), dim=1)

        # 根据指定的方向进行拼接
        if direction == 'right':
            # 拼接在右边：需要拼接宽度
            concatenated_image = torch.cat((image1, image2_resized), dim=3)  # dim=3表示在宽度方向拼接
        elif direction == 'down':
            # 拼接在下边：需要拼接高度
            concatenated_image = torch.cat((image1, image2_resized), dim=2)  # dim=2表示在高度方向拼接
        elif direction == 'left':
            # 拼接在左边：需要拼接宽度
            concatenated_image = torch.cat((image2_resized, image1), dim=3)  # dim=3表示在宽度方向拼接
        elif direction == 'up':
            # 拼接在上边：需要拼接高度
            concatenated_image = torch.cat((image2_resized, image1), dim=2)  # dim=2表示在高度方向拼接

        return concatenated_image



# 在 ComfyUI 中的节点映射配置
NODE_CLASS_MAPPINGS = {
    "PD_Image_Crop_Location": PD_Image_Crop_Location, 
    "PD_ImageConcanate": PD_ImageConcanate, # 这个节点对应的类
}

# 设置节点在 UI 中显示的名称
NODE_DISPLAY_NAME_MAPPINGS = {
    "PD_Image_Crop_Location": "PD Image Crop Location",
    "PD_ImageConcanate": "PD ImageConcanate", # 自定义节点名称
}
