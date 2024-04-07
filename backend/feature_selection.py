from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class RemoveCorrelatedFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.65):
        self.threshold = threshold
        self.correlated_features = None

    def fit(self, X, y=None):
        correlation_matrix = np.corrcoef(X,y, rowvar=False)
        highly_correlated_mask = np.abs(correlation_matrix) > self.threshold
        upper_triangle_mask = np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
        highly_correlated_mask = highly_correlated_mask & upper_triangle_mask
        correlated_pairs = np.where(highly_correlated_mask)
        self.correlated_features = set()
        for feature1, feature2 in zip(*correlated_pairs):
            if feature1 not in self.correlated_features and feature2 not in self.correlated_features:
                correlation1 = correlation_matrix[feature1, feature2]
                correlation2 = correlation_matrix[feature2, feature1]
                if correlation1 > correlation2:
                    self.correlated_features.add(feature2)
                else:
                    self.correlated_features.add(feature1)
        return self

    def transform(self, X):
        return np.delete(X, list(self.correlated_features), axis=1)