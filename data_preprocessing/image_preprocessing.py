# -*- coding: utf-8 -*-
"""image_preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pWeky8qUYu0V3rWsUZCzjP6UqqcE9wLM
"""

import cv2
import numpy as np
def image_preprocessing(image):
  gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
  thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
  # Remove horizontal lines
  horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
  remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)
  cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    cv2.drawContours(thresh, [c], -1, (0,255,255), 5)
  # Remove vertical lines
  vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
  remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
  cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  cnts = cnts[0] if len(cnts) == 2 else cnts[1]
  for c in cnts:
    cv2.drawContours(thresh, [c], -1, (0,255,255), 15)
  contours,hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
  bounding_boxes = []
  for cnt in contours:
    if cv2.contourArea(cnt)>50:
      [x,y,w,h] = cv2.boundingRect(cnt)
      if (x, y) != (0, 0) and (y+h-y)/image.shape[0] > 0.18 and (x+w-x)/image.shape[1] > 0.01 and (x+w-x)/(y+h-y) > 0.15:
        bounding_boxes.append([x,y,x+w,y+h])
  new_thresh = np.where(thresh == 255, 0, 255)
  if np.array(bounding_boxes).size != 0:
    xxmin = min(np.array(bounding_boxes)[:, 0])
    yymin = min(np.array(bounding_boxes)[:, 1])
    xxmax = max(np.array(bounding_boxes)[:, 2])
    yymax = max(np.array(bounding_boxes)[:, 3])
    xxmin = xxmin - 25 if xxmin - 25 > 0 else 0
    xxmax = xxmax + 40 if xxmax + 40 < image.shape[1] else xxmax
    yymin = yymin - 5 if yymin - 5 > 0 else yymin
    yymax = yymax + 5 if yymax + 5 < image.shape[0] else yymax
    return new_thresh[yymin:yymax, xxmin:xxmax]
  else:
    return new_thresh