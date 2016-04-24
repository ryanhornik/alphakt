import csv

import os

from pybrain.datasets import SupervisedDataSet
from pybrain.structure import FeedForwardNetwork, FullConnection, LinearLayer, SigmoidLayer


def main():
    nn = build_nn()
    ds = build_data()


if __name__ == "__main__":
    main()


def build_nn():
    nn = FeedForwardNetwork()

    # 24 columns per dataset  with bins 34
    in_layer = LinearLayer(24)
    hidden_layer = SigmoidLayer(12)
    out_layer = LinearLayer(1)

    in_to_hidden = FullConnection(in_layer, hidden_layer)
    hidden_to_out = FullConnection(hidden_layer, out_layer)

    nn.addConnection(in_to_hidden)
    nn.addConnection(hidden_to_out)

    nn.sortModules()

    return nn


def build_data(directory):
    ds = SupervisedDataSet(24, 1)
    for f in os.listdir(directory):
        fin = open(directory + f, 'r')
        csv_in = csv.DictReader(fin)

        for row in csv_in:
            ds.addSample(
                (row[''])
            )

    return ds
