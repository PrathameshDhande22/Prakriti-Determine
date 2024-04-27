import logging
import pandas as pd
from logger import logger
from diet import recommend_Diet
from weasyprint import HTML, CSS
from nltk.tokenize import sent_tokenize
from typing import Literal
import os

df = pd.read_csv(os.path.join("dataset", "videos.csv"))
# nltk.download("punkt")

logging.getLogger("weasyprint").setLevel(logging.WARNING)
logging.getLogger("fontTools").setLevel(logging.WARNING)

def createHTMLListString(text: str, listTag: Literal["<ul>", "<ol>"], closingTag: Literal["</ul>", "</ol>"]) -> str:
    text: list[str] = sent_tokenize(text)
    text.insert(0, listTag)
    text.insert(len(text), closingTag)
    for i in range(1, len(text)-1):
        text[i] = f"<li>{text[i]}</li>"
    text = "".join(text)
    return text


def createHTMLVideoElement(videos: dict[str, str]) -> str:
    htmlstr = list()
    for vids in videos:
        htmlstr.append("<div style='margin-top:9px;'>")
        htmlstr.append(f"<span>{vids} ➡️ </span>")
        htmlstr.append(f"<a href='{videos[vids]}'>{videos[vids]}</a>")
        htmlstr.append("</div>")
    videosString = "".join(htmlstr)
    return videosString


def recommentVideos(dosha: str) -> dict[str, str]:
    vids = df.loc[df["Doshas"] == dosha].drop("Doshas", axis=1).to_dict()
    return dict(zip(list(vids["Title"].values()), list(vids["Video"].values())))


def createPDF(consume: str, avoid: str, dosha: str, lifeStyle: str) -> bytes:
    with open(os.path.join("doc.html"), "r", encoding="utf8") as f:
        html_content = str(f.read())
    videos = recommentVideos(dosha)
    html_content = html_content.format(
        dosha, createHTMLListString(consume, "<ul>", "</ul>"), createHTMLListString(avoid, "<ul>", "</ul>"), createHTMLListString(lifeStyle, "<ol>", "</ol>"), createHTMLVideoElement(videos=videos))
    pdf = HTML(string=html_content).write_pdf(stylesheets=[
        CSS(string="@page {size: A4; margin: 18mm 15mm 25mm 15mm;}")])
    logger.info("Created PDF File")
    return pdf
