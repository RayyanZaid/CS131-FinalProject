import cv2

# To get angles between joints
import mediapipe as mp


import numpy as np

import cloud

import visualGlobals

# MediaPipe drawing utility
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

feedback_conditions = {
'leg_too_far': {
    'condition': lambda angle: angle > 140,
    'message': "Bring your feet closer to the chair. Feet are too far in front of you.",
    'lastFrame' : -10000
},
'leg_too_close': {
    'condition': lambda angle: angle < 60,
    'message': "Your feet are underneath the chair. Please bring them forward.",
    'lastFrame' : -10000,
},
'neck_too_down': {
    'condition': lambda angle: angle < 115,
    'message': "You are pointed too downwards. Lift your neck and point your instrument forward (parallel to the ground).",
    'lastFrame' : -10000,
},
'neck_too_up': {
    'condition': lambda angle: angle > 170,
    'message': "You are pointed too upwards. Bring your neck down.",
    'lastFrame' : -10000,
},
'back_too_hunched': {
    'condition': lambda angle: angle < 65,
    'message': "You are too hunched forward. Sit back and try to make your back straight.",
    'lastFrame' : -10000,
},
'back_too_leaned_back': {
    'condition': lambda angle: angle > 130,
    'message': "You are too leaned back. Sit up and try to make your back straight.",
    'lastFrame' : -10000,
},
}


# main function for posture grading video stream
    # 1) while loop that records user
    # 2) use mediapipe to get joints
    # 3) calculate angles to keep track of posture
    
def process_feedback(feedback_conditions, leg_position_angle, neck_posture_angle, sitting_posture_angle, frame, numFrame, fps):
    numFeedbackPointersPerFrame = 0
    feedbackString = ""
    feedbackImage = None

    # Iterate over each condition in the dictionary
    for key, details in feedback_conditions.items():
        # Check the condition and append feedback if necessary
        moreThan3Seconds = (numFrame - details['lastFrame']) / fps > 180

        if 'leg' in key and moreThan3Seconds:
            if details['condition'](leg_position_angle) and leg_position_angle != None:
                numFeedbackPointersPerFrame += 1
                feedbackString += f"{numFeedbackPointersPerFrame}. {details['message']} \n"
                feedbackImage = frame
                feedback_conditions[key]['lastFrame'] = numFrame

        elif 'neck' in key and moreThan3Seconds and neck_posture_angle != None:
            if details['condition'](neck_posture_angle):
                numFeedbackPointersPerFrame += 1
                feedbackString += f"{numFeedbackPointersPerFrame}. {details['message']} \n"
                feedbackImage = frame
                feedback_conditions[key]['lastFrame'] = numFrame

        elif 'back' in key and moreThan3Seconds and sitting_posture_angle != None:
            if details['condition'](sitting_posture_angle):
                numFeedbackPointersPerFrame += 1
                feedbackString += f"{numFeedbackPointersPerFrame}. {details['message']} \n"
                feedbackImage = frame
                feedback_conditions[key]['lastFrame'] = numFrame

    return feedbackString, feedbackImage


