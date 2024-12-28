
**Comfyui\_PDuse**

<a name="heading_0"></a>1. **Node\_README\_AR.md**

<a name="heading_1"></a>1.1 **安装方法**

(以ComfyUI官方便携包和秋叶整合包为例，其他ComfyUI环境请修改依赖环境目录)

<a name="heading_2"></a>1.2 **工作流用示例**

在workflow目录下有json格式的工作流示例文件，示范了如何在ComfyUI中使用这些节点。

下载解压zip文件，将得到的文件夹复制到 ComfyUI\custom\_nodes\。

<a name="heading_3"></a>1.3 **节点使用示例**

在ComfyUI画布双击, 在搜索框输入"PD"。

![](Aspose.Words.14473600-fb86-46bf-b04a-a30ce5ab0be9.001.png)

<a name="heading_4"></a>1.4 **更新说明：**

- 添加三个节点，字面意思，处理json和字体的功能，适合批量处理。

  <a name="heading_5"></a>2. **节点说明：**

  <a name="heading_6"></a>2.1 **PD\_group字体大小统一:**

- PD\_groupfontsize:主要用来修改json文件里面编组字体大小，
- font\_size 设置：主要是要统一设置的字体大小。
- tile：保留那个不需要改变字体大小的组。
- https://github.com/7BEII/Comfyui_PDuse/blob/f011c9c848b6a3aed06a17b29d87ba898ad74e2f/img/Aspose.Words.14473600-fb86-46bf-b04a-a30ce5ab0be9.002.png

  ![](Aspose.Words.14473600-fb86-46bf-b04a-a30ce5ab0be9.002.png)

  <a name="heading_7"></a>2.2 **PD\_批量JSON递增编号排序JSON**

- "input\_folder":   输入文件夹路径         
- "output\_folder":  输出文件夹路径
- "start\_x": "INT",起始坐标 X
- "start\_y": "INT",   起始坐标 Y
- "increment": 坐标递增步长
- "file\_prefix": 输出文件前缀

  ![](Aspose.Words.14473600-fb86-46bf-b04a-a30ce5ab0be9.003.png)

  <a name="heading_8"></a>2.3 **PD\_批量去除文本字体**

- "directory\_path:  # 文件夹路径
- "words\_to\_remove: # 要删除的单词

  ![](Aspose.Words.14473600-fb86-46bf-b04a-a30ce5ab0be9.004.png)


