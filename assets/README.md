# 教学样本

本目录的文本是为本项目重新编写的教学素材，与仓库采用相同许可。`learning_guide.txt` 描述虚构的学习社团；设备型号、传感器数量和项目安排均为练习数据。`beijing_guide.txt` 与 `history_note.txt` 用于文本加载和切分练习。

`learning_guide.pdf` 从同名文本生成，供 PDF 加载与问答使用。重新生成：

```console
python scripts/generate_sample_pdf.py
```

生成需要可选开发依赖 `reportlab`。仓库已提供生成后的 PDF，运行课程无需重新生成。不包含原学习目录中来源或许可未确认的文档。
