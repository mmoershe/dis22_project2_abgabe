import marimo

__generated_with = "0.14.9"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import os

    CURRENT_DIRECTORY: str = os.path.dirname(__file__)
    ROOT_DIRECTORY: str = os.path.dirname(CURRENT_DIRECTORY)
    DATA_DIRECTORY: str = os.path.join(ROOT_DIRECTORY, "data")
    CLUSTER2_DIRECTORY: str = os.path.join(DATA_DIRECTORY, "cluster2.tsv")

    class Data: 
        def __init__(self): 
            self.raw_df: pd.DataFrame = pd.read_csv(CLUSTER2_DIRECTORY, delimiter="\t")
            self.queries: pd.Series = self.raw_df["query"]
    return (Data,)


@app.cell
def _(Data):
    data = Data()
    return


if __name__ == "__main__":
    app.run()
