from flask import Flask, request, jsonify, render_template, url_for
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import yaml
from settings import add_RUL_column
from sklearn.model_selection import train_test_split
from feature_selection import RemoveCorrelatedFeatures
from settings import Linear_Regression
import sqlite3
#from config import app 

app = Flask(__name__)


with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/train', methods=['POST'])
def train():

    conn = sqlite3.connect('cmapss_dataset.db')
    c = conn.cursor()
    query = f"""SELECT * FROM cmapss_dataset"""
    c.execute(query)
    data = c.fetchall()
    conn.close()
    col_names = config['col_names']
    #train = pd.DataFrame(data, columns=[col_names])
    

    drop_indices = [col_names.index(label) for label in config['index_names'] + config['setting_names']]
    #X_train = train.drop(columns=drop_labels).copy()

    X_train = np.array([row[:-11] for row in data])
    y_train = np.array([row[-1] for row in data])

    X_train = np.delete(X_train, drop_indices, axis=1)

    X_train, X_test, y_train, y_test = train_test_split(
        #X_train.drop('RUL', axis=1),  # predictor
        #X_train['RUL'],  # target
        X_train, y_train,
        test_size=0.3,  # split
        random_state=0)  # set seed for reproducibility
    
    model = request.form['model']
    selection = request.form['selection']
    if model == 'rf': 
        if selection == 'base': 
            ml_pipe = joblib.load('RF_base.pkl')
        elif selection == 'corr': 
            ml_pipe = joblib.load('RF_correlation.pkl')
        else: 
            return "Invalid selection"
    elif model == 'svr':
        if selection == 'base': 
            ml_pipe = joblib.load('SVR_base.pkl')
        elif selection == 'corr': 
            ml_pipe = joblib.load('SVR_correlation.pkl')
        else: 
            return "Invalid selection"
    elif model == 'lr':
        if selection == 'base': 
            ml_pipe = joblib.load('LR_base.pkl')
        elif selection == "corr":
            ml_pipe = joblib.load('LR_correlation.pkl')
        else: 
            return "Invalid selection"
    else:    
        return "Invalid model"
    
    ml_pipe.fit(X_train, y_train)
    pred_train = ml_pipe.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, pred_train))
    train_r2 = r2_score(y_train, pred_train)
    train_mae = mean_absolute_error(y_train, pred_train)
    pred_test = ml_pipe.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, pred_test))
    test_r2 = r2_score(y_test, pred_test)
    test_mae = mean_absolute_error(y_test, pred_test)
    return render_template('index.html', model = model, selection=selection, train_rmse=train_rmse, train_r2=train_r2, train_mae=train_mae, test_rmse=test_rmse, test_r2=test_r2, test_mae=test_mae)

#testing react + flask communication
@app.route('/score')
def score(): 
    return 

if __name__ == '__main__':
    app.run(debug=True)
