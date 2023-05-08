import cv2
from collections import deque
import math

FONT_SCALE = 1e-3
THICKNESS_SCALE = 2e-3

def main():
    clicks = []

    # Callback function to record the location of clicks
    def click_event(event, x, y, flags, params):
        global handlingClick
        global img

        # Ignore additional clicks if a click is being processed
        if event == cv2.EVENT_LBUTTONDOWN and handlingClick == False:
            handlingClick = True
            local_img = img.copy()
            height, width, *_ = img.shape

            with ResetHandlingClickOnExit():
                # Draw the click
                put_circle(local_img, x, y)
                cv2.imshow('image', local_img)

                # Set up stores for:
                # Use label
                label = ""
                # Intermediate frames so user can delete text
                frames = deque()

                # Process user input
                while True:
                    key = cv2.waitKey(0)
                    if key == 13:  # Enter key
                        # User done with text
                        break

                    elif key == 27:  # Escape key
                        # Undo click -> reset image
                        cv2.imshow('image', img)
                        return

                    elif key >= 32 and key <= 126:  # Printable ASCII
                        # Save the frame
                        frames.append(local_img.copy())
                        # Update the label
                        label += chr(key)
                        put_text(local_img, label, x, y)
                        cv2.imshow('image', local_img)
                    
                    elif key == 127 and len(label) > 0:  # Delete key
                        # Remove last character
                        label = label[:-1]
                        # Return to last frame
                        local_img = frames.pop()
                        cv2.imshow('image', local_img)
                
                # Log and store the data
                clicks.append((label, x/width, y/height))
                print((label, x/width, y/height))
                img = local_img

    # Display the image
    cv2.imshow('image', img)

    cv2.setMouseCallback('image', click_event)

    # Wait for user input and break if q is pressed
    while True:
        key = cv2.waitKey(0)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

    # Write to file
    with open("output.csv", "w") as f:
        for click in clicks:
            f.write(f"{click[0]},{click[1]},{click[2]}\n")

def put_circle(img, x, y):
    height, width, *_ = img.shape
    
    cv2.circle(img,
               (x, y),
               radius=5,
               color=(0, 0, 255),
               thickness=-math.ceil(min(width, height) * THICKNESS_SCALE))

def put_text(img, text, x, y):
    height, width, *_ = img.shape

    cv2.putText(img,
                text,
                (x + 10, y),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=min(width, height) * FONT_SCALE,
                color=(0, 0, 255),
                thickness=math.ceil(min(width, height) * THICKNESS_SCALE))
    
class ResetHandlingClickOnExit:
    def __init__(self):
        pass
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, traceback):
        global handlingClick
        handlingClick = False

if __name__ == '__main__':
    # change image path here
    img = cv2.imread('image.jpg')
    handlingClick = False
    main()
