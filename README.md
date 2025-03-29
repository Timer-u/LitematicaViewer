LitematicaViewer投影查看器 v0.6.4
=================================

### Minecraft tool - A tool make easy to check litematica files 让我的世界投影查看更加的轻量便捷

GITHUB链接: https://github.com/albertchen857/LitematicaViewer
求求点点星吧 I want Stars~

A light Viewer of Litematica files

* `imput file` Input your file first and choose mode for check your file.
* `output` Output Litematica analysis data into a file or chart. (Text File & Excel File)
* `Classification Output` Output Litematica analysis data with classification into a file or chart. (Text File & Excel File)
* `Simple Analysis` used for easy check your block numbers and names, no properties
* `Container Analysis` analysis containers with items inside, show items and basic infos
* `Spawn Regular Shape` A Light Tool to generate a regular shape
* `Fill Specific Block` A Light Tool to replace multiple types of blocks with your own setting limitations
* `3D Rendering` 3d Rendering target Litematic file.
* `Transfer Litematic File Version` Transfer 1.21 Litematic file into old versions (1.16 ~ 1.12)

一个轻量便捷的投影查看器

* `导入` 导入投影文件
* `导出` 导出投影数据 (文本&表格)
* `分类导出` 导出分类投影数据 (文本&表格)
* `简洁分析` 轻量分析，只会显示方块名与数量
* `容器分析` 容器分析，显示容器中存储的方块和基础信息
* `生成图形投影` 快捷生成一个常规立方体
* `替换特定方块` 快速替换/限制投影里的不同方块
* `3D渲染` 3D渲染目标投影 (可能引起卡顿)
* `跨版本转换投影` 将默认最新版本投影转换到1.16/1.13版本的投影文件

# 分支图
```
投影查看器LitematicaViewer
|-分析analysis
| |-简洁分析simpleAnalysis
| |-容器分析ContainerAnalysis
| | |-普通分析Norm
| | |-分类分析(开发ing)Cate
| |-全面分析 (关闭)FullAnalysis
|-导出Output
| |-普通导出 (txt/csv)Norm
| |-分类导出 (txt/csv)Cate
|-统计Stat
| |-常规统计 (红石/中位/其他)Basic
| |-成分统计 (方块拼图)PieGraph
| |-3D渲染 (旋转/静止)3DRender
|-功能func
| |-生成图形投影Polygon
| | |-立方体生成Cube
| | |-特殊形状生成(开发)Unusual
| |-替换特定方块ChangeIndentifyBlock
| |-投影转换版本 (1.17/1.15/1.12)TransVersion
|-界面UI
  |-字体/颜色/布局自定义美化(开发) UIupdate
```