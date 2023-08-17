import json
from flask import Flask, jsonify
import numpy as np
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/recommendations/<int:product_index>', methods=['GET'])
def get_recommendations(product_index, num_recommendations=5):

    similarity_matrix = np.genfromtxt('similarity_matrix.csv', delimiter=',') 
    URL = "https://script.google.com/macros/s/AKfycbw08tF8pg8Qi4-uwyqeZKefbTb2OWAKhVydTCBSLgqhJ5y59gpTBvcIX-LwKpX7RfTRRg/exec"
    r = requests.get(url = URL).json()
       
    similar_products = np.argsort(similarity_matrix[product_index])[::-1]
    
    recommended_indices=[]
    for i in similar_products:
        if(i==product_index):
            continue
        
        if (r[i]['carbon_footprint (kg)'] < r[product_index]['carbon_footprint (kg)'] and r[i]['price (in Rs)'] <= r[product_index]['price (in Rs)']+10000):
            recommended_indices.append(int(i))
        if(len(recommended_indices)==num_recommendations):
            break
    return jsonify({'recommendations': recommended_indices})

if __name__ == '__main__':
    app.run()
