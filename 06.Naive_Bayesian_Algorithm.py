'''
Question: Write a program to implement the naïve Bayesian classifier for a sample training data set stored as a .CSV file. Compute the accuracy of the classifier, considering few test data sets.

'''


import csv
import random
import math


def loadcsv(filename):
    lines = csv.reader(open(filename, "r"))
    dataset = list(lines)
    for i in range(len(dataset)):
        # converting strings into numbers for processing
        dataset[i] = [float(x) for x in dataset[i]]

    return dataset


def splitdataset(dataset, splitratio):
    # split according to splitratio
    trainsize = int(len(dataset) * splitratio)
    trainset = []
    copy = list(dataset)
    while len(trainset) < trainsize:
        # generate indices for the dataset list randomly to pick ele for training data
        index = random.randrange(len(copy))
        trainset.append(copy.pop(index))
    return [trainset, copy]


def separatebyclass(dataset):
    separated = {}  # dictionary of classes 1 and 0
    # creates a dictionary of classes 1 and 0 where the values are
    # the instances belonging to each class
    for i in range(len(dataset)):
        vector = dataset[i]
        if vector[-1] not in separated:
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    print(separated)
    return separated


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


def summarize(dataset):  # creates a dictionary of classes
    summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
    del summaries[-1]  # excluding labels +ve or -ve
    return summaries


def summarizebyclass(dataset):
    separated = separatebyclass(dataset)
    # print(separated)
    summaries = {}
    for classvalue, instances in separated.items():
        # for key,value in dic.items()
        # summaries is a dic of tuples(mean,std) for each class value
        summaries[classvalue] = summarize(
            instances
        )  # summarize is used to cal to mean and std
    return summaries


def calculateprobability(x, mean, stdev):
    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stdev, 2))))
    return (1 / (math.sqrt(2 * math.pi) * stdev)) * exponent


def calculateclassprobabilities(summaries, inputvector):
    probabilities = {}  # probabilities contains the all prob of all class of test data
    for (
        classvalue,
        classsummaries,
    ) in summaries.items():  # class and attribute information as mean and sd
        probabilities[classvalue] = 1
        for i in range(len(classsummaries)):
            mean, stdev = classsummaries[
                i
            ]  # take mean and sd of every attribute for class 0 and 1 seperaely
            x = inputvector[i]  # testvector's first attribute
            probabilities[classvalue] *= calculateprobability(x, mean, stdev)
            # use normal dist
    return probabilities


def predict(summaries, inputvector):  # training and test data is passed
    probabilities = calculateclassprobabilities(summaries, inputvector)
    bestLabel, bestProb = None, -1
    for (
        classvalue,
        probability,
    ) in probabilities.items():  # assigns that class which has he highest prob
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classvalue
    return bestLabel


def getpredictions(summaries, testset):
    predictions = []
    for i in range(len(testset)):
        result = predict(summaries, testset[i])
        predictions.append(result)
    return predictions


def getaccuracy(testset, predictions):
    correct = 0
    for i in range(len(testset)):
        if testset[i][-1] == predictions[i]:
            correct += 1
    return (correct / float(len(testset))) * 100.0


def main():
    filename = "ConceptLearning.csv"
    splitratio = 0.76
    dataset = loadcsv(filename)

    trainingset, testset = splitdataset(dataset, splitratio)
    print(
        "Split {0} rows into train={1} and test={2} rows".format(
            len(dataset), len(trainingset), len(testset)
        )
    )
    # prepare model
    summaries = summarizebyclass(trainingset)
    # print(summaries)
    # test model
    predictions = getpredictions(
        summaries, testset
    )  # find the predictions of test data with the training data
    accuracy = getaccuracy(testset, predictions)
    print("Accuracy of the classifier is : {0}%".format(accuracy))


main()
