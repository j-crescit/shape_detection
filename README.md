# Shape Detection

<br>

## Introduction
1. Find the outline of the object and detect shape.

2. Detects corner points and areas of the object shape.

3. Analyze the position of the center of gravity of an object.

<br>

## code

The code does the following in sequence:

Reading the image and converting from RGB to GrayScale

Removing Gaussian Noise vis Gaussian Blur

Appling Inverse Binary Thresholding Finding Invrese Binary Adaptive Thresholding

Finding all Countours in the processed image

Filtering countours bases on their area

Initializing a new image and drawing the filtered contours

<br>

## Dependencies
* python

* opencv

<br>

## Sample output:

<img src = "image/shape_save.png" width="300%" height="300%"/>

<br>
<br>
<br>
<br>
<br>
<br>

# Apply in **Energy Harvesting**

<br>

## 1. Wind Flow Energy Harvesting

* Vibration energy generated wind flow is
* Various aerodynamically phenomena occur depending on the cross-sectional shape of the bluff body, which has a great influence on energy harvesting efficiency.

<br>

## 2. Measure Amplitude

* The vibration system of the bluff body is analyzed to understand the aerodynamic phenomenon.

* Representatively, there is a method of measuring and analyzing the amplitude of a vibrating blur body with a laser sensor.

* However, other movements of the bluff body (slice, self-strain, etc.) cannot be analyzed.

* It is possible to visually analyze the appearance of the harvester while grasping the vibration system through the camera.