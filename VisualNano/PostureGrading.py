import cv2

# To get angles between joints
import mediapipe as mp


import numpy as np

# MediaPipe drawing utility
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# main function for posture grading video stream
    # 1) while loop that records user
    # 2) use mediapipe to get joints
    # 3) calculate angles to keep track of posture

def postureGrading():

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        return


    # Variable to keep track of testing status. 
    # Will recieve signal from other Nano to switch testingFinished = True
    testingFinished = False

    # Variable to detect if user says "Stop"
    userInterruptedTesting = False

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():


            interruptionForDebugging = cv2.waitKey(1) and 0xFF == ord('q')

            if interruptionForDebugging:
                print("In Debug")

            if  userInterruptedTesting:
                print("Do not keep results of this rest")
                break

            if testingFinished:

                print("Need to calculate score here and send pictures of posture to database")


            success, frame = cap.read()
            if not success:
                print("Error: Frame not available. Video has finished or is corrupt")
                break

            # Convert the BGR image to RGB for mediapipe cuz it cv2 uses BGR
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the image and detect the pose
            results = pose.process(frame_rgb)

            # Draw the pose annotations on the frame.
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())



        # If no end cases run, then perform calculations
            # Display the frame. Might delete this later (just for debugging)
            cv2.imshow('Video Stream', frame)

            sitting_posture, holding_posture, shoulder_alignment, leg_position = get_pose_estimation(frame,pose)

            print(f"Sitting Posture : {sitting_posture}")
            print(f"Holding Posture : {holding_posture}")
            print(f"Shoulder Algin : {shoulder_alignment}")
            print(f"Leg Position : {leg_position}")
            

    cap.release()
    cv2.destroyAllWindows()

def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Middle point
    c = np.array(c)  # End point
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    if angle > 180.0:
        angle = 360-angle
    return angle

def get_pose_estimation(image, pose):
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.pose_landmarks:
        return None, None, None

    landmarks = results.pose_landmarks.landmark

    sitting_posture = calculate_angle(
        [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y]
    )

    # Calculate specific angles from the landmarks
    holding_posture = calculate_angle(
        [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]
    )

    shoulder_alignment = calculate_angle(
        [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
    )

    leg_position = calculate_angle(
        [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
    )

    

    return sitting_posture, holding_posture, shoulder_alignment, leg_position

if __name__ == '__main__':
    postureGrading()
