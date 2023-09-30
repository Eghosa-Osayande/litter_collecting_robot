

import os

folder: str = os.path.dirname(os.path.abspath(__file__))
os.chdir(folder)


def rename_images_in_folder(folderName: str, count: int, extension: str = '.png'):
    for file in os.listdir(folderName):
        # Checking if the file is present in the list

        oldName = os.path.join(folder, folderName, file)
        n = os.path.splitext(file)[0]

        b = f'{count}' + extension
        newName = os.path.join(folder, folderName, b)

        # Rename the file
        os.rename(oldName, newName)
        count = count+1


res = os.listdir(folder)
print(res)

rename_images_in_folder(folderName='positive', count=99999)
rename_images_in_folder(folderName='negative', count=99999)
rename_images_in_folder(folderName='positive', count=1)
rename_images_in_folder(folderName='negative', count=1)
# rename_images_in_folder(folderName='pepsi_positve', count=777)
