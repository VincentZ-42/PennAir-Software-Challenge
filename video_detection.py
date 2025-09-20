import cv2
import numpy as np

def process_frame(frame):
    """
    Process a single frame to detect solid shapes on grassy background
    """
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks for colors

    # Green (grass + green shapes)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Non-green (all other shapes)
    mask_non_green = cv2.bitwise_not(mask_green)

    # Low-texture check for green shapes
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Compute local variance (sliding window)
    kernel_size = 9
    mean = cv2.blur(gray.astype(np.float32), (kernel_size, kernel_size))
    sq_mean = cv2.blur((gray.astype(np.float32)**2), (kernel_size, kernel_size))
    local_variance = sq_mean - mean**2

    # Adjust these to match the texture of the grass in the background
    variance_thresh = 100
    low_texture_mask = (local_variance < variance_thresh).astype(np.uint8) * 255

    # Combine green mask with low-texture mask
    mask_green_shapes = cv2.bitwise_and(mask_green, low_texture_mask)

    # Combine masks (non-green + green shapes)
    combined_mask = cv2.bitwise_or(mask_non_green, mask_green_shapes)

    # Clean masks
    kernel = np.ones((5,5), np.uint8)
    mask_clean = cv2.morphologyEx(combined_mask, cv2.MORPH_OPEN, kernel)
    mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_CLOSE, kernel)

    # Find contours and draw
    contours, _ = cv2.findContours(mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = frame.copy()
    
    shape_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            shape_count += 1
            # Draw contour with red outline
            cv2.drawContours(output, [cnt], -1, (0,0,255), 2)
            
            # Compute center of shape
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # Draw center as a small red dot
                cv2.circle(output, (cX, cY), 4, (0, 0, 255), -1)
                # Put coordinate text
                cv2.putText(output, f"({cX},{cY})", (cX-30, cY-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
    
    # Add shape count to frame
    cv2.putText(output, f"Shapes detected: {shape_count}", (10, 30), 
               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    return output

def main():
    # Initialize video capture
    # Change to 0 for webcam, or file path for video
    cap = cv2.VideoCapture("Dynamic.mp4")  
    if not cap.isOpened():
        print("Error: Could not open video source!")
        return
    
    print("Press 'q' to quit, 's' to save current frame")
    
    while True:
        # Read frame from video
        ret, frame = cap.read()
        if not ret:
            print("End of video or failed to read frame")
            break
        
        # Process the frame
        processed_frame = process_frame(frame)
        
        # Display the processed frame
        cv2.imshow('Shape Detection - Live', processed_frame)
        
        # Check for key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # Quit
            break
        elif key == ord('s'):  # Save current frame
            cv2.imwrite('saved_frame.png', processed_frame)
            print("Frame saved as 'saved_frame.png'")
        elif key == ord('p'):  # Pause/play
            cv2.waitKey(0)  # Wait until any key is pressed
    
    # Clean up
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()