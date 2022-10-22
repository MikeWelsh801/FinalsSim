import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def load_from_file(file):
    # load the data from url csv
    df = pd.read_csv(file, header=0)
    df = df.sample(frac=1).reset_index(drop=True)
    df.head()

    # Parse csv and store into variables
    X = df[["VFG","VFGA","VFG%","V3P","V3PA","V3P%","V2P","V2PA","V2P%",
            "VFT","VFTA","VFT%","VORB","VDRB","VTRB","VAST","VSTL","VBLK",
            "VTOV","VPF","VPTS","VFG Opp","VFGA Opp","VFG% Opp","V3P Opp",
            "V3PA Opp","V3P% Opp","V2P Opp","V2PA Opp","V2P% Opp","VFT Opp",
            "VFTA Opp","VFT% Opp","VORB Opp","VDRB Opp","VTRB Opp","VAST Opp",
            "VSTL Opp","VBLK Opp","VTOV Opp","VPF Opp","VPTS Opp","HFG","HFGA",
            "HFG%","H3P","H3PA","H3P%","H2P","H2PA","H2P%","HFT","HFTA","HFT%",
            "HORB","HDRB","HTRB","HAST","HSTL","HBLK","HTOV","HPF","HPTS",
            "HFG Opp","HFGA Opp","HFG% Opp","H3P Opp","H3PA Opp","H3P% Opp",
            "H2P Opp","H2PA Opp","H2P% Opp","HFT Opp","HFTA Opp","HFT% Opp",
            "HORB Opp","HDRB Opp","HTRB Opp","HAST Opp","HSTL Opp","HBLK Opp",
            "HTOV Opp","HPF Opp","HPTS Opp"]].values
    y = df["Home/Away Wins"].values
    print("X: ", np.shape(X))
    print("y: ", np.shape(y))
    return df, X, y


# Plots the data
def plot(X, y, title):
    plt.title(title)
    colors = {"H": "red", "A": "blue"}
    plt.scatter(X[:, 2], X[:, 44], c=[colors[_y] for _y in y], edgecolors="k", s=25)
    plt.show()
