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
![Alt text](image/shape_save.png)
<br>
<br>
<br>
<br>
<br>
<br>

# Apply in **Energy Harvesting**

<br>

## 1. Energy Harvesting

The depletion of fossil fuels and the increase in energy consumption have become a global environmental problem. Accordingly, many studies are being conducted with interest in converting natural energy such as solar energy, thermal energy, wind energy, etc. into electrical energy based on a lot of interest in alternative energy development. The availability of low-cost renewable and scalable energy harvesting systems may enable electronic equipment to operate autonomously in the long run, with the aim of developing devices that utilize energy from the environment to eliminate the drawbacks of conventional small batteries and enhance performance.

<br>

## 2. Wind Energy Harvesting

While various methods are being introduced to acquire energy from nature, we approached them by harvesting electrical energy based on vibration energy. Vibration-based energy harvesting has the advantage of being compact by harvesting electrical energy with mechanical movements from external influences. It can also be applied at low wind speeds and has the advantage of being able to build a wireless network.

<br>

## 3. Measure Amplitude

Previously, the vibration system of the energy harvester was analyzed by measuring the amplitude with a laser sensor, but it is insufficient when it is accompanied by a deformation process of the bluff body. Therefore, we recognized the appearance of the harvester with a camera, found the center of gravity, and coordinated it to enable visual analysis of the harvester.

