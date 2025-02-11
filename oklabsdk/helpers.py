import pymupdf
import base64

import pymupdf4llm

pymupdf.TEXT_PRESERVE_WHITESPACE = False
pymupdf.TEXTFLAGS_TEXT = pymupdf.TEXT_PRESERVE_LIGATURES | pymupdf.TEXT_PRESERVE_WHITESPACE | pymupdf.TEXT_MEDIABOX_CLIP | pymupdf.TEXT_CID_FOR_UNKNOWN_UNICODE

def pdftomd(pdf_path):
    md_text = pymupdf4llm.to_markdown(pdf_path, write_images=True, image_path="./pics")
    with open(pdf_path + ".md", "w", encoding="utf8") as f:
        f.write(md_text)
    return md_text
  


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if __name__ == "__main__":
    pdftomd("H_Pracovni_zarazeni.pdf")
