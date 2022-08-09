import click
import io
import re

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams


@click.command()
@click.option("--infilename", help="Input file name.")
@click.option("--outfilename", help="Output file name.")
def main(infilename: str, outfilename: str):
    with open(infilename,'rb') as infile:
        manager = PDFResourceManager()
        stream = io.StringIO()
        converter = TextConverter(manager, stream, laparams= LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        for page in PDFPage.get_pages(infile):
            interpreter.process_page(page)
     
        text = stream.getvalue()
        text = text.replace(u"\xa0", u" ")
        text = text.replace(u"\x0c", u" ")
        text = text.replace(u"\x0a", u" ")

        pattern = "Physical Description: ([0-9]+) ([ a-z]+)\(s\)"
        expression = re.compile(pattern)
        results = {}
        for match in expression.findall(text):
            count = match[0]
            type = match[1]

            if results.get(type, None) is None:
                results[type] = int(count)
            else:
                results[type] = results[type] + int(count)

        with open(outfilename,'w') as outfile:
            total = 0
            for type, count in results.items():
                print(f"{type}: {count}", file=outfile)
                total = total + count
            print(f"\ntotal: {total}", file=outfile)


if __name__ == "__main__":
    main()