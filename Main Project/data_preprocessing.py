#python file that handles the preprocessing of sound data to extract,
#from the sensor and normalize the data for our machine learning model.
#Remember: Raspberry Pi limited memory, limited compute power.


import os
import numpy as np
import pandas as pd
import librosa as lb

def read_audio_file(file_path):
    """
    This function reads the audio file from the given file path.
    """
    # Read the audio file
    data, sample_rate = lb.load(file_path, sr=None)
    return data, sample_rate

def normalize_data(data):
    """
    This function normalizes the audio data.
    """
    # Normalize data
    normalized_data = (data - np.min(data)) / (np.max(data) - np.min(data))
    return normalized_data

def extract_features(data, sample_rate):
    """
    This function extracts features from the audio data.
    """
    # Extract features from the audio data
    # This is just a placeholder. You'll need to replace this with your actual feature extraction code.
    mfccs = lb.feature.mfcc(y=data, sr=sample_rate)
    return mfccs

def preprocess_audio_file(file_path):
    """
    This function preprocesses the audio file.
    """
    # Read the audio file
    data, sample_rate = read_audio_file(file_path)

    # Normalize the audio data
    normalized_data = normalize_data(data)

    # Extract features from the audio data
    features = extract_features(normalized_data, sample_rate)

    return features



