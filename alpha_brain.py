import csv

from multiprocessing import Process

import os

from statistics import pstdev, mean

from numpy import random as nrand, sqrt

from pybrain.datasets import SupervisedDataSet
from pybrain.tools.customxml import NetworkWriter, NetworkReader
from pybrain.tools.shortcuts import buildNetwork

from constants import input_columns, normalized_columns, nominal_columns
from pybrain.supervised import BackpropTrainer, RPropMinusTrainer


def check(nn, csv_in):
    for row in csv_in:
        inputs = tuple(map(lambda x: row[x], input_columns))
        if '' in inputs or row['8hr_score'] == '':
            continue
        print('Guessed: {}\nActual: {}'.format(nn.activate(inputs), row['8hr_score']))


def build_nn():
    print("Building nn")
    nn = buildNetwork(len(input_columns), 12, 1)
    return nn


def read_and_transform_data(directory):
    input_rows = []
    for f in os.listdir(directory):
        fin = open(directory + f, 'r')
        csv_in = csv.DictReader(fin)

        blanks = 0
        for row in csv_in:
            inputs = {k: row[k] for k in input_columns}
            inputs['8hr_score'] = row['8hr_score']
            if '' in inputs.values():
                blanks += 1
                continue
            input_rows.append(inputs)

        print("Finished File, {} blanks".format(blanks))

    normalize(input_rows)
    map_nominal_values(input_rows)

    return input_rows


def build_data(directory):
    print("Building data")
    ds = SupervisedDataSet(len(input_columns), 1)

    input_rows = read_and_transform_data(directory)

    for row in input_rows:
        ds.addSample(get_input_tuple(row), row['8hr_score'], )

    return ds


def normalize(input_rows):
    stats = {'mean': {}, 'sd': {}}
    for col in normalized_columns:
        column_list = [int(data[col]) for data in input_rows]
        stats['mean'][col] = mean(column_list)
        stats['sd'][col] = pstdev(column_list, mu=stats['mean'][col])

    for row in input_rows:
        for col in normalized_columns:
            if stats['sd'][col] == 0:
                row[col] = 0
            else:
                row[col] = (int(row[col]) - stats['mean'][col]) / stats['sd'][col]


def map_nominal_values(input_rows):
    nominal_value_maps = {}
    for col in nominal_columns:
        nominal_values = {row[col] for row in input_rows}
        nominal_value_maps[col] = {val: i for i, val in enumerate(nominal_values)}

    for col in nominal_columns:
        for row in input_rows:
            row[col] = nominal_value_maps[col][row[col]]


def get_all(directory):
    nn = build_nn()
    ds = build_data(directory)
    trainer = BackpropTrainer(nn, ds)
    return nn, ds, trainer


def train_n_nn(n, ds):
    datasets = list(n_datasets(ds, 7, max_items=200000))

    p3 = Process(target=train_rprop, args=('p3', datasets[0]))
    p3.start()

    p4_1 = Process(target=train_rprop, args=('p4', datasets[1]),
                   kwargs={'etaminus': 0.8, 'etaplus': 1.5})
    p4_1.start()
    p4_2 = Process(target=train_rprop, args=('p4', datasets[2]),
                   kwargs={'etaminus': 1, 'etaplus': 1.7})
    p4_2.start()
    p4_3 = Process(target=train_rprop, args=('p4', datasets[3]),
                   kwargs={'etaminus': 0.65, 'etaplus': 1.3})
    p4_3.start()

    p6_1 = Process(target=train_rprop, args=('p6', datasets[4]),
                   kwargs={'delta0': 0.5})
    p6_1.start()
    p6_2 = Process(target=train_rprop, args=('p6', datasets[5]),
                   kwargs={'delta0': 0.3})
    p6_2.start()
    p6_3 = Process(target=train_rprop, args=('p6', datasets[6]),
                   kwargs={'delta0': 0.7})
    p6_3.start()


def train_backprop(name, ds, rate):
    nn = build_nn()
    trainer = BackpropTrainer(nn, ds, learningrate=rate)
    print("Training nn (BPROP) - {} examples".format(rate, len(ds)))
    trainer.trainUntilConvergence()
    NetworkWriter.writeToFile(nn, '{}_B_NeuralNet.xml'.format(name, rate))


def train_rprop(name, ds, etaminus=0.5, etaplus=1.2, deltamin=1e-06, deltamax=5.0, delta0=0.1):
    nn = build_nn()
    trainer = RPropMinusTrainer(nn, dataset=ds, etaminus=etaminus, etaplus=etaplus,
                                deltamin=deltamin, deltamax=deltamax, delta0=delta0)
    print("Training nn (RPROP) - {} examples".format(len(ds)))
    trainer.trainUntilConvergence()
    NetworkWriter.writeToFile(nn, '{}_R_NeuralNet.xml'.format(name))


def n_datasets(ds, n=2, max_items=None):
    """Produce n new datasets, each containing 1/n of the original dataset"""
    indicies = nrand.permutation(len(ds))
    separator = int(len(ds) // n)
    if max_items:
        separator = min(separator, max_items)

    indicies_lists = [indicies[x * separator: (x + 1) * separator] for x in range(0, n)]

    data_sets = (SupervisedDataSet(inp=ds['input'][indicies_lists[y]].copy(),
                                   target=ds['target'][indicies_lists[y]]) for y in range(0, n))

    return data_sets


def get_input_tuple(input_row):
    return tuple(input_row[x] for x in input_columns)


def test_on_data(nn, rows, sample=None):
    if isinstance(nn, str):
        nn = NetworkReader.readFrom(nn)

    if isinstance(rows, str):
        test_rows = read_and_transform_data('completed_data/fixed/')
    else:
        test_rows = rows

    if sample:
        test_rows = nrand.permutation(rows)[:sample]

    squared_error_sum = 0
    for r in test_rows:
        result = nn.activate(get_input_tuple(r))
        squared_error_sum += pow(result[0] - int(r['8hr_score']), 2)
    return sqrt(squared_error_sum / len(test_rows))


def main():
    train_n_nn(7, build_data('completed_data/fixed/'))


if __name__ == "__main__":
    main()
