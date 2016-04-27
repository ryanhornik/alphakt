import csv

import os
from numpy import random

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.shortcuts import buildNetwork

from constants import input_columns
from pybrain.supervised import BackpropTrainer


def check(nn, csv_in):
    for row in csv_in:
        inputs = tuple(map(lambda x: row[x], input_columns))
        if '' in inputs or row['8hr_score'] == '':
            continue
        print('Guessed: {}\nActual: {}'.format(nn.activate(inputs), row['8hr_score']))


def build_nn():
    print("Building nn")
    nn = buildNetwork(len(input_columns), 12, 1)
    # nn = FeedForwardNetwork()
    #
    # # 24 columns per dataset  with bins 34
    # in_layer = LinearLayer(len(input_columns))
    # hidden_layer = SigmoidLayer(12)
    # out_layer = LinearLayer(1)
    #
    # nn.addInputModule(in_layer)
    # nn.addModule(hidden_layer)
    # nn.addOutputModule(out_layer)
    #
    # in_to_hidden = FullConnection(in_layer, hidden_layer)
    # hidden_to_out = FullConnection(hidden_layer, out_layer)
    #
    # nn.addConnection(in_to_hidden)
    # nn.addConnection(hidden_to_out)
    #
    # nn.sortModules()

    return nn


def build_data(directory):
    print("Building data")
    ds = SupervisedDataSet(len(input_columns), 1)
    for f in os.listdir(directory):
        fin = open(directory + f, 'r')
        csv_in = csv.DictReader(fin)

        blanks = 0
        for row in csv_in:
            inputs = tuple(map(lambda x: row[x], input_columns))
            if '' in inputs or row['8hr_score'] == '':
                blanks += 1
                continue
            ds.addSample(inputs, (row['8hr_score'],))
        print("Finished File, {} blanks".format(blanks))

    return ds


def get_all(directory):
    nn = build_nn()
    ds = build_data(directory)
    trainer = BackpropTrainer(nn, ds)
    return nn, ds, trainer


def main():
    nn = build_nn()
    ds = build_data('completed_data/fixed/')

    trainer = BackpropTrainer(nn, ds)
    print("Training nn")
    trainer.trainUntilConvergence(verbose=True)


def n_datasets(ds, n=2):
    """Produce n new datasets, each containing 1/n of the original dataset"""
    indicies = random.permutation(len(ds))
    separator = int(len(ds) // n)

    indicies_lists = [indicies[x*separator: (x+1)*separator] for x in range(0, n)]

    data_sets = (SupervisedDataSet(inp=ds['input'][indicies_lists[y]].copy(),
                                   target=ds['target'][indicies_lists[y]]) for y in range(0, n))

    return data_sets


if __name__ == "__main__":
    main()
