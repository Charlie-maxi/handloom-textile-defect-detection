import cv2
import numpy as np

from skimage.feature import (
    graycomatrix,
    graycoprops
)

def extract_features(image):

    # If a file path is given
    if isinstance(image, str):
        img = cv2.imread(image)
    else:
        # Gradio provides an RGB NumPy array
        img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if img is None:
        raise ValueError(
            "Unable to read image. Please upload a valid fabric image."
        )

    b, g, r = cv2.split(img)

    r_mean = np.mean(r)
    g_mean = np.mean(g)
    b_mean = np.mean(b)

    r_std = np.std(r)
    g_std = np.std(g)
    b_std = np.std(b)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    hist = cv2.calcHist(
        [gray],
        [0],
        None,
        [4],
        [0,256]
    ).flatten()

    hist = hist / hist.sum()

    glcm = graycomatrix(
        gray,
        distances=[1],
        angles=[0],
        levels=256,
        symmetric=True,
        normed=True
    )

    contrast = graycoprops(glcm, 'contrast')[0,0]
    homogeneity = graycoprops(glcm, 'homogeneity')[0,0]
    energy = graycoprops(glcm, 'energy')[0,0]
    correlation = graycoprops(glcm, 'correlation')[0,0]

    edges = cv2.Canny(
        gray,
        100,
        200
    )

    edge_density = np.sum(edges > 0) / edges.size

    weave_regularity = 1 / (1 + np.std(gray))

    thresh = cv2.threshold(
        gray,
        127,
        255,
        cv2.THRESH_BINARY
    )[1]

    defect_area = (
        np.sum(thresh == 0)
        /
        thresh.size
    ) * 100

    return [[
        r_mean,
        g_mean,
        b_mean,

        r_std,
        g_std,
        b_std,

        hist[0],
        hist[1],
        hist[2],
        hist[3],

        contrast,
        homogeneity,
        energy,
        correlation,

        edge_density,

        weave_regularity,

        defect_area
    ]]