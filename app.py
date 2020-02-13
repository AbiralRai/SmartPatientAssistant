import os
from flask import Flask, redirect, url_for, request, render_template
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename


heart_model = load_model('heart_model.h5')
UPLOAD_FOLDER = './CSV'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Type of file allowed to be uploaded
    
    Arguments:
        filename {[str]} -- Name of the file 
    
    Returns:
        [str] -- full file path
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def return_prediction(model, sample):
    """Return a prediction for heart classification

    Arguments:
        model {model.h5} -- Pre-trained model to predict the heart classification
        sample {array} -- Sample of the ECG reading of dimension (1,186,1)

    Returns:
        string -- Returns the predictions
    """
    SAMPLE_NUMBER = 186
    
    if (SAMPLE_NUMBER != sample.size  ):
        return ["Invaild Sample Size"]
    else:
        classes = np.array(['Normal beat', 'Supraventricular premature beat', 'Premature ventricular contraction',
                            'Fusion of ventricular and normal beat', 'Unclassifiable beat'])
        y_pred = model.predict(sample)
        predict = np.argmax(y_pred, axis=1)
        return classes[predict]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return(render_template('index.html'))

    file = request.files['file']
    if request.method == 'POST':
        # Check file and save to CSV folder
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            sample = np.loadtxt('./CSV/' + filename, delimiter=",")

            # Reshape sample for model
            sample = pd.DataFrame(sample)
            newSample = sample.iloc[:, :186].values
            testSample = newSample[np.newaxis, ...]
            prediction = return_prediction(heart_model, testSample)[0]

            return render_template('index.html', result=prediction)
            
        return render_template('index.html')



if __name__ == '__main__':
    app.run()
