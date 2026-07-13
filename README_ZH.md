# bubbleDAS

作者： 杨天让, 方桢  

[![License|0](https://img.shields.io/badge/license-AGPL3.0-red.svg)](LICENSE)  

[English](README.MD) | 中文

## 简介

`bubbleDAS` 是一个**集成气泡检测工具**，可辅助电解槽或电解池电极上的气泡可视化研究。

![[res4Readme/UI.png]]

## 功能特点

|                        **输入要求**                         |                       **输出结果**                       |         **注意事项**          |
|:-----------------------------------------------------------:|:--------------------------------------------------------:|:-----------------------------:|
|                          **视频**                           |           气泡检测统计（如每帧平均停留气泡数）           | 输出结果可直接加载至软件中。  |
|                          **图片**                           | 带 `xywh` 坐标的 `.txt` 文件（可通过 **labelImg** 读取） |  推荐使用 **labelImg** 工具   |
| **视频 + 通过 anylabeling 标注的膈膜区域（Membrane zone）** |               更多统计数据（如膜覆盖比例）               | 推荐使用 **anylabeling** 工具 |

### 注意事项：

- **气泡状态** 包括：
  - **粘附（Staying）**：气泡吸附在电极/背景上。
  - **流动（Flowing）**：气泡在通道/前景中流动。
  - **脱附（Detaching/Out）**：从停留状态转为流动状态。
  - **吸附（Attaching/Back）**：从流动状态转为停留状态。  
  **详细定义请参考 DOI: ........**

- 不安装 labelImg 和 anylabeling 不会影响软件运行，但可能导致软件的部分输入和输出难以理解。

## 安装指南

### 快速安装（不支持 GPU 加速）

1. 从 [python.org](https://www.python.org/) 下载 **Python 3.12.13**。
2. 安装依赖包：

```bash
pip install ultralytics matplotlib numpy pandas shapely tqdm wxPython pgzip -i https://pypi.tuna.tsinghua.edu.cn/simple
```

3. 从本项目的 `\release` 文件夹复制最新版本到本地。
4. 运行 `MainEntry.py`：
   - **Windows 系统**：
     - 打开包含 `MainEntry.py` 的文件夹。
     - 在另一窗口打开 `python.exe` 所在文件夹。
     - 将 `MainEntry.py` 拖到 `python.exe` 上运行。
   - **其他方式**：
```bash
<your python path> <the path where MainEntry.py is located>
```

### 常规安装（支持 GPU 加速）

1. 从 [python.org](https://www.python.org/) 安装 **Python 3.8–3.12**。
2. 安装与 GPU 驱动兼容的 **PyTorch**：
   - 推荐按照 [PyTorch 官方指南](https://pytorch.org/get-started/locally/) 操作。
3. 安装其他依赖包：

   ```bash
   pip install ultralytics matplotlib numpy pandas shapely tqdm wxPython pgzip -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

4. 从本项目的 `\release` 文件夹克隆最新版本到本地。
5. 使用与上述相同方式运行 `MainEntry.py`。

## 其他工具：labelImg 与 anylabeling

此处我们提供一个可用的下载方法。[labelImg](https://github.com/HumanSignal/labelImg)  和 [anylabeling](https://github.com/vietanhdev/anylabeling) 的官方安装方法请参见其 github 首页。

> [!attention] 注意
> 替换代码时，请保持缩进量。也即，原来这行代码前有多少个空格或`tab`，更改后这行代码前就应有多少空格或`tab`。

### labelImg（用于查看图片识别的结果）

1. pip安装：

```bash
pip install labelimg -i https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 修改 `canvas.py` 文件（路径：`<python folder>\Lib\site-packages\libs\canvas.py`）：
   - 替换第 526 行：

```python
p.drawRect(left_top.x(), left_top.y(), rect_width, rect_height)
```

为：

```python
p.drawRect(int(left_top.x()), int(left_top.y()), int(rect_width), int(rect_height))
```

   - 替换第 530–531 行：

```python
     p.drawLine(self.prev_point.x(), 0, self.prev_point.x(), self.pixmap.height())
     p.drawLine(0, self.prev_point.y(), self.pixmap.width(), self.prev_point.y())
```

为：

```python
p.drawLine(int(self.prev_point.x()), 0, int(self.prev_point.x()), int(self.pixmap.height()))
p.drawLine(0, int(self.prev_point.y()), int(self.pixmap.width()), int(self.prev_point.y()))
```

3. 修改 `shape.py` 文件（路径：`<python folder>\Lib\site-packages\libs\shape.py`）：
   - 替换第 131 行：

```python
painter.drawText(min_x, min_y, self.label)
```

 为：
 
```python
painter.drawText(int(min_x), int(min_y), self.label)
```

4. 创建快捷方式并运行：

```bash
<your python folder>\pythonw.exe -c "from labelImg.labelImg import main; main()"
```

---

### anylabeling（用于标注膜面积）

1. 安装：

```bash
pip install anylabeling -i https://pypi.tuna.tsinghua.edu.cn/simple
```
   
2. 启动：

```bash
anylabeling
```


## 授权协议

本项目采用 **AGPL 3.0** 授权协议。详细内容请见 [LICENSE](LICENSE) 文件。