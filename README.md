# ComfyUI PDuse

## 工作流用示例
在workflow目录下有json格式的工作流示例文件，示范了如何在ComfyUI中使用这些节点。

## 安装方法
(以ComfyUI官方便携包和秋叶整合包为例，其他ComfyUI环境请修改依赖环境目录)

### 安装插件
* 推荐使用 ComfyUI Manager 安装。
* 或者在CompyUI插件目录(例如“CompyUI\custom_nodes\”)中打开cmd窗口，键入    
```
git clone 
```
* 或者下载解压zip文件，将得到的文件夹复制到 ```ComfyUI\custom_nodes\```。   
* Python环境下安装 pip install -r requirements.txt

## 常见问题
如果节点不能正常加载，或者使用中出现错误，请在ComfyUI终端窗口查看报错信息。以下是常见的错误及解决方法。

## 节点说明

#### **JSON处理**
##### PDJSON_Group​
- directory_path​​ ​​：指定要处理的JSON文件所在文件夹路径
- ​​color_choice​​​​：选择要批量修改的颜色（图中选为Blue）
- ​​modify_size​​​​：enable（启用修改）或 disable（保持原样）font_size​​
- ​​作用​​：当modify_size启用时，设置目标字体大小范围：8~72（仅在修改时生效）
- ​​target_title​​​​：指定只修改特定标题的组（留空则修改所有组）
- ​​output_folder指定输出文件夹路径（留空则覆盖原文件）
- ​​new_filename​​（图中为_fix01）新文件名后缀格式file.json → file_fix01.json
- ​​Result​​：输出显示处理结果（如成功/错误信息）

#### **text处理**

##### PD_ImageMergerWithText
> 字体文件可以放入文件夹fonts 。
> 两张图片合在一起，然后两个文字分别加上去，制作对比图使用。

- image1+ ​​​​image2 ：尽量要求同样尺寸，如果不同，会自动等比例缩放对齐
- text1 + text2   ：支持中文，需字体文件包含中文编码，可输入如"效果图“：“原图”之类
- font_size​：小于20可能看不清，大于80可能超出画布
- ​​padding_up​：文字​​上方​​的留白高度，10-30
- ​​padding_down：文字​**​下方​**​的留白高度  10- 1000 ,可以往下扩多一些方便排版
- font_file​  选择字体样式, 需将.ttf/.otf文件放入插件目录的fonts文件夹
##### PD_Text Overlay Node
> PD_Text Overlay Node 主要作用是给图片添加文字，并且指定位置贴上去。
- image：要处理的输入图片
- text：需要叠加的文字内容 
- font_size：字体大小 
- font_color：文字颜色，使用HEX格式，如#000000 
- position_x：文字水平位置（0到1，0是左，1是右） 
- position_y：文字垂直位置（0到1，0是上，1是下） 
- letter_gap：字符间距（可为负数，负数使字母靠近） 
- font_name：使用的字体文件名（从fonts目录中选择）

#### **image处理**