from django.forms.models import model_to_dict
from .models import Input, Output
from imutils.object_detection import non_max_suppression
import re
import cv2
import pytesseract
import numpy as np
from PIL import Image

ptrn = re.compile(".*(?P<pan>[A-Z0]{3}[ABCFGHJLPT][A-Z0]{1}[Oo0-9]{4}[A-Z0]{1})")
layer_names = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"
]


def extract_pan(img_path, ptrn):
    img = cv2.imread(img_path)
    if img is None:
        return -1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    strng = [ptrn.match(i.strip()) for i in pytesseract.image_to_string(gray).split("\n") if i.strip()]
    pan_no = [i.groupdict()['pan'] for i in strng if i]
    if pan_no:
        return pan_no[0]
    h, w = img.shape[:2]
    new_w = 640
    new_h = round(h * new_w / (w * 32)) * 32
    img = cv2.resize(img, (new_w, new_h))
    net = cv2.dnn.readNet("model/frozen_east_text_detection.pb")
    means = tuple(cv2.cvtColor(img, cv2.COLOR_BGR2RGB).mean(axis=(0, 1)))
    blob = cv2.dnn.blobFromImage(img, 1.0, (new_w, new_h), means, swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layer_names)
    ax0, ax1, ax2, ax3 = np.where(scores >= 0.05)
    selected_geometry = geometry[ax0, :, ax2, ax3]
    offset_x = ax3 * 4
    offset_y = ax2 * 4
    cos = np.cos(selected_geometry[:, 4])
    sin = np.sin(selected_geometry[:, 4])
    h, w = selected_geometry[:, [0, 2]].sum(axis=1), selected_geometry[:, [1, 3]].sum(axis=1)
    endX = (offset_x + (cos * selected_geometry[:, 1]) + (sin * selected_geometry[:, 2])).astype(int)
    endY = (offset_y - (sin * selected_geometry[:, 1]) + (cos * selected_geometry[:, 2])).astype(int)
    startX = (endX - w).astype(int)
    startY = (endY - h).astype(int)
    rects = list(zip(startX, startY, endX, endY))
    confidences = scores[ax0, ax1, ax2, ax3]
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    img1 = img.copy()
    for (startX, startY, endX, endY) in boxes:
        cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
    tmp = []
    for startx, starty, endx, endy in boxes:
        pad_x = int((endx - startx) * .1)
        pad_y = int((endy - starty) * .1)
        startx = max(0, startx - pad_x)
        starty = max(0, starty - pad_y)
        endx = min(img.shape[1], endx + pad_x)
        endy = min(img.shape[0], endy + pad_y)
        if abs(startx - endx) > abs(starty - endy):
            text = pytesseract.image_to_string(img1[starty:endy, startx:endx])
            #             display(text)
            if ptrn.match(text.strip()):
                return ptrn.match(text.strip()).groupdict()['pan']
            tmp.append(img1[starty:endy, startx:endx])
        else:
            text1 = pytesseract.image_to_string(np.rot90(img1[starty:endy, startx:endx]))
            if ptrn.match(text1.strip()):
                return ptrn.match(text1.strip()).groupdict()['pan']
            text2 = pytesseract.image_to_string(np.rot90(img1[starty:endy, startx:endx], -1))
            if ptrn.match(text2.strip()):
                return ptrn.match(text2.strip()).groupdict()['pan']
            tmp.append(np.rot90(img1[starty:endy, startx:endx]))
    for img2 in tmp:
        gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray)
        #         display(text)
        if ptrn.match(text.strip()):
            return ptrn.match(text.strip()).groupdict()['pan']
        th = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 19, 5)
        text = pytesseract.image_to_string(th)
        if ptrn.match(text.strip()):
            return ptrn.match(text.strip()).groupdict()['pan']
    return Image.fromarray(img)


def process_pan(inp):
    pan = extract_pan(inp.image.path, ptrn)
    if not isinstance(pan, str):
        out = Output(input = inp, number=None, status=0, error="Invalid Image")
    else:
        out = Output(input = inp, number=pan, status=1, error=None)
    return out