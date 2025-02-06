import sys

import pymupdf as fitz
import logging
import os


def compress_pdf(input_pdf, output_pdf):
    """Сжимает PDF-файл, уменьшая качество изображений."""
    doc = fitz.open(input_pdf)
    doc.save(output_pdf, garbage=4, deflate=True, clean=True, incremental=False)
    logging.info(f"Сжатый PDF сохранён как {output_pdf}")
    logging.info(f"размер сжатого файла: {(os.path.getsize(output_pdf) // 1024 / 1024)} MB")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    compress_pdf("../files/guide.pdf", "../files/compress_guide.pdf")