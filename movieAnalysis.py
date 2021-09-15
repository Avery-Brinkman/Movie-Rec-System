from sklearn import tree
from sklearn.datasets import load_iris

iris = load_iris()

x = iris.data
y = iris.target

clf  = tree.DecisionTreeClassifier()

clf.fit(x, y)

tree.plot_tree(clf)