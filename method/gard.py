# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 14:57:03 2017

@author: Administrator
"""
import numpy
import doc_matrix as dm
import figure
X = []
Y = []
def matrix_factorisation(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    global X
    global Y
    Q = Q.T
    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i, :], Q[:, j])
                    for k in range(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P, Q)
        e = 0
        t = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i, :], Q[:, j]), 2)
                    for k in range(K):
                        t = t + (beta / 2) * (pow(P[i][k], 2) + pow(Q[k][j], 2))
                        e = e + t
        print 'zui:',t
        print 'loss',e
        if(step>200):
            X.append(step)
            Y.append(e)
        if step > 4000:
            figure.paint1(X, Y)
            break
    return P, Q.T
if __name__ == '__main__':
    C = dm.getMatrix('tp_风湿科')
    R = numpy.array(C)
    d = R.shape
    U = numpy.random.rand(d[0],10)
    V = numpy.random.rand(d[1],10)
    nP, nQ = matrix_factorisation(R, U, V, 10)
    nR = numpy.dot(nP, nQ.T)
    print(nR)

