

import os
import cv2 as cv

folder: str = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder)


def resize(srcFolder: str, resizeDir: str, count: int, extension: str = '.png'):

    if not os.path.exists(resizeDir):
        os.mkdir(resizeDir)

    folder_contents = os.listdir(srcFolder)
    for file in folder_contents:
        print(f'{count} of {len(folder_contents)}')
        # Checking if the file is present in the list

        oldName = os.path.join(folder, srcFolder, file)
        img = cv.imread(oldName)

        shape = img.shape
        maxSize=650
        if shape[0] > maxSize:
            scale_percent = int((maxSize*100)/shape[0])  # percent of original size
            width = int(img.shape[1] * scale_percent / 100)
            height = int(img.shape[0] * scale_percent / 100)
            dim = (width, height)
            img = cv.resize(img, dim, interpolation=cv.INTER_AREA)

        file_name = f'{count}' + extension

        newName = os.path.join(resizeDir, file_name)
        cv.imwrite(newName, img)

        count = count+1


resize(srcFolder=os.path.join('raw_images','fearless_web'), resizeDir='positivew', count=104)