import numpy as np
import librosa
import joblib
import pickle
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import sounddevice as sd
import wave


def record_audio(file_path, duration=5, sample_rate=44100, channels=1):
    print("Recording...")
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()
    print("Recording complete.")

    print("Saving to", file_path)
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

if __name__ == "__main__":
    file_path = "output.wav"
    record_audio(file_path)
#replace with your path to the label
labelencoder_src='label_encoder.joblib'
#replace with your audio file path
filename='output.wav'
model_path = '/Users/giablum/Downloads/src/Sound Identifier ML/sound_model.h5'

# Load the trained model
model_path = '/Users/giablum/Downloads/src/Sound Identifier ML/sound_model.h5'
model = load_model(model_path)

loaded_label_encoder = joblib.load(labelencoder_src)
def features_extractor(file):
    audio, sample_rate = librosa.load(file, res_type='kaiser_fast') 
    mfccs_features = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40)
    mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
    return mfccs_scaled_features

# Example usage for prediction

mfccs_scaled_features = features_extractor(filename)
mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

# Make predictions
raw_predictions = model.predict(mfccs_scaled_features)
predicted_label = np.argmax(raw_predictions)

# Ensure labelencoder is a LabelEncoder object
if isinstance(loaded_label_encoder, LabelEncoder):
    predicted_class =loaded_label_encoder.classes_[predicted_label]
    my_dict={0:'air conditioner', 1: 'Car Horn', 2: 'Children Playing', 3:'Dog Barking', 4:'drill', 7:'jackhammer',8:'siren', 5:'engine idling', 6:'gun shot',9:'street music' }
    
    print("Predicted Class Label:", my_dict[predicted_class])
else:
    print("Error: labelencoder is not a LabelEncoder object.")