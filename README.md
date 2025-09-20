# PennAir-Software-Challenge

Develop an algorithm to detect solid shapes on a grassy background, trace their outlines, locate their centers.

## Tasks Completed

1. Shape Detection on Static Image ✅
   - Approach was to use both a colored and texture approach to distinguish between the grass and the solid shapes.
     - The colored approach involved comparing all the shapes against green background and distinguishing shapes. However, this excluded the green colored solid shapes.
     - Thus, we added the texture approach to ensure we also include green colored solid shapes.
   - Once we could distinguish between the grass and the shapes, we could draw the outline around the shapes and determine their centerpoints.

## Dependencies

- Code was written in Python 3.13.5 with the libraries `numpy` and `cv2` installed. You can use the following to install these packages:
  - `pip3 install numpy`
  - `pip3 install opencv-python`
- To run code
  1. Clone the repository onto your local computer
  2. Enter `python3 shape_etection.py` in the terminal
  3. The file "Detected_Static_Shape.png" will contained the detected shapes.
