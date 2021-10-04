# -*- coding: utf-8 -*-
"""digitrecognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eMhJ2sfrSrtZvntONbdeBofJQZd2WS8z
"""

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)


train = pd.read_csv('C:\\Users\\User\\PycharmProjects\\pythonProject2\\train.csv').to_numpy()[:, 1:].T
train_labels = pd.read_csv('C:\\Users\\User\\PycharmProjects\\pythonProject2\\train.csv', usecols=[0]).to_numpy().reshape((1, -1))
test = pd.read_csv('C:\\Users\\User\\PycharmProjects\\pythonProject2\\test.csv').to_numpy().T

print(train.shape, train_labels.shape, test.shape)


# GRADED CLASS: Sigmoid

class Sigmoid:
    def __call__(self, z):
        """
        Compute the sigmoid of z

        Arguments:
        z -- scalar or numpy array of any size.

        Return:
        sigmoid(z)
        """
        return 1 / (1 + np.exp(-z))

    def prime(self, z):
        """
        Compute the derivative of sigmoid of z

        Arguments:
        z -- scalar or numpy array of any size.

        Return:
        Sigmoid prime
        """
        return self.__call__(z) * (1 - self.__call__(z))


def one_hot(Y, n_classes):
    """
    Encode labels into a one-hot representation

    Arguments:
    Y -- array of input labels of shape (1, n_samples)
    n_classes -- number of classes

    Returns:
    onehot, a matrix of labels by samples. For each column, the ith index will be
        "hot", or 1, to represent that index being the label; shape - (n_classes, n_samples)
    """

    matrix = np.zeros((n_classes, Y.shape[1]))
    for i in range(n_classes):
        matrix[i, np.argwhere(Y == i)[:, 1]] = 1

    return matrix


def compute_cost(A2, Y):
    """
    Computes the cross-entropy cost given in equation (4)

    Arguments:
    A2 -- sigmoid output of the hidden layer activation, of shape (classes, n_examples)
    Y -- labels of shape (classes, n_examples)

    Returns:
    cost -- cross-entropy cost given equation (4)
    """

    m = Y.shape[1]  # number of examples

    # Compute the cross-entropy cost
    ### START CODE HERE ###
    cost = np.sum(Y * np.log(A2) + (1 - Y) * np.log(1 - A2)) / -m
    ### END CODE HERE ###

    return cost


class Regularization:
    """
    Regularization class

    Arguments:
    lambda_1 -- regularization coeficient for l1 regularization
    lambda_2 -- regularization coeficient for l2 regularization
    """

    def __init__(self, lambda_1, lambda_2):
        self.lambda_1 = lambda_1
        self.lambda_2 = lambda_2

    def l1(self, W1, W2, m):
        """
        Compute l1 regularization part

        Arguments:
        W1 -- weigts of shape (n_hidden_units, n_features)
        W2 -- weigts of shape (output_size, n_hidden_units)
        m -- n_examples

        Returns:
        l1_term -- float, check formula (6)
        """
        ### START CODE HERE ###
        return (self.lambda_1 / (m)) * (np.linalg.norm(W1, ord=1) + np.linalg.norm(W2, ord=1))
        ### END CODE HERE ###

    def l1_grad(self, W1, W2, m):
        """
        Compute l1 regularization term

        Arguments:
        W1 -- weigts of shape (n_hidden_units, n_features)
        W2 -- weigts of shape (output_size, n_hidden_units)
        m -- n_examples

        Returns:
         dict with l1_grads "dW1" and "dW2"
            which are grads by corresponding weights
        """
        ### START CODE HERE ###
        return dict(dW1=self.lambda_1 / (m) * np.sign(W1), dW2=self.lambda_1 / (m) * np.sign(W2))
        ### END CODE HERE ###

    def l2(self, W1, W2, m):
        """
        Compute l2 regularization term

        Arguments:
        W1 -- weigts of shape (n_hidden_units, n_features)
        W2 -- weigts of shape (output_size, n_hidden_units)
        m -- n_examples

        Returns:
        l2_term: float, check formula (6)
        """
        ### START CODE HERE ###
        return (self.lambda_2 / (2 * m)) * (np.linalg.norm(W1, ord=2) ** 2 + np.linalg.norm(W2, ord=2) ** 2)
        ### END CODE HERE ###

    def l2_grad(self, W1, W2, m):
        """
        Compute l2 regularization term

        Arguments:
        W1 -- weigts of shape (n_hidden_units, n_features)
        W2 -- weigts of shape (output_size, n_hidden_units)
        m -- n_examples

        Returns:
        l2_grads: dict with keys "dW1" and "dW2"
        """
        ### START CODE HERE ###
        return dict(dW1=self.lambda_2 * W1 / (m), dW2=self.lambda_2 * W2 / (m))
        ### END CODE HERE ###


