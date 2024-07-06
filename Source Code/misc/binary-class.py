import numpy as np
import librosa
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Step 1: Feature Extraction with Padding
def extract_features(audio_file, max_length):
    y, sr = librosa.load(audio_file, sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    zero_crossing_rate = np.mean(librosa.feature.zero_crossing_rate(y=y))
    
    if mfccs.shape[1] < max_length:
        pad_width = max_length - mfccs.shape[1]
        mfccs = np.pad(mfccs, ((0, 0), (0, pad_width)), mode='constant')
    else:
        mfccs = mfccs[:, :max_length]
        
    return np.concatenate((mfccs.flatten(), [spectral_centroid, spectral_bandwidth, zero_crossing_rate]))

wheeze_folder = "wheeze"
wheeze_files = [os.path.join(wheeze_folder, file) for file in os.listdir(wheeze_folder) if file.endswith(".wav")]

crackle_folder = "nonwheeze" 
crackle_files = [os.path.join(crackle_folder, file) for file in os.listdir(crackle_folder) if file.endswith(".wav")]

max_length = 7855 

wheeze_features = np.array([extract_features(file, max_length) for file in wheeze_files])
crackle_features = np.array([extract_features(file, max_length) for file in crackle_files])

wheeze_labels = np.zeros(wheeze_features.shape[0])
crackle_labels = np.ones(crackle_features.shape[0])

X = np.vstack((wheeze_features, crackle_features))
y = np.hstack((wheeze_labels, crackle_labels))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

classifier = SVC(kernel='linear')
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy*100:.2f}%")
new_features = extract_features('check.wav', max_length)

prediction = classifier.predict([new_features])

if prediction == 0:
    print("The audio contains wheeze.")
else:
    print("The audio does not contain wheeze.")
