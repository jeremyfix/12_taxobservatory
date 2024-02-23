# Copyright (c) 2015-2024 Data4Good
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

python3 -m venv venv
source venv/bin/activate
python -m pip install camelot-py opencv-python-headless ghostscript

"""

# Standard imports
from pathlib import Path
import argparse
import glob

# External imports
import camelot
import matplotlib.pyplot as plt


def extract_tables(rootdir: Path, flavor: str):
    pdf_files = glob.glob(str(rootdir / "*.pdf"))
    for filename in pdf_files:
        tables = camelot.read_pdf(filename, flavor=flavor)
        print(f"For file {filename}, I found {len(tables)} tables")
        for itable, table in enumerate(tables):
            print(table.df)
            img_filename = filename + f"t{itable}" + "-contour.png"
            fig = camelot.plot(table, kind="text", filename=img_filename)
            # sys.exit(-1)
            plt.close()
        print("")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--rootdir",
        type=Path,
        help="The path to a directory containing the PDFs",
        default=None,
        required=True,
    )

    parser.add_argument("--flavor", choices=["stream", "lattice"], required=True)

    args = parser.parse_args()
    rootdir = Path(args.rootdir)

    extract_tables(rootdir, args.flavor)
