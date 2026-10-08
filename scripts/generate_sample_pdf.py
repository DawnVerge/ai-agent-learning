"""将自编 learning_guide.txt 排为三页 PDF；需要 reportlab。"""
from pathlib import Path
import argparse
from html import escape

ROOT = Path(__file__).resolve().parents[1]


def generate(output=None, font_path=None):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

    source = ROOT / "assets" / "learning_guide.txt"
    output = Path(output) if output else source.with_suffix(".pdf")
    if font_path:
        pdfmetrics.registerFont(TTFont("SampleChinese", str(font_path)))
    else:
        # CID 字体避免将系统字体文件加入仓库。生成 PDF 时可用 --font 嵌入本机字体。
        pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    font = "SampleChinese" if font_path else "STSong-Light"
    body = ParagraphStyle("body", fontName=font, fontSize=11, leading=21,
                          alignment=TA_LEFT, textColor=colors.HexColor("#24364B"),
                          wordWrap="CJK", spaceAfter=13)
    title = ParagraphStyle("title", parent=body, fontSize=22, leading=32, spaceAfter=24,
                           textColor=colors.HexColor("#134E6F"))
    heading = ParagraphStyle("heading", parent=body, fontSize=16, leading=25, spaceAfter=19,
                             textColor=colors.HexColor("#134E6F"))
    note = ParagraphStyle("note", parent=body, fontSize=9, leading=16,
                          textColor=colors.HexColor("#516779"), spaceAfter=24)
    paragraphs = source.read_text(encoding="utf-8").strip().split("\n\n")
    story = []
    chapter = 0
    for index, paragraph in enumerate(paragraphs):
        if index == 0:
            first, _, disclaimer = paragraph.partition("\n")
            story += [Paragraph(escape(first), title), Paragraph(escape(disclaimer), note)]
            continue
        lines = paragraph.splitlines()
        chapter_heading = lines[0]
        if chapter_heading.startswith(("第一章", "第二章", "第三章")):
            if chapter:
                story.append(PageBreak())
            chapter += 1
            story.append(Paragraph(escape(chapter_heading), heading))
            for line in lines[1:]:
                story.append(Paragraph(escape(line), body))
        else:
            story.append(Paragraph(escape(paragraph), body))
        story.append(Spacer(1, 6))

    def decorate(canvas, doc):
        canvas.setFont(font, 9)
        canvas.setFillColor(colors.HexColor("#66798B"))
        canvas.drawString(48, 30, "AI Agent Learning - original fictional sample")
        canvas.drawRightString(A4[0] - 48, 30, f"{doc.page}")
        canvas.setStrokeColor(colors.HexColor("#D7E1EA"))
        canvas.line(48, 48, A4[0] - 48, 48)

    output.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(output), pagesize=A4, leftMargin=48, rightMargin=48,
                                 topMargin=46, bottomMargin=67, title="星河 AI 学习社团手册",
                                 author="AI Agent Learning", subject="Original fictional teaching sample")
    document.build(story, onFirstPage=decorate, onLaterPages=decorate)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="输出路径，默认 assets/learning_guide.pdf")
    parser.add_argument("--font", type=Path, help="可选：嵌入支持中文的 TTF 字体；不复制字体文件到仓库")
    args = parser.parse_args()
    print(generate(args.output, args.font))

if __name__ == "__main__":
    main()
