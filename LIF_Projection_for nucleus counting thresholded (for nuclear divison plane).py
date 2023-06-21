import read_lif as lif
import numpy as np
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os
import skimage.filters as skfilter
import skimage.io as skio
import skimage.color as skcolor
import scipy
import matplotlib.pyplot as plt
from collections import Counter

def my_thresholding(input_matrix):
    test_file = input_matrix
    number_of_pixels = input_matrix.shape[0]*input_matrix.shape[-1]
    threshold = 0.005
    additional_discard = 0

    OneD_image = sorted(list(np.ravel(test_file)))
    counter = Counter(OneD_image)

    intensities_to_nullify = []
    greatest_peaks = {0:0}
    for i in sorted(list(counter.keys())):
        if round(counter[i]/number_of_pixels, 5) < threshold:
            intensities_to_nullify.append(i)
        if list(greatest_peaks.values())[0] < counter[i]:
            greatest_peaks = {i:counter[i]}
    test_file[test_file <= int(list(greatest_peaks.keys())[0])] = 0

    for i in intensities_to_nullify:
        test_file[test_file == i] = 0
    try:
        discard_less_than = sorted(list(set(list(np.ravel(test_file)))))[additional_discard]
        test_file[test_file <= discard_less_than] = 0
    except:
        pass
    return test_file

#사용자를 위한 GUI를 통한 파일 불러오기
Tk().withdraw()
filename = askopenfilename()

#파일 불러오기
reader = lif.Reader(filename)
series = reader.getSeries()

#파일 경로 지정하기

filepath = "projection_results"

try:
    os.chdir('./' + filepath)
except:
    os.makedirs(filepath)
    os.chdir('./' + filepath)

header = 0

image = 0

for i in range(len(series)):
    try:
        chosen = series[i]

        position_name = chosen.getName()
        if position_name[-3:] == "001":
            header += 1

        for j in range(len(chosen.getChannels())):
            if j != 0:
                continue
            image = chosen.getFrame(T=0, channel=j)
            #print(image)
            thresh_cal = my_thresholding(np.max(image, axis=0))
            shape = list(thresh_cal.shape)
            shape.append(3)
            img = np.zeros(tuple(shape), dtype=np.uint8)
            img[:,:,1] = thresh_cal
            #img[:,:, 1:] = 0

            # mean 값으로 projection 했을 때가 궁금해서 만들어 봄
            # img = Image.fromarray(np.nanmean(image, axis=0, dtype=np.uint8), 'L')

            output_name = position_name + "_ChannelNo" + str(j+1)
            format = "png"

            skio.imsave(fname=output_name + '.' + format, arr=img)
            #print(output_name + '.' + format)
    except:
        pass

#os.chdir("../")