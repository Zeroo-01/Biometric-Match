import cv2
import fingerprint_feature_extractor

if __name__ == '__main__':
    # Read the first input image
    img1_path = 'enhanced/1.jpg'
    img1 = cv2.imread(img1_path, 0)  # Adjust the path as needed

    # Read the second input image
    img2_path = 'enhanced/1.jpg'  # Adjust the path as needed
    img2 = cv2.imread(img2_path, 0)

    # Extract minutiae features from both images
    FeaturesTerm1, FeaturesBif1, FeaturesTerm2, FeaturesBif2, similarity_score = fingerprint_feature_extractor.extract_minutiae_features(
        img1, img2, spuriousMinutiaeThresh=10, invertImage=False)

    # Print the similarity score
    print("Similarity Score:", similarity_score)
