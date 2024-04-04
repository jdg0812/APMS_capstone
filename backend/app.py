from flask import Flask, request, jsonify, render_template, url_for
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import yaml
from settings import add_RUL_column
from sklearn.model_selection import train_test_split
import sqlite3
from config import app 


with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

model = joblib.load('base_rf_pipe.joblib')


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
    train = pd.DataFrame(data, columns=[col_names])
    

    drop_labels = config['index_names']+config['setting_names']
    X_train = train.drop(columns=drop_labels).copy()

    X_train, X_test, y_train, y_test = train_test_split(
        X_train.drop('RUL', axis=1),  # predictor
        X_train['RUL'],  # target
        test_size=0.3,  # split
        random_state=0)  # set seed for reproducibility
    
    model.fit(X_train, y_train)
    pred_train = model.predict(X_train)
    train_rmse = np.sqrt(mean_squared_error(y_train, pred_train))
    train_r2 = r2_score(y_train, pred_train)
    train_mae = mean_absolute_error(y_train, pred_train)
    pred_test = model.predict(X_test)
    test_rmse = np.sqrt(mean_squared_error(y_test, pred_test))
    test_r2 = r2_score(y_test, pred_test)
    test_mae = mean_absolute_error(y_test, pred_test)
    return render_template('index.html', train_rmse=train_rmse, train_r2=train_r2, train_mae=train_mae, test_rmse=test_rmse, test_r2=test_r2, test_mae=test_mae)

#testing react + flask communication
@app.route('/test_data')
def test_data(): 
    return {'test': ['test1', 'test2', 'test3']}

if __name__ == '__main__':
    app.run(debug=True)
