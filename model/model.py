import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix
import fingerprint_feature_extractor


def calculate_similarity_score(image1_path, image2_path):
    # Extract minutiae features from both images
    FeaturesTerm1, FeaturesBif1, FeaturesTerm2, FeaturesBif2, similarity_score = fingerprint_feature_extractor.extract_minutiae_features(
        image1_path, image2_path, spuriousMinutiaeThresh=10, invertImage=False)
    return similarity_score  # Return the similarity score


def collect_data(directory):
    """
    Collect similarity scores and labels for images in the given directory.
    """
    data = {'similarity_scores': [], 'labels': []}

    for subdir, dirs, files in os.walk(directory):
        # Determine label based on subdirectory name
        label = subdir.split('/')[-1] == 'match'
        for file in files:
            img1_path = os.path.join(subdir, file)
            for other_file in files:
                if other_file != file:
                    img2_path = os.path.join(subdir, other_file)
                    similarity_score = calculate_similarity_score(
                        img1_path, img2_path)
                    data['similarity_scores'].append(similarity_score)
                    data['labels'].append(label)

    return data


def main():
    train_match_dir = 'path/to/trainMatch'
    train_reject_dir = 'path/to/trainReject'

    match_data = collect_data(train_match_dir)
    reject_data = collect_data(train_reject_dir)

    # Combine data from both categories
    combined_data = {
        'similarity_scores': match_data['similarity_scores'] + reject_data['similarity_scores'],
        'labels': match_data['labels'] + reject_data['labels']
    }

    # Convert lists to NumPy arrays for easier manipulation
    similarity_scores = np.array(
        combined_data['similarity_scores']).reshape(-1, 1)
    labels = np.array(combined_data['labels'])

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        similarity_scores, labels, test_size=0.2, random_state=42)

    # Normalize the similarity scores
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train the SVM model
    svm_model = SVC(kernel='linear')  # Using linear kernel for simplicity
    svm_model.fit(X_train_scaled, y_train)

    # Predict on the test set
    y_pred = svm_model.predict(X_test_scaled)

    # Evaluate the model
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))


if __name__ == "__main__":
    main()
