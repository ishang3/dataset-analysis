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
    range_values = [x for x in range(0,600,interval)][1:]

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

    plt.savefig('output/frequency.png')



def crop_and_save(x,y,width,height,image,file_name):
    if not os.path.exists('output/cropped_anns_rgb'):
        os.mkdir('output/cropped_anns_rgb')
    if not os.path.exists('output/cropped_anns_gray'):
        os.mkdir('output/cropped_anns_gray')

    try:
        rgb_image = image[y:y+height,x:x+width]
        img_gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('output/cropped_anns_rgb/'+ str(number_of_annotations) + '-'
                    + file_name.split('/')[-1], rgb_image)
        cv2.imwrite('output/cropped_anns_gray/' + str(number_of_annotations) + '-'
                    + file_name.split('/')[-1], img_gray)
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
                    if crop:
                        img_path = path + filename.split('.')[0] + '.' + 'jpg'
                        image = cv2.imread(img_path)
                        crop_and_save(int(xmin),int(ymin),int(width),
                                  int(height),image,img_path)


                    line = fp.readline()


    #this sorts all the annotations by box area
    sorted_d = sorted(total.items(), key=operator.itemgetter(1))

    #creates a dictionary of the width or height of each ann
    create_histogram(dimensions)

    average_per_image =  number_of_annotations / len(total.items())

    with open('output/output.txt', 'a') as the_file:
        the_file.write(f'Average Number of Annotations per image {average_per_image}')
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

    if not os.path.exists('output'):
        os.mkdir('output')

    parser = argparse.ArgumentParser()

    parser.add_argument('-data', '--dataset', help="Enter location of dataset; must be in kitti format")
    parser.add_argument('-crop', '--crop', help="To crop images annotations or not",default=True)
    parser.add_argument('-range', '--range', help="Interval for building histogram", default=50)

    args = parser.parse_args()

    global crop,interval
    crop = args.crop
    interval = args.range

    args = parser.parse_args()
    driver(args.dataset)