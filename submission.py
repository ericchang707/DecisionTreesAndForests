import numpy as np
from collections import Counter
import time



class DecisionNode:
    """Class to represent a single node in a decision tree."""

    def __init__(self, left, right, decision_function, class_label=None):
        """Create a decision function to select between left and right nodes.
        Note: In this representation 'True' values for a decision take us to
        the left. This is arbitrary but is important for this assignment.
        Args:
            left (DecisionNode): left child node.
            right (DecisionNode): right child node.
            decision_function (func): function to decide left or right node.
            class_label (int): label for leaf node. Default is None.
        """

        self.left = left
        self.right = right
        self.decision_function = decision_function
        self.class_label = class_label

    def decide(self, feature):
        # """Get a child node based on the decision function.͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
        # Args:͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
        #     feature (list(int)): vector for feature.͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
        # Return:͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
        #     Class label if a leaf node, otherwise a child node.͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
        # """͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
        """Determine recursively the class of an input array by testing a value
           against a feature's attributes values based on the decision function.

        Args:
            feature: (numpy array(value)): input vector for sample.

        Returns:
            Class label if a leaf node, otherwise a child node.
        """

        if self.class_label is not None:
            return self.class_label

        elif self.decision_function(feature):
            return self.left.decide(feature)

        else:
            return self.right.decide(feature)


def load_csv(data_file_path, class_index=-1):
    """Load csv data in a numpy array.
    Args:
        data_file_path (str): path to data file.
        class_index (int): slice output by index.
    Returns:
        features, classes as numpy arrays if class_index is specified,
            otherwise all as nump array.
    """

    handle = open(data_file_path, 'r')
    contents = handle.read()
    handle.close()
    rows = contents.split('\n')
    out = np.array([[float(i) for i in r.split(',')] for r in rows if r])

    if(class_index == -1):
        classes= out[:,class_index]
        features = out[:,:class_index]
        return features, classes
    elif(class_index == 0):
        classes= out[:, class_index]
        features = out[:, 1:]
        return features, classes

    else:
        return out


def build_decision_tree():
    """Create a decision tree capable of handling the sample data.
    Tree is built fully starting from the root.

    Returns:
        The root node of the decision tree.
    """

    func0 = lambda feature: feature[0] == 0
    decision_tree_root = DecisionNode(None, None, func0, None)
    decision_tree_root.right = DecisionNode(None, None, None, 1)
    func1 = lambda feature: feature[3] == 0
    decision_tree_root.left = DecisionNode(None, None, func1, None)
    func2 = lambda feature: feature[2] == 1
    func3 = lambda feature: feature[1] == 1
    decision_tree_root.left.right = DecisionNode(None, None, func3, None)
    decision_tree_root.left.left = DecisionNode(None, None, func2, None)
    decision_tree_root.left.right.left = DecisionNode(None, None,None, 0)
    decision_tree_root.left.right.right = DecisionNode(None, None, None, 1)
    decision_tree_root.left.left.right = DecisionNode(None, None, None, 1)
    decision_tree_root.left.left.left = DecisionNode(None, None, None, 0)
    
    return decision_tree_root


def confusion_matrix(classifier_output, true_labels):
    """Create a confusion matrix to measure classifier performance.

    Classifier output vs true labels, which is equal to:
    Predicted  vs  Actual Values.

    Output will in the format:

                        |Predicted|
    |T|                
    |R|    [[true_positive, false_negative],
    |U|    [false_positive, true_negative]]
    |E|

    Args:
        classifier_output (list(int)): output from classifier.
        true_labels: (list(int): correct classified labels.
    Returns:
        A two dimensional array representing the confusion matrix.
    """

    # TODO: finish this.͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
    classifier_output = np.array(classifier_output)
    true_labels = np.array(true_labels)
    true_list = true_labels[classifier_output == true_labels]
    false_list = true_labels[classifier_output != true_labels]
    TruePos = np.sum(np.array(true_list) == 1).astype(float)
    TrueNeg = np.sum(np.array(true_list) == 0).astype(float)
    FalseNeg = np.sum(np.array(false_list) == 1).astype(float)
    FalsePos = np.sum(np.array(false_list) == 0).astype(float)
    confusion_matrix = np.array([[TruePos, FalseNeg], [FalsePos, TrueNeg]])
    return confusion_matrix


