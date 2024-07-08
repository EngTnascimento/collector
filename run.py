import logging

import pandas as pd

from collector import Collector

software_false_list = [
    "https://www.arrow.com",
    "https://www.insight.com",
    "https://www.cdw.com",
    "https://www.scansource.com",
    "https://www.techdata.com",
    "https://www.synnex.com",
    "https://www.ingrammicro.com",
    "https://www.arrow.com",
    "https://www.convergetp.com",
    "https://www.eplus.com",
]

mkts_false_list = [
    "https://www.duolingo.com",
    "https://www.grammarly.com",
    "https://www.roku.com",
    "https://www.spotify.com",
    "https://www.khanacademy.org",
    "https://www.coursera.org",
    "https://www.epicgames.com",
    "https://www.canva.com",
    "https://www.dropbox.com",
    "https://www.evernote.com",
]


software_false_collector = Collector(
    software_false_list,
    file_path="dataset/software_false.parquet",
    concurrent=True,
    max_workers=10,
)

mkts_false_collector = Collector(
    mkts_false_list,
    file_path="dataset/mkts_false.parquet",
    concurrent=True,
    max_workers=10,
)

software_false_collector.crawl()
mkts_false_collector.crawl()