# GRADED CLASS NeuralNetwork

class NeuralNetwork:
    """
    Arguments:
    n_features: int -- Number of features
    n_hidden_units: int -- Number of hidden units
    n_classes: int -- Number of classes
    learning_rate: float
    reg: instance of Regularization class
    """

    def __init__(self, n_features, n_hidden_units, n_classes, learning_rate, reg=Regularization(0.1, 0.2),
                 sigm=Sigmoid()):
        self.n_features = n_features
        self.n_classes = n_classes
        self.learning_rate = learning_rate
        self.n_hidden_units = n_hidden_units
        self.reg = reg
        self.sigm = sigm
        self.W1 = None
        self.b1 = None
        self.W2 = None
        self.b2 = None

        self.initialize_parameters()

    def initialize_parameters(self):
        """
        W1 -- weight matrix of shape (self.n_hidden_units, self.n_features)
        b1 -- bias vector of shape (self.n_hidden_units, 1)
        W2 -- weight matrix of shape (self.n_classes, self.n_hidden_units)
        b2 -- bias vector of shape (self.n_classes, 1)
        """
        np.random.seed(42)

        ### START CODE HERE ###
        self.W1 = np.random.normal(0, 0.01, size=(self.n_hidden_units, self.n_features))
        self.b1 = np.zeros((self.n_hidden_units, 1))
        self.W2 = np.random.normal(0, 0.01, size=(self.n_classes, self.n_hidden_units))
        self.b2 = np.zeros((self.n_classes, 1))
        ### END CODE HERE ###

    def forward_propagation(self, X):
        """
        Arguments:
        X -- input data of shape (number of features, number of examples)

        Returns:
        dictionary containing "Z1", "A1", "Z2" and "A2"
        """
        # Implement Forward Propagation to calculate A2 (probabilities)
        ### START CODE HERE ###
        Z1 = np.dot(self.W1, X) + self.b1
        A1 = self.sigm(Z1)
        Z2 = np.dot(self.W2, A1) + self.b2
        A2 = self.sigm(Z2)
        ### END CODE HERE ###

        return {
            'Z1': Z1,
            'A1': A1,
            'Z2': Z2,
            'A2': A2
        }

    def backward_propagation(self, X, Y, cache):
        """
        Arguments:
        X -- input data of shape (number of features, number of examples)
        Y -- one-hot encoded vector of labels with shape (n_classes, n_samples)
        cache -- a dictionary containing "Z1", "A1", "Z2" and "A2"

        Returns:
        dictionary containing gradients "dW1", "db1", "dW2", "db2"
        """
        m = X.shape[1]

        # Retrieve A1 and A2 from dictionary "cache".
        ### START CODE HERE ###
        A1, A2 = cache['A1'], cache['A2']
        ### END CODE HERE ###

        # Calculate gradients for L1, L2 parts using attribute instance of Regularization class
        ### START CODE HERE ###
        l1_grad, l2_grad = self.reg.l1_grad(self.W1, self.W2, m), self.reg.l2_grad(self.W1, self.W2, m)
        ### END CODE HERE ###

        # Backward propagation: c`alculate dW1, db1, dW2, db2 (using obtained L1, L2 gradients)
        ### START CODE HERE ###
        dZ2 = A2 - Y
        dW2 = np.dot(dZ2, A1.T) / m + l1_grad['dW2'] + l2_grad['dW2']
        db2 = np.sum(dZ2, axis=1, keepdims=True) / m
        dZ1 = np.dot(self.W2.T, dZ2) * self.sigm.prime(cache['Z1'])
        dW1 = np.dot(dZ1, X.T) / m + l1_grad['dW1'] + l2_grad['dW1']
        db1 = np.sum(dZ1, axis=1, keepdims=True) / m
        ### END CODE HERE ###

        return {
            'dW1': dW1,
            'db1': db1,
            'dW2': dW2,
            'db2': db2
        }

    def update_parameters(self, grads):
        """
        Updates parameters using the gradient descent update rule

        Arguments:
        grads -- python dictionary containing gradients "dW1", "db1", "dW2", "db2"
        """

        # Retrieve each gradient from the dictionary "grads"
        ### START CODE HERE ###
        dW1 = grads['dW1']
        dW2 = grads['dW2']
        db1 = grads['db1']
        db2 = grads['db2']
        ## END CODE HERE ###

        # Update each parameter
        ### START CODE HERE ###
        self.W1 = self.W1 - self.learning_rate * dW1
        self.W2 = self.W2 - self.learning_rate * dW2
        self.b1 = self.b1 - self.learning_rate * db1
        self.b2 = self.b2 - self.learning_rate * db2
        ### END CODE HERE ###


