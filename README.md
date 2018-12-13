# A Prediction System for Movie Revenue
CSCI 5502 Data Mining Final Project

## Structure
* **datasets**: store all csv files generated from original TMDb datasets
* **notebook**: Jupyter notebooks. Mainly used for analyzing correlations between attributes
* **src**: source Python 3 files of the system

## Environment & Dependency
* Python 3
* Pandas
* scikit-learn
* Matplot
* [TMDb datasets](https://www.kaggle.com/tmdb/tmdb-movie-metadata) in the directory `datasets`

## How to run the system
The main program is `movie_revenue_predictor.py`. You need to execute this program in the directory `Movie_Revenue_Predictor`. Then, the program can be executed by the instruction `python3 src/movie_revenue_predictor.py`.

### Diagram
![](https://raw.githubusercontent.com/Sayter99/Movie_Revenue_Predictor/master/key_result/diagram/movie_revenue_predictor_diagram.png)

### Parameters
There are paramters can be changed to conduct different tests.

```Python
classification_method = 1 # 0: single classifier 1: boosting
plotting = False # plotting classification result or not
evaluation_method = 0 # 0: classification error 1: RMSE
test_times = 10 # how many rounds of tests
```