from shapely.geometry import Polygon
import os
import operator
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import cv2
import argparse



def create_histogram(dimensions):
    histogram = {}
    range_values = [x for x in range(0,600,50)][1:]

    dict = []
    temp = []
    for value in range_values:
        for file in dimensions:
            if file not in temp:
                width, height = dimensions[file]
                if width < value or height < value:
                    temp.append(file)
                    if str(value) not in histogram:
                        histogram[str(value)] = 1
                    else:
                        histogram[str(value)] += 1

    objects = list(histogram.keys())
    y_pos = np.arange(len(objects))
    performance = list(histogram.values())

    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel('Usage')
    plt.title('IMAGE annotation frequency by pixel size')

    plt.show()


def crop_and_save(x,y,width,height,image,file_name):
    if not os.path.exists('cropped_anns'):
        os.mkdir('cropped_anns')

    try:
        new_image = image[y:y+height,x:x+width]
        cv2.imwrite('cropped_anns/'+ str(number_of_annotations) + '-'
                    + file_name.split('/')[-1], new_image)
    except:
        print('DOES NOT WORK',file_name)


def driver(path):
    total = {}

    dimensions = {}
    global number_of_annotations
    number_of_annotations = 0
    for filename in os.listdir(f'{path}/'):
        file_end = filename.split('.')[-1]
        if file_end == 'txt':
            with open(f'{path}/'+filename) as fp:
                line = fp.readline()
                while line:
                    number_of_annotations += 1
                    splitted = line.split(' ')
                    xmin = float(splitted[4])
                    ymin = float(splitted[5])
                    xmax = float(splitted[6])
                    ymax = float(splitted[7])

                    box = [[xmin,ymax],[xmax,ymax],[xmax,ymin],[xmin,ymin]]
                    width = xmax - xmin
                    height = ymax - ymin
                    dimensions[filename] = (width,height)
                    box = Polygon(box)
                    total[filename] = box.area

                    # this will take the image and the ann coordinates
                    # and then save the cropped annotation in a separate folder
                    # img_path = path + filename.split('.')[0] + '.' + 'jpg'
                    # image = cv2.imread(img_path)
                    # crop_and_save(int(xmin),int(ymin),int(width),
                    #               int(height),image,img_path)


                    line = fp.readline()


    #this sorts all the annotations by box area
    sorted_d = sorted(total.items(), key=operator.itemgetter(1))

    #creates a dictionary of the width or height of each ann
    create_histogram(dimensions)

    average_per_image =  number_of_annotations / len(total.items())


    print("average number of annotations",average_per_image)

if __name__ == '__main__':

    ## TODO

    ## width,height,area,average brightness,name of the file(primary key)



    #This script will return
    # 1) Histogram of the different range of pixel sizes
    # 2) Avg. Number of Annotations Per Image
    # 3) Crops each annotation in a new folder
    # 4) Interval Range for Histogram

    #Command Line Arguments
    #location to kitti file format



    driver('deep-test-2/test-data/box-train/')