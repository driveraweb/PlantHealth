import numpy as np

NDVI_VID = 0
VIS_VID = 1
NO_VID = -1
FRAMERATE = 40
MAX_FEATURES = 500
GOOD_MATCH_PERCENT = .12
H = np.asarray([[ 9.20594188e-01,  -1.42957852e-01,  2.54077905e+01],
                [-1.95122194e-02,   8.20436221e-01,  4.61027479e+01],
                [-1.97094364e-05,  -3.27387298e-04,  1.00000000e+00]])
H_SHORT = np.asarray([[ 9.96989355e-01, -3.23739855e-02, -2.29815889e+01],
                      [-5.52607506e-03,  9.61416255e-01,  2.97800662e+01],
                      [ 3.13973868e-05, -1.09498814e-04,  1.00000000e+00]])
#H_LONG
#H = np.asarray([[ 8.86888432e-01,  4.39226569e-02,  2.45432770e+01],
#       [-2.51932559e-02,  9.22965234e-01,  1.07536386e+02],
#       [-3.72214918e-05,  3.27009413e-05,  1.00000000e+00]])
#H_long = np.asarray([[  9.80667346e-01,   1.26994766e-02,   1.78365943e+01],
#       [ -4.96549469e-02,   1.01925158e+00,   2.79901091e+01],
#       [ -1.06449700e-04,   3.45053055e-06,   1.00000000e+00]])
CMAP = np.asarray([[255, 255, 255],
       [250, 250, 250],
       [246, 246, 246],
       [242, 242, 242],
       [238, 238, 238],
       [233, 233, 233],
       [229, 229, 229],
       [225, 225, 225],
       [221, 221, 221],
       [216, 216, 216],
       [212, 212, 212],
       [208, 208, 208],
       [204, 204, 204],
       [200, 200, 200],
       [195, 195, 195],
       [191, 191, 191],
       [187, 187, 187],
       [183, 183, 183],
       [178, 178, 178],
       [174, 174, 174],
       [170, 170, 170],
       [166, 166, 166],
       [161, 161, 161],
       [157, 157, 157],
       [153, 153, 153],
       [149, 149, 149],
       [145, 145, 145],
       [140, 140, 140],
       [136, 136, 136],
       [132, 132, 132],
       [128, 128, 128],
       [123, 123, 123],
       [119, 119, 119],
       [115, 115, 115],
       [111, 111, 111],
       [106, 106, 106],
       [102, 102, 102],
       [ 98,  98,  98],
       [ 94,  94,  94],
       [ 90,  90,  90],
       [ 85,  85,  85],
       [ 81,  81,  81],
       [ 77,  77,  77],
       [ 73,  73,  73],
       [ 68,  68,  68],
       [ 64,  64,  64],
       [ 60,  60,  60],
       [ 56,  56,  56],
       [ 52,  52,  52],
       [ 56,  56,  56],
       [ 60,  60,  60],
       [ 64,  64,  64],
       [ 68,  68,  68],
       [ 73,  73,  73],
       [ 77,  77,  77],
       [ 81,  81,  81],
       [ 85,  85,  85],
       [ 90,  90,  90],
       [ 94,  94,  94],
       [ 98,  98,  98],
       [102, 102, 102],
       [106, 106, 106],
       [111, 111, 111],
       [115, 115, 115],
       [119, 119, 119],
       [123, 123, 123],
       [128, 128, 128],
       [132, 132, 132],
       [136, 136, 136],
       [140, 140, 140],
       [145, 145, 145],
       [149, 149, 149],
       [153, 153, 153],
       [157, 157, 157],
       [161, 161, 161],
       [166, 166, 166],
       [170, 170, 170],
       [174, 174, 174],
       [178, 178, 178],
       [183, 183, 183],
       [187, 187, 187],
       [191, 191, 191],
       [195, 195, 195],
       [200, 200, 200],
       [204, 204, 204],
       [208, 208, 208],
       [212, 212, 212],
       [216, 216, 216],
       [221, 221, 221],
       [225, 225, 225],
       [229, 229, 229],
       [233, 233, 233],
       [238, 238, 238],
       [242, 242, 242],
       [246, 246, 246],
       [250, 250, 250],
       [255, 255, 255],
       [250, 250, 250],
       [245, 245, 245],
       [240, 240, 240],
       [235, 235, 235],
       [230, 230, 230],
       [225, 225, 225],
       [220, 220, 220],
       [215, 215, 215],
       [210, 210, 210],
       [205, 205, 205],
       [200, 200, 200],
       [195, 195, 195],
       [190, 190, 190],
       [185, 185, 185],
       [180, 180, 180],
       [175, 175, 175],
       [170, 170, 170],
       [165, 165, 165],
       [160, 160, 160],
       [155, 155, 155],
       [151, 151, 151],
       [146, 146, 146],
       [141, 141, 141],
       [136, 136, 136],
       [131, 131, 131],
       [126, 126, 126],
       [121, 121, 121],
       [116, 116, 116],
       [111, 111, 111],
       [106, 106, 106],
       [101, 101, 101],
       [ 96,  96,  96],
       [ 91,  91,  91],
       [ 86,  86,  86],
       [ 81,  81,  81],
       [ 76,  76,  76],
       [ 71,  71,  71],
       [ 66,  66,  66],
       [ 61,  61,  61],
       [ 56,  56,  56],
       [ 66,  66,  80],
       [ 77,  77, 105],
       [ 87,  87, 130],
       [ 98,  98, 155],
       [108, 108, 180],
       [119, 119, 205],
       [129, 129, 230],
       [140, 140, 255],
       [131, 147, 239],
       [122, 154, 223],
       [113, 161, 207],
       [105, 168, 191],
       [ 96, 175, 175],
       [ 87, 183, 159],
       [ 78, 190, 143],
       [ 70, 197, 127],
       [ 61, 204, 111],
       [ 52, 211,  95],
       [ 43, 219,  79],
       [ 35, 226,  63],
       [ 26, 233,  47],
       [ 17, 240,  31],
       [  8, 247,  15],
       [  0, 255,   0],
       [  7, 255,   0],
       [ 15, 255,   0],
       [ 23, 255,   0],
       [ 31, 255,   0],
       [ 39, 255,   0],
       [ 47, 255,   0],
       [ 55, 255,   0],
       [ 63, 255,   0],
       [ 71, 255,   0],
       [ 79, 255,   0],
       [ 87, 255,   0],
       [ 95, 255,   0],
       [103, 255,   0],
       [111, 255,   0],
       [119, 255,   0],
       [127, 255,   0],
       [135, 255,   0],
       [143, 255,   0],
       [151, 255,   0],
       [159, 255,   0],
       [167, 255,   0],
       [175, 255,   0],
       [183, 255,   0],
       [191, 255,   0],
       [199, 255,   0],
       [207, 255,   0],
       [215, 255,   0],
       [223, 255,   0],
       [231, 255,   0],
       [239, 255,   0],
       [247, 255,   0],
       [255, 255,   0],
       [255, 249,   0],
       [255, 244,   0],
       [255, 239,   0],
       [255, 233,   0],
       [255, 228,   0],
       [255, 223,   0],
       [255, 217,   0],
       [255, 212,   0],
       [255, 207,   0],
       [255, 201,   0],
       [255, 196,   0],
       [255, 191,   0],
       [255, 185,   0],
       [255, 180,   0],
       [255, 175,   0],
       [255, 170,   0],
       [255, 164,   0],
       [255, 159,   0],
       [255, 154,   0],
       [255, 148,   0],
       [255, 143,   0],
       [255, 138,   0],
       [255, 132,   0],
       [255, 127,   0],
       [255, 122,   0],
       [255, 116,   0],
       [255, 111,   0],
       [255, 106,   0],
       [255, 100,   0],
       [255,  95,   0],
       [255,  90,   0],
       [255,  85,   0],
       [255,  79,   0],
       [255,  74,   0],
       [255,  69,   0],
       [255,  63,   0],
       [255,  58,   0],
       [255,  53,   0],
       [255,  47,   0],
       [255,  42,   0],
       [255,  37,   0],
       [255,  31,   0],
       [255,  26,   0],
       [255,  21,   0],
       [255,  15,   0],
       [255,  10,   0],
       [255,   5,   0],
       [255,   0,   0],
       [255,   0,  15],
       [255,   0,  31],
       [255,   0,  47],
       [255,   0,  63],
       [255,   0,  79],
       [255,   0,  95],
       [255,   0, 111],
       [255,   0, 127],
       [255,   0, 143],
       [255,   0, 159],
       [255,   0, 175],
       [255,   0, 191],
       [255,   0, 207],
       [255,   0, 223],
       [255,   0, 239]], dtype='uint8')