def precision(classifier_output, true_labels):
    """Get the precision of a classifier compared to the correct values.
    Precision is measured as:
        true_positive/ (true_positive + false_positive)
    Args:
        classifier_output (list(int)): output from classifier.
        true_labels: (list(int): correct classified labels.
    Returns:
        The precision of the classifier output.
    """

    classifier_output = np.array(classifier_output)
    true_labels = np.array(true_labels)
    true_list = true_labels[classifier_output == true_labels]
    false_list = true_labels[classifier_output != true_labels]
    TruePos = np.sum(np.array(true_list) == 1).astype(float)
    TrueNeg = np.sum(np.array(true_list) == 0).astype(float)
    FalseNeg = np.sum(np.array(false_list) == 1).astype(float)
    FalsePos = np.sum(np.array(false_list) == 0).astype(float)
    return TruePos/(TruePos+FalsePos)


def recall(classifier_output, true_labels):
    """Get the recall of a classifier compared to the correct values.
    Recall is measured as:
        true_positive/ (true_positive + false_negative)
    Args:
        classifier_output (list(int)): output from classifier.
        true_labels: (list(int): correct classified labels.
    Returns:
        The recall of the classifier output.
    """

    classifier_output = np.array(classifier_output)
    true_labels = np.array(true_labels)
    true_list = true_labels[classifier_output == true_labels]
    false_list = true_labels[classifier_output != true_labels]
    TruePos = np.sum(np.array(true_list) == 1).astype(float)
    TrueNeg = np.sum(np.array(true_list) == 0).astype(float)
    FalseNeg = np.sum(np.array(false_list) == 1).astype(float)
    FalsePos = np.sum(np.array(false_list) == 0).astype(float)
    confusion_matrix = np.array([[TruePos, FalseNeg], [FalsePos, TrueNeg]])
    return TruePos/(TruePos+FalseNeg)

def accuracy(classifier_output, true_labels):
    """Get the accuracy of a classifier compared to the correct values.
    Accuracy is measured as:
        correct_classifications / total_number_examples
    Args:
        classifier_output (list(int)): output from classifier.
        true_labels: (list(int): correct classified labels.
    Returns:
        The accuracy of the classifier output.
    """

    classifier_output = np.array(classifier_output)
    true_labels = np.array(true_labels)
    correct_classifications = np.sum(np.array(classifier_output) == np.array(true_labels))
    accuracy = correct_classifications/len(true_labels)
    return accuracy


def gini_impurity(class_vector):
    """Compute the gini impurity for a list of classes.
    This is a measure of how often a randomly chosen element
    drawn from the class_vector would be incorrectly labeled
    if it was randomly labeled according to the distribution
    of the labels in the class_vector.
    It reaches its minimum at zero when all elements of class_vector
    belong to the same class.
    Args:
        class_vector (list(int)): Vector of classes given as 0 or 1.
    Returns:
        Floating point number representing the gini impurity.
    """
    classes = np.array(class_vector)
    if len(class_vector) > 0:
        p_0 = np.mean(classes.astype(float) == 0)
        p_1 = np.mean(classes.astype(float) == 1)
        gini = 1.0 - p_0**2 - p_1**2 + 1e-8
    else:
        gini = 0.0
    return gini




