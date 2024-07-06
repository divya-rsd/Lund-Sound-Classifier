import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

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
crackle_folder = "nonwheeze"
both_folder = "both"
normal_folder = "none"

wheeze_files = [os.path.join(wheeze_folder, file) for file in os.listdir(wheeze_folder) if file.endswith(".wav")]
crackle_files = [os.path.join(crackle_folder, file) for file in os.listdir(crackle_folder) if file.endswith(".wav")]
both_files = [os.path.join(both_folder, file) for file in os.listdir(both_folder) if file.endswith(".wav")]
normal_files = [os.path.join(normal_folder, file) for file in os.listdir(normal_folder) if file.endswith(".wav")]

max_length = 7855 

wheeze_features = np.array([extract_features(file,max_length) for file in wheeze_files])
crackle_features = np.array([extract_features(file,max_length) for file in crackle_files])
both_features = np.array([extract_features(file,max_length) for file in both_files])
normal_features = np.array([extract_features(file,max_length) for file in normal_files])


wheeze_labels = np.zeros(wheeze_features.shape[0])
crackle_labels = np.ones(crackle_features.shape[0])
both_labels = np.full(both_features.shape[0], 2)
normal_labels = np.full(normal_features.shape[0], 3)

X = np.vstack((wheeze_features, crackle_features, both_features, normal_features))
y = np.hstack((wheeze_labels, crackle_labels, both_labels, normal_labels))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

classifier = SVC(kernel='linear')
classifier.fit(X_train, y_train)

# Step 7: Evaluate the Model
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy*100:.2f}%")

def predict(audio_file):
    audio_file = "static/" + audio_file[:-4] + "_without_hb.wav"
    new_features = extract_features(audio_file,max_length)  # Replace with your new audio file
    prediction = classifier.predict([new_features])

    if prediction == 0:
        class_ = "wheeze"
    elif prediction == 1:
        class_ = "crackle"
    elif prediction == 2:
        class_ = "wheeze and crackle"
    else:
        class_ = "none"
    print(f"The audio contains {class_}.")

    return class_

# predict("recording_9_without_hb.wav")