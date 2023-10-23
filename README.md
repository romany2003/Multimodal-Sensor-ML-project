# Multimodal-Sensor-ML-project

1 Objective
To design and implement a real-time multimodal learning system that com-
bines mobile sensor data, Principal Component Analysis (PCA), Dynamic
Time Warping (DTW), and anomaly detection techniques.
2 Assignments
2.1 Socket Programming with Data Buffering 
Download the sensor logger app for android or iPhone.
1. Implement a TCP socket server in Python that receives and displays
sensor data. The server should handle multiple client connections con-
currently. 
2. Implement data buffering. Store data in a buffer before batch process-
ing.
3. Parse the buffered JSON objects and store them into a time-stamped
CSV or txt file.
1
2.2 Principal Component Analysis (PCA) with Co-
variance Matrix 
1. Calculate the covariance matrix of the stored sensor data. 
2. Implement the PCA algorithm from scratch1, performing eigenvalue
decomposition on the covariance matrix.
3. Visualize the principal components and project the data onto a lower-
dimensional space. Compare the variance explained by each compo-
nent.
2.3 Dynamic Time Warping (DTW) with Early Aban-
doning
1. Implement the DTW algorithm from scratch2, incorporating early aban-
doning to improve computational efficiency. 
2. Perform DTW on two different sets of time-series data from the mobile
sensor to identify similar patterns.
2.4 Anomaly Detection
1. Use the PCA transformed data to train a simple anomaly detection
model (e.g., One-Class SVM)
