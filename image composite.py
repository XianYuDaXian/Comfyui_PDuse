import torch
from PIL import Image
import numpy as np

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

    def concanate(self, image1, image2, direction, match_image_size, first_image_shape=None):
        # 检查批处理大小是否不同
        batch_size1 = image1.shape[0]
        batch_size2 = image2.shape[0]

        if batch_size1 != batch_size2:
            # 计算需要重复的次数以使两批大小一致
            max_batch_size = max(batch_size1, batch_size2)
            repeats1 = max_batch_size // batch_size1
            repeats2 = max_batch_size // batch_size2
            
            # 重复图像以匹配最大的批处理大小
            image1 = image1.repeat(repeats1, 1, 1, 1)  # 重复batch维度
            image2 = image2.repeat(repeats2, 1, 1, 1)

        if match_image_size:
            # 使用提供的first_image_shape，若没有则使用image1的形状
            target_shape = first_image_shape if first_image_shape is not None else image1.shape

            # 获取image2的原始尺寸
            original_height = image2.shape[1]
            original_width = image2.shape[2]
            original_aspect_ratio = original_width / original_height  # 计算宽高比
            
            if direction in ['left', 'right']:
                # 沿宽度方向拼接，匹配目标高度并调整宽度以保持_aspect ratio
                target_height = target_shape[1]
                target_width = int(target_height * original_aspect_ratio)
            elif direction in ['up', 'down']:
                # 沿高度方向拼接，匹配目标宽度并调整高度以保持AspectRatio
                target_width = target_shape[2]
                target_height = int(target_width / original_aspect_ratio)
            
            # 将image2调整为上下文尺度函数所需的格式（B, C, H, W）
            image2_for_upscale = image2.movedim(-1, 1)  # 交换通道维度
            
            # 调整image2的大小以匹配目标尺寸，使用lanczos插值
            # 这里调用了一个名为common_upscale的函数
            image2_resized = common_upscale(image2_for_upscale, target_width, target_height, "lanczos", "disabled")
            
            # 将image2调整回原始格式（B, H, W, C）
            image2_resized = image2_resized.movedim(1, -1)
        else:
            image2_resized = image2  # 如果不需要调整大小，直接使用原始图像

        # 确保两张图片的通道数一致
        channels_image1 = image1.shape[-1]
        channels_image2 = image2_resized.shape[-1]

        if channels_image1 != channels_image2:
            if channels_image1 < channels_image2:
                # 给image1添加alpha通道
                alpha_channel = torch.ones(  # 创建全1的alpha通道
                    (*image1.shape[:-1], channels_image2 - channels_image1),  # 通道数差值
                    device=image1.device  # 在与image1相同的设备上创建
                )
                image1 = torch.cat((image1, alpha_channel), dim=-1)  # 拼接通道
            else:
                # 给image2添加alpha通道
                alpha_channel = torch.ones(
                    (*image2_resized.shape[:-1], channels_image1 - channels_image2),
                    device=image2_resized.device
                )
                image2_resized = torch.cat((image2_resized, alpha_channel), dim=-1)

        # 根据指定的方向进行拼接
        if direction == 'right':
            concatenated_image = torch.cat((image1, image2_resized), dim=2)  # 沿宽度方向拼接
        elif direction == 'down':
            concatenated_image = torch.cat((image1, image2_resized), dim=1)  # 沿高度方向拼接
        elif direction == 'left':
            concatenated_image = torch.cat((image2_resized, image1), dim=2)  # 沿宽度方向拼接
        elif direction == 'up':
            concatenated_image = torch.cat((image2_resized, image1), dim=1)  # 沿高度方向拼接

        return concatenated_image  # 返回拼接后的图像


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
