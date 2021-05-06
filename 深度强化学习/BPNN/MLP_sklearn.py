from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import numpy as np
from math import exp

#############################################################
X, y = make_classification(n_samples=100, random_state=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)


clf = MLPClassifier(random_state=1, max_iter=300).fit(X_train, y_train)

pred_proba = clf.predict_proba(X_test[:1])
pred_result = clf.predict(X_test[:25, :])
score = clf.score(X_test, y_test)

# plot

dashes = [10, 5, 100, 5]  # 10 points on, 5 off, 100 on, 5 off
fig, ax = plt.subplots()
line1, = ax.plot(range(25), y_test, '--', linewidth=2, label='测试数据')
line1.set_dashes(dashes)
line2, = ax.plot(range(25), pred_result, dashes=[30, 5, 10, 5], label='输出数据')
ax.legend(loc='lower right')
#设置字体为楷体
plt.rcParams['font.sans-serif'] = ['KaiTi']
#plt.show()

##############################################
file_name = '..\wheat-seeds.csv'
tmp = np.loadtxt(file_name, dtype=np.float16, delimiter=",")

train_data_input = tmp[:,:7]
train_data_output = tmp[:,7]

test_data_input = tmp[150:210,:7]
test_data_output = tmp[150:210,7]

clf1 = MLPClassifier(random_state=1, max_iter=3000).fit(train_data_input, train_data_output)
pred_proba1 = clf1.predict_proba(test_data_input)
pred_result1 = clf1.predict(test_data_input)
score1 = clf1.score(test_data_input, test_data_output)
