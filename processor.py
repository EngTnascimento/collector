from typing import Optional

import pandas as pd


class Processor:
    def __init__(self, labeled_paths: dict[bool, str], out_put_path: str) -> None:
        self.labeled_paths: dict[bool, str] = labeled_paths
        self.true_df: Optional[pd.DataFrame] = None
        self.false_df: Optional[pd.DataFrame] = None
        self.merged_df: Optional[pd.DataFrame] = None
        self.out_put_path: str = out_put_path

    def __load_df(self):
        for path, label in self.labeled_paths.items():
            if label:
                self.true_df = pd.read_parquet(path, engine="fastparquet")
            else:
                self.false_df = pd.read_parquet(path, engine="fastparquet")

    def __merge_df(self) -> pd.DataFrame:
        pass

    def process(self):
        self.__load_df()
        self.merged_df: pd.DataFrame = (
            self.__merge_df()
            if self.true_df and self.false_df
            else self.true_df or self.false_df
        )
