import cv2
import mediapipe as mp
import numpy as np

# MediaPipe drawing utility
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def postureGrading():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video stream")
        return

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
    out = cv2.VideoWriter('LegPositionTesting.mp4', fourcc, 20.0, (640, 480))  # Output file, codec, fps, resolution

    testingFinished = False
    userInterruptedTesting = False
    sittingPostureGrade = 0
    neckPostureGrade = 0
    legPositionGrade = 0
    numFrames = 0

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            numFrames += 1
            if numFrames == 201:
                testingFinished = True

            if cv2.waitKey(1) & 0xFF == ord('q') or userInterruptedTesting or testingFinished:
                if testingFinished:
                    # Compute averages
                    print(f"Sitting Posture Grade: {sittingPostureGrade / numFrames}")
                    print(f"Neck Posture Grade: {neckPostureGrade / numFrames}")

                    print(f"Leg Position Grade: {legPositionGrade / numFrames}")
                break

            success, frame = cap.read()
            if not success:
                print("Error: Frame not available")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)
            mp_drawing.draw_landmarks(
                frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            if results.pose_landmarks:
                angles = get_pose_estimation(frame, pose)
                if angles:
                    sitting_posture_angle, neck_posture_angle, leg_position_angle = angles
                    # Drawing angles on the frame
                    # cv2.putText(frame, f'Sitting Posture: {sitting_posture_angle:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
                    # cv2.putText(frame, f'Neck Posture: {neck_posture_angle:.2f}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

                    cv2.putText(frame, f'Leg Position: {leg_position_angle:.2f}', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            # Write the frame into the file 'output.mp4'
            out.write(frame)

            cv2.imshow('Video Stream', frame)

    cap.release()
    out.release()  # Close the video file
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
    neck_posture = calculate_angle(
        [landmarks[mp_pose.PoseLandmark.NOSE].x, landmarks[mp_pose.PoseLandmark.NOSE].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
    )


    leg_position = calculate_angle(
        [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_KNEE].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE].y],
        [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE].y]
    )

    

    return sitting_posture, neck_posture, leg_position


# ChatGPT generated

# ChatGPT Prompt:  create a 2-tuple : int dictionary where highest grade range set from 85 to 100, where the grade is 100%. 
# From this range, decrement grade by 5 points for each 5-degree decrease until we reach a grade of 60. 
# Angles outside of the ranges specified will be graded as 0.

sittingPostureDict = {

    (90, 100): 100,


    (85, 89): 90,
    (80, 84): 80,
    (75, 79): 70,
    (70, 74): 60,
    (65, 69): 50,
    (60, 64): 40,
    (0, 59): 0,


    (101, 105): 90,
    (106, 110): 80,
    (111, 115): 70,
    (116, 120): 60,
    (121, 125): 50,
    (126, 130): 40,
    (130, 180): 0,
    (146, 180): 0 
}

# Define the holding posture dictionary with detailed ranges
holdingPostureDict = {
    (75, 85): 100,

    (70, 74): 95,
    (65, 69): 90,
    (60, 64): 85,
    (55, 59): 80,
    (50, 54): 75,
    (45, 49): 70,
    (40, 44): 65,
    (35, 39): 60,
    (0, 34): 0,  

    (86, 90): 95,
    (91, 95): 90,
    (96, 100): 85,
    (101, 105): 80,
    (106, 110): 75,
    (111, 115): 70,
    (116, 120): 65,
    (121, 125): 60,
    (126, 180): 0
}



legPositionDict = {
    (90, 105): 100,
    (85, 89): 95,
    (80, 84): 90,
    (75, 79): 85,
    (70, 74): 80,
    (65, 69): 75,
    (60, 64): 70,
    (55, 59): 65,
    (50, 54): 60,
    (0, 44) : 0,
    # Extending ranges above 100
    (106, 110): 95,
    (111, 115): 90,
    (116, 120): 85,
    (121, 125): 80,
    (126, 130): 75,
    (131, 135): 70,
    (136, 140): 65,
    (141, 145) : 60,
    (146,180) : 0
}


def gradePostureForEachFrame(angle, angleRangeToGrade):

    for (low, high), grade in angleRangeToGrade.items():
        if low <= angle <= high:
            return grade
        
    return -1  



def wrapUpTesting(sittingPostureGrade, neckPostureGrade, legPositionGrade, imageToFeedbackDict, testName):

    # Calculate Final Weighted Grade

    # Most important is Sitting, then Holding, then Leg
    
    finalGrade = 0.4 * sittingPostureGrade + 0.35 * neckPostureGrade + 0.25 * legPositionGrade

    # Send Feedback and Grade to Cloud Database



    # Return the Grade

    return finalGrade

if __name__ == '__main__':
    postureGrading()
