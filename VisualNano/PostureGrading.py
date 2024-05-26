# For video stream
import cv2

# To get angles between joints
import mediapipe as mp

print(mp.__version__)


# main function for posture grading video stream
    # 1) while loop that records user
    # 2) use mediapipe to get joints
    # 3) calculate angles to keep track of posture


def postureGrading() -> int:

    # Gets the camera
    cap = cv2.VideoCapture(0)


    if not cap.isOpened():
        print("Error: Could not open video stream")
        return
    
    # Variable to keep track of testing status. 
    # Will recieve signal from other Nano to switch testingFinished = True
    testingFinished = False

    # Variable to detect if user says "Stop"
    userInterruptedTesting = False

    while True:

        success, frame = cap.read()

        if not success:
            print("Error: Frame not available. Video has finished or is corrupt")
        
        # Display the frame. Might delete this later (just for debugging)

        cv2.imshow('Video Stream', frame)

        interruptionForDebugging = cv2.waitKey(1) and 0xFF == ord('q')

        if interruptionForDebugging:
            print("In Debug")

        if  userInterruptedTesting:
            print("Do not keep results of this rest")
            break

        if testingFinished:

            print("Need to calculate score here and send pictures of posture to database")


if __name__ == '__main__':
    postureGrading()