def postureGrading():
    print("Got into the postureGrading() function")

    cap = cv2.VideoCapture(0)


    print("Started VideoCapture")
    if not cap.isOpened():
        print("Error: Could not open video stream")
        return

    try:
        fps = cap.get(cv2.CAP_PROP_FPS)
        numFrames = 0
        sittingPostureGrade, neckPostureGrade, legPositionGrade = 0, 0, 0
        feedbackArray = []

        print("Going to use mp pose. Im pretty sure this is the error")
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            print("Inside MP POSE")
            while True:

                print("Inside While loop")
                success, frame = cap.read()
                if not success:
                    print("Error: Frame not available. Video has finished or is corrupt")
                    break
                
                if visualGlobals.testDoneFlag:
                    print("Test Done Flag is True now")
                    break

                cv2.imshow('Video Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("What the")
                    break

                # Process the image and detect the pose
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    # Extract posture angles
                    sitting_posture_angle, neck_posture_angle, leg_position_angle = get_pose_estimation(frame, pose)
                    # Calculate grades
                    sittingPostureGrade += gradePostureForEachFrame(sitting_posture_angle, sittingPostureDict)
                    neckPostureGrade += gradePostureForEachFrame(neck_posture_angle, neckPostureDict)
                    legPositionGrade += gradePostureForEachFrame(leg_position_angle, legPositionDict)

                    # Collect feedback

                    
                    if len(feedbackArray) < 6:
                        feedbackString , feedbackImage = process_feedback(feedback_conditions, leg_position_angle, neck_posture_angle, sitting_posture_angle, frame, numFrames, fps)

                        if len(feedbackString) > 0:
                            feedbackArray.append((feedbackString,feedbackImage))

    finally:
        cap.release()
        cv2.destroyAllWindows()
        calculate_final_grades_and_cleanup(sittingPostureGrade, neckPostureGrade, legPositionGrade, numFrames, feedbackArray)

def calculate_final_grades_and_cleanup(sittingPostureGrade, neckPostureGrade, legPositionGrade, numFrames, feedbackArray):
    # Normalize grades
    sittingPostureGrade /= max(numFrames, 1)
    neckPostureGrade /= max(numFrames, 1)
    legPositionGrade /= max(numFrames, 1)

    # Calculate final weighted grade
    finalGrade = 0.4 * sittingPostureGrade + 0.35 * neckPostureGrade + 0.25 * legPositionGrade
    print(f"Final Grades: Sitting: {sittingPostureGrade}, Neck: {neckPostureGrade}, Legs: {legPositionGrade}, Combined: {finalGrade}")

    # Send feedback and grade to cloud
    cloud.store_grade_with_files("user1", visualGlobals.testName, finalGrade, feedbackArray)

            


    print("Done with posture grading in postureMain.py")

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
    (85, 105): 100,
    (80, 84): 95,
    (75, 79): 90,
    (70, 74): 85,
    (65, 69): 80,
    (60, 64): 75,
    (55, 59): 70,
    (0, 54): 65,

    (106, 115): 95,
    (116, 125): 90,
    (126, 135): 85,
    (136, 145): 80,
    (146, 155): 75,
    (156, 165): 70,
    (166, 180): 65,
}

# Define the holding posture dictionary with detailed ranges
neckPostureDict = {
    (140, 160): 100,
    (125, 139): 95,
    (120, 124): 90,
    (115, 119): 85,
    (110, 114): 80,
    (95, 109): 75,
    (0, 94): 70,

    (161, 170): 95,
    (171, 180): 90,
    (181, 190): 85,
    (191, 200): 80,
}

legPositionDict = {
    (70, 100): 100,
    (65, 69): 95,
    (60, 64): 90,
    (55, 59): 85,
    (50, 54): 80,
    (45, 49): 75,
    (0, 44): 70,

    (101, 110): 95,
    (111, 120): 90,
    (121, 130): 85,
    (131, 140): 80,
    (141, 150): 75,
    (151, 160): 70,
    (161, 180): 65,
}



def gradePostureForEachFrame(angle, angleRangeToGrade):

    if angle == None:
        return 0
    for (low, high), grade in angleRangeToGrade.items():
        if low <= angle <= high:
            return grade
        
    return 0



def wrapUpTesting(sittingPostureGrade, neckPostureGrade, legPositionGrade, feedbackArray, testName):

    # Calculate Final Weighted Grade

    # Most important is Sitting, then Holding, then Leg
    
    finalGrade = 0.4 * sittingPostureGrade + 0.35 * neckPostureGrade + 0.25 * legPositionGrade

    # Send Feedback and Grade to Cloud Database
    cloud.store_grade_with_files("user1", testName, finalGrade, feedbackArray)

if __name__ == '__main__':
    postureGrading()
