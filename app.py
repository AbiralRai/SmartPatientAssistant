from flask import Flask, redirect, url_for, request, render_template
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model


def return_prediction(model, sample):
    """Return a prediction for heart classification

    Arguments:
        model {model.h5} -- Pre-trained model to predict the heart classification
        sample {array} -- Sample of the ECG reading of dimension (1,186,1)

    Returns:
        string -- Returns the predictions
    """
    classes = np.array(['Normal bea t', 'Supraventricular premature beat', 'Premature ventricular contraction',
                        'Fusion of ventricular and normal beat', 'Unclassifiable beat'])
    y_pred = model.predict(sample)
    predict = np.argmax(y_pred, axis=1)
    return classes[predict]


heart_model = load_model('heart_model.h5')
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return(render_template('index.html'))

    if request.method == 'POST':
        sample = request.form['sample']
        sampleURL = sample
        sample = np.loadtxt(sampleURL, delimiter=",")
        # Reshape sample for model
        sample = pd.DataFrame(sample)
        newSample = sample.iloc[:, :186].values
        testSample = newSample[np.newaxis, ...]

        print(testSample.shape)

        prediction = return_prediction(heart_model, testSample)[0]

        return render_template('index.html', result=prediction)


if __name__ == '__main__':
    app.run()