def gini_gain(previous_classes, current_classes):
    """Compute the gini impurity gain between the previous and current classes.
    Args:
        previous_classes (list(int)): Vector of classes given as 0 or 1.
        current_classes (list(list(int): A list of lists where each list has
            0 and 1 values).
    Returns:
        Floating point number representing the information gain.
    """
    
    giniprevious= gini_impurity(previous_classes)
    bob = len(current_classes)
    joe = len(previous_classes)
    gini = giniprevious
    for i in range(bob):
        gini = gini - gini_impurity(current_classes[i]) * len(current_classes[i])/joe

    return float(gini)


class DecisionTree:
    """Class for automatic tree-building and classification."""

    def __init__(self, depth_limit=float('inf')):
        """Create a decision tree with a set depth limit.
        Starts with an empty root.
        Args:
            depth_limit (float): The maximum depth to build the tree.
        """

        self.root = None
        self.depth_limit = depth_limit

    def fit(self, features, classes):
        """Build the tree from root using __build_tree__().
        Args:
            features (m x n): m examples with n features.
            classes (m x 1): Array of Classes.
        """

        self.root = self.__build_tree__(features, classes)


    def __build_tree__(self, features, classes, depth=0):
        """Build tree that automatically finds the decision functions.
        Args:
            features (m x n): m examples with n features.
            classes (m x 1): Array of Classes.
            depth (int): depth to build tree to.
        Returns:
            Root node of decision tree.
        """

        if features.shape[0] <= 1:
            return DecisionNode(None, None, None, classes[0])
        
        if(len(set(classes)) == 1):
            return DecisionNode(None, None, None, classes[0])

        if depth >= self.depth_limit:
            count_class_0, count_class_1 = np.bincount(classes)
            if count_class_1 > count_class_0:   
                return DecisionNode(None, None, None, 1)
            else:
                return DecisionNode(None, None, None, 0)
        
        bestfeat = None
        bestgini = 0.0
        threshold = None
        finalsplit = None
            

            
        for i in range(features.shape[1]):
            step = (max(features[:, i]) - min(features[:, i]))/400.0
            finalsplit = []
            thresholdfinal = float('-inf')
            bestginigain = float('-inf')
            for j in np.arange(min(features[:, i]) + step, max(features[:, i]), step):
                currthreshold = j
                splitdis = np.zeros(len(classes))
                for a in range(len(classes)):
                    if features[a, i] > currthreshold:
                        splitdis[a] = 1
                    else:
                        splitdis[a] = 0
        
                gini = gini_gain(classes, [classes[np.where(splitdis == 0)],
                                                   classes[np.where(splitdis == 1)]])
                if gini > bestginigain:
                    bestginigain = gini
                    thresholdfinal = currthreshold
                    finalsplit = splitdis
            if bestgini < bestginigain:
                bestgini = bestginigain
                bestfeat = i
                threshold = thresholdfinal
                finalsplit = finalsplit
            
                
        if bestgini == 0.0:
            return DecisionNode(None, None, None, classes[0])
        
        
        cvleft = classes[features[:, bestfeat] <= threshold]
        leftfeature = features[features[:, bestfeat] <= threshold]
        cvright = classes[features[:, bestfeat] > threshold]
        rightfeature = features[features[:, bestfeat] > threshold]
        
        func = lambda features: features[bestfeat] <= threshold
        
        currnode = DecisionNode(None, None, func, None)
        currnode.left = self.__build_tree__(leftfeature, cvleft, depth = depth + 1)
        currnode.right = self.__build_tree__(rightfeature, cvright, depth = depth + 1)
        
        return currnode





    def classify(self, features):
        """Use the fitted tree to classify a list of example features.
        Args:
            features (m x n): m examples with n features.
        Return:
            A list of class labels.
        """

        predicted_labels = [self.root.decide(features[i]) for i in range(features.shape[0])]
        return predicted_labels


