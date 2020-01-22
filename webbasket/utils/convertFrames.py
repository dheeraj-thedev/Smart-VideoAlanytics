# Program To Read video
# and Extract Frames
import cv2
import os
# Function to extract frames
def FrameCapture(path, storagepath):
    # Path to video file
    vidObj = cv2.VideoCapture(path)
    # Used as counter variable
    count = 0
    # checks whether frames were extracted
    success = 1
    while success:
        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()
        # Saves the frames with frame-count
        cv2.imwrite(storagepath+"/frame%d.jpg"% count, image)
        count += 1
# Driver Code

if __name__ == '__main__':
    try:
        # Calling the function
        #FrameCapture("C:\\Users\\Admin\\PycharmProjects\\project_1\\openCV.mp4")
        videoPath= r"D:\Data-Videos\dELHI\AGRASEN ELEVATED ROAD\Delhi to noida"
        listofFiles= os.listdir(videoPath)
        folderCtr=0
        for video in listofFiles:
            pathtoVid=videoPath+'\\'+video
            pathtoImg="C:\\Output\\Dropbox\\"
            print("capturing")
            imgpath=pathtoImg+video
            os.mkdir(imgpath)
            FrameCapture(pathtoVid,imgpath)
            print("captured "+ pathtoVid)
    except Exception as e:
        print(e)
