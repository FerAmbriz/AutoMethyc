# Comparative
## PCA
To reduce data dimensionality, we performed a principal component analysis (PCA) to identify the axes of greatest variation and assess differential clustering between samples and normal controls. The results are provided in the file CSV/pca_vectors.csv.


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