class RandomForest:
    """Random forest classification."""

    def __init__(self, num_trees, depth_limit, example_subsample_rate,
                 attr_subsample_rate):
        """Create a random forest.
         Args:
             num_trees (int): fixed number of trees.
             depth_limit (int): max depth limit of tree.
             example_subsample_rate (float): percentage of example samples.
             attr_subsample_rate (float): percentage of attribute samples.
        """

        self.trees = []
        self.num_trees = num_trees
        self.depth_limit = depth_limit
        self.example_subsample_rate = example_subsample_rate
        self.attr_subsample_rate = attr_subsample_rate
        self.feature_list = []

    def fit(self, features, classes):
        """Build a random forest of decision trees using Bootstrap Aggregation.
            features (m x n): m examples with n features.
            classes (m x 1): Array of Classes.
        """
        num_samples = len(classes)
        num_subsamples = int(self.example_subsample_rate * num_samples)
        num_feat = len(features[0])
        num_features = int(self.attr_subsample_rate * num_feat)
        for i in range(self.num_trees):
            subfeatindex= np.random.choice(num_samples, num_subsamples, replace = True).reshape(-1, 1)
            subsamp = np.squeeze(features[subfeatindex])
            subfeatsubidx = np.random.choice(num_feat, num_features, replace = False)
            self.feature_list.append(subfeatsubidx)
            subsampfeats = subsamp[:, subfeatsubidx]
            subsampfeats_classes = classes[subfeatindex].astype(int)
            tree = DecisionTree(self.depth_limit)
            tree.fit(subsampfeats, np.squeeze(subsampfeats_classes))
            self.trees.append(tree)


    def classify(self, features):
        """Classify a list of features based on the trained random forest.
        Args:
            features (m x n): m examples with n features.
        """
  
        class_label = []
        for i in range(self.num_trees):
            tree = self.trees[i]
            class_labels = np.array(tree.classify(features[:, self.feature_list[i]])).reshape(-1, 1)
            class_label.append(class_labels)
            
        class_label = np.column_stack(class_label)
        majority_vote= np.mean(class_label, axis=1)
        featurelist = (majority_vote > 0.5).reshape(-1, 1)

        return featurelist



