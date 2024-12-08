# Comparative
## PCA
To reduce the dimensionality of the data, we did an analysis of
principal components, see the axes of greatest variation and see if
there is a differential grouping between the samples and normals. The
output is in 'CSV/pca_vectors.csv0


## Differential methylation

Differential methylation was made on the comparison of cases and
controls, with a implementation of shapiro wilk test, and t-student or
The Mann-Whitney U test in each site.

## ROC

For Receiver Operating Characteristic (ROC) analysis, the best
combination of sites that allows separation between controls and cases
is identified in an unsupervised manner, where possible combinations
between the sites with the highest number of outliers are performed,
followed by the prediction evaluation using a logistic regression model.
Finally, the ROC curve analysis is performed, evaluating the best
combination.
