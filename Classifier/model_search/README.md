First I’ll verify the baseline model makes sense and tune it to optimal point
- [x] Analyze baseline model (the one previously made)
- [ ] Verifying parameters/splits that it learns actually make sense
- [x] Cross-validation for proper performance metrics
- [x] Hyperparameter tuning 
 
Then I will search for a better model than the baseline
- [ ] Model search
- [ ] Different models/architectures
- [ ] All cross-validated and tuned to optimality
- [ ] Diagnosis of learned parameters/splits
 
Now I will explore different features and their encodings 
- [ ] Feature Engineering
- [ ] Predictive power of features to predict class labels (mutual info/Correlation/covariance)
- [ ] Subsets of features (urls and tokens)
- [ ] unigrams/bigrams/trigrams
- [ ] Different encoding methods (BOW/tf-idf/word embeddings)
 
For each possible combination of features I will look into the structure of the feature space to see if it coincides with my understanding of the data
- [ ] Cluster Analysis of Feature Space 
- [ ] Try different number of clusters and evaluate strength of results (for example, ideally 2 clusters should actually give some meaningful output. Similarly k=num_queries should also be informative)
- [ ] Investigate if the groups have some bearing on the actual labels or domain information that we have (might have some link with the different queries used to obtain videos)
 
Some random ideas I have which don’t fall into a specific bucket
- [ ] Looking at how sensitive the analysis results are to changes in magic numbers like arbitrary thresholds (50% flagged videos in a channel flags the channel, maybe we should use 20% 🤷‍)
- [ ] Maybe using smaller bootstrapped samples to train a lot of models on the smaller dataset and see performance on the bigger one. Maybe we don’t need to train a stable model on the whole smaller dataset, Might also provide an estimate of the variance of the model. (I’m a bit iffy on this idea since we are already using a bagging based model which kind of does something similar and this analysis could be done in the model search part too.)