class Vectorization:
    """Vectorization preparation for Assignment 5."""

    def __init__(self):
        pass

    def non_vectorized_loops(self, data):
        """Element wise array arithmetic with loops.
        This function takes one matrix, multiplies by itself and then adds to
        itself.
        Args:
            data: data to be added to array.
        Returns:
            Numpy array of data.
        """

        non_vectorized = np.zeros(data.shape)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                non_vectorized[row][col] = (data[row][col] * data[row][col] +
                                            data[row][col])
        return non_vectorized

    def vectorized_loops(self, data):
        """Element wise array arithmetic using vectorization.
        This function takes one matrix, multiplies by itself and then adds to
        itself.
        Args:
            data: data to be sliced and summed.
        Returns:
            Numpy array of data.
        """

        vectorized = np.multiply(data,data) + data
        return vectorized

    def non_vectorized_slice(self, data):
        """Find row with max sum using loops.
        This function searches through the first 100 rows, looking for the row
        with the max sum. (ie, add all the values in that row together).
        Args:
            data: data to be added to array.
        Returns:
            Tuple (Max row sum, index of row with max sum)
        """

        max_sum = 0
        max_sum_index = 0
        for row in range(100):
            temp_sum = 0
            for col in range(data.shape[1]):
                temp_sum += data[row][col]

            if temp_sum > max_sum:
                max_sum = temp_sum
                max_sum_index = row

        return max_sum, max_sum_index

    def vectorized_slice(self, data):
        """Find row with max sum using vectorization.
        This function searches through the first 100 rows, looking for the row
        with the max sum. (ie, add all the values in that row together).
        Args:
            data: data to be sliced and summed.
        Returns:
            Tuple (Max row sum, index of row with max sum)
        """

        sum = np.sum(data, axis = 1)[:100]
        max = np.max(sum)
        maxindex = np.argmax(sum)
        return max, maxindex

    def non_vectorized_flatten(self, data):
        """Display occurrences of positive numbers using loops.
         Flattens down data into a 1d array, then creates a dictionary of how
         often a positive number appears in the data and displays that value.
         ie, [(1203,3)] = integer 1203 appeared 3 times in data.
         Args:
            data: data to be added to array.
        Returns:
            List of occurrences [(integer, number of occurrences), ...]
        """

        unique_dict = {}
        flattened = np.hstack(data)
        for item in range(len(flattened)):
            if flattened[item] > 0:
                if flattened[item] in unique_dict:
                    unique_dict[flattened[item]] += 1
                else:
                    unique_dict[flattened[item]] = 1

        return unique_dict.items()

    def vectorized_flatten(self, data):
        """Display occurrences of positive numbers using vectorization.
         Flattens down data into a 1d array, then creates a dictionary of how
         often a positive number appears in the data and displays that value.
         ie, [(1203,3)] = integer 1203 appeared 3 times in data.
         Args:
            data: data to be added to array.
        Returns:
            List of occurrences [(integer, number of occurrences), ...]
        """

        flatten = np.hstack(data)
        uniquenumber, count = np.unique(flatten, return_counts = True)
        uniquedict = [(uniquenumber[i], count[i]) for i in range(len(uniquenumber)) if uniquenumber[i] > 0 ]
        return uniquedict
    
    
    def non_vectorized_glue(self, data, vector, dimension='c'):
        """Element wise array arithmetic with loops.
        This function takes a multi-dimensional array and a vector, and then combines
        both of them into a new multi-dimensional array. It must be capable of handling
        both column and row-wise additions.
        Args:
            data: multi-dimensional array.
            vector: either column or row vector
            dimension: either c for column or r for row
        Returns:
            Numpy array of data.
        """
        if dimension == 'c' and len(vector) == data.shape[0]:
            non_vectorized = np.ones((data.shape[0],data.shape[1]+1), dtype=float)
            non_vectorized[:, -1] *= vector
        elif dimension == 'r' and len(vector) == data.shape[1]:
            non_vectorized = np.ones((data.shape[0]+1,data.shape[1]), dtype=float)
            non_vectorized[-1, :] *= vector
        else:
            raise ValueError('This parameter must be either c for column or r for row')
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                non_vectorized[row, col] = data[row, col]
        return non_vectorized

    def vectorized_glue(self, data, vector, dimension='c'):
        """Array arithmetic without loops.
        This function takes a multi-dimensional array and a vector, and then combines
        both of them into a new multi-dimensional array. It must be capable of handling
        both column and row-wise additions.
        Args:
            data: multi-dimensional array.
            vector: either column or row vector
            dimension: either c for column or r for row
        Returns:
            Numpy array of data.
            
        """
        if dimension == 'c':
            vectorized = np.column_stack((data, vector))
        else:
            vectorized = np.row_stack((data,vector))
        return vectorized

    def non_vectorized_mask(self, data, threshold):
        """Element wise array evaluation with loops.
        This function takes a multi-dimensional array and then populates a new
        multi-dimensional array. If the value in data is below threshold it
        will be squared.
        Args:
            data: multi-dimensional array.
            threshold: evaluation value for the array if a value is below it, it is squared
        Returns:
            Numpy array of data.
        """
        non_vectorized = np.zeros_like(data, dtype=float)
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                val = data[row, col]
                if val >= threshold:
                    non_vectorized[row, col] = val
                    continue
                non_vectorized[row, col] = val**2

        return non_vectorized

    def vectorized_mask(self, data, threshold):
        """Array evaluation without loops.
        This function takes a multi-dimensional array and then populates a new
        multi-dimensional array. If the value in data is below threshold it
        will be squared. You are required to use a binary mask for this problem
        Args:
            data: multi-dimensional array.
            threshold: evaluation value for the array if a value is below it, it is squared
        Returns:
            Numpy array of data.
        """
        vectorized = np.where((data < threshold), data * data, data)
        return vectorized

def return_your_name():
    # return your name͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
    # TODO: finish this͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄈͏︀͏︆
    return("Eric Chang")