# GRADED CLASS NNClassifier

class NNClassifier:
    """
    NNClassifier class

    Arguments:
    model -- instance of NN
    epochs: int -- Number of epochs
    """

    def __init__(self, model, epochs=0):
        self.model = model
        self.epochs = epochs
        self._cost = []  # Collect values of cost function after each epoch to build graph later

    def fit(self, X, Y):
        """
        Learn weights and errors from training data

        Arguments:
        X -- input data of shape (number of features, number of examples)
        Y -- labels of shape (1, number of examples)
        """

        # Don't forget to one_hot encode Y before learn
        # After each epoch compute self._cost for plotting later
        ### START CODE HERE ###

        cache = self.model.forward_propagation(X)
        grads = self.model.backward_propagation(X, one_hot(Y, 10), cache)
        self.model.update_parameters(grads)
        self._cost.append(compute_cost(cache['A2'], one_hot(Y, 10)))

        while self._cost[-1] >= 0.9:
            cache = self.model.forward_propagation(X)
            grads = self.model.backward_propagation(X, one_hot(Y, 10), cache)
            self.model.update_parameters(grads)
            self._cost.append(compute_cost(cache['A2'], one_hot(Y, 10)))

            if self.epochs % 100 == 0:
                print(self._cost[-1])


        ### END CODE HERE ###

    def predict(self, X):
        """
        Generate array of predicted labels for the input dataset

        Arguments:
        X -- input data of shape (number of features, number of examples)

        Returns:
        predicted labels of shape (1, n_samples)
        """

        ### START CODE HERE ### (≈ 1 line of code)
        cache = self.model.forward_propagation(X)
        ### END CODE HERE ###

        return np.argmax(cache['A2'], axis=0).T


def accuracy(pred, labels):
    return (np.sum(pred == labels, axis=1) / float(labels.shape[1]))[0]


NN = NeuralNetwork(784, 300, 10, 0.1)
classifier = NNClassifier(NN)  #
classifier.fit(train, train_labels)

pred_train = classifier.predict(train)
pred_test = classifier.predict(test)

print('train set accuracy: ', accuracy(pred_train, train_labels))

test_labels = open('C:\\Users\\User\\PycharmProjects\\pythonProject2\\test_labels.csv', 'w+')

result = pd.DataFrame(pred_test, columns=['Label'])
result.index += 1

print(result.shape)
# print(result)

result.to_csv(test_labels, index_label='ImageId')

# test_labels.close()