# MIT License
#
# Copyright (c) 2024 dataforgood
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Standard imports
import logging

# Local imports
from . import img_table_extraction, pagefilter


class ReportProcessor:
    def __init__(self, config: dict) -> None:
        # Report filter
        self.page_filter = pagefilter.from_config(config["pagefilter"])

        # Table extraction from images
        img_table_extractors = config["table_extraction"]["img"]
        self.img_table_extractors = [
            img_table_extraction.from_config(name) for name in img_table_extractors
        ]

    def process(self, pdf_filepath: str) -> dict:
        logging.info(f"Processing {pdf_filepath}")

        assets = {
            "pagefilter": {},
            "text_table_extractors": {},
            "img_table_extractors": {},
        }

        # Filtering the pages
        self.page_filter(pdf_filepath, assets)

        pdf_to_process = assets["pagefilter"]["target_pdf"]

        # Process the selected pages to detect the tables and extract
        # their contents
        for img_table_extractor in self.img_table_extractors:
            img_table_extractor(pdf_to_process, assets)

        # Given the parsed content to the RAG for identifying the key numbers
        # TODO
        # For now, just print the results
        print(assets)

        return assets
