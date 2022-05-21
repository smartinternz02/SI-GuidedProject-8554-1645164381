import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
#importing the inputScript file used to analyze the URL
import inputScript 
import json
import requests


#load model
app = Flask(__name__)
# model = pickle.load(open('Phishing_Website.pkl', 'rb'))

# @app.route('/')
# def helloworld():
#     return render_template("index.html")


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "Vhsx7vmc7em10KcOYiAVGpWhgtyR0-l5vzCXo8pT8EhI"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}

#response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/8dd91582-83ea-48ee-b477-a85f1fbdf010/predictions?version=2022-03-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
#print("Scoring response")
#print(response_scoring.json())
#Redirects to the page to give the user iput URL.
@app.route('/')
def predict():
    return render_template('final.html')

#Fetches the URL given by the URL and passes to inputScript
@app.route('/y_predict',methods=['POST'])
def y_predict():
    url = request.form['URL']
    checkprediction = inputScript.main(url)
    #t = [[checkprediction]]
    payload_scoring = {"input_data": [{"fields":checkprediction , "values": checkprediction}]}

    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/8dd91582-83ea-48ee-b477-a85f1fbdf010/predictions?version=2022-03-06', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    #print("Scoring response")
    #print(response_scoring.json())
    #prediction = model.predict(checkprediction)
    
    #print(response_scoring)
    output=response_scoring.json()['predictions'][0]['values'][0][0]
    if(output==1):
        pred="Your are safe!!  This is a Legitimate Website."
        
    else:
        pred="You are on the wrong site. Be cautious!"
    return render_template('final.html', prediction_text='{}'.format(pred),url=url)
#Takes the input parameters fetched from the URL by inputScript and returns the predictions
# @app.route('/predict_api',methods=['POST'])
# def predict_api():
#     '''
#     For direct API calls trought request
#     '''
#     data = request.get_json(force=True)
#     prediction = model.y_predict([np.array(list(data.values()))])

#     output = prediction[0]
#     return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True)

