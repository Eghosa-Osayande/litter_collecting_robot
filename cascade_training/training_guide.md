# Haars Cascade Training Guide


## STEP 1

Manually create folders for /positive and /negative in your project. Now with our game and our script both running, with the OpenCV output window focused we can press 'f' to capture a screenshot and save it to the positive folder, or 'd' to save a screenshot to the negative folder.

Remember you want to collect lots of examples of each. I captured 100 positive and 100 negative, but you will likely want to do even more than that. And remember to get a variety of samples from all different conditions you want your model to recognize objects in. When you're done, review your captures to check for any mistakes and confirm you got a good variety. Again, the more samples you get, the better your final results will be. But we can always come back, collect more screenshots later, and retrain our model.

Now we need to prepare the negative samples to be used for training. To do this, we simply need to create a text file that lists where all our negative samples can be found. 

```c:/YandeCode/project/.env/Scripts/python.exe c:/YandeCode/project/train_cascade/gen_neg_des_file.py```

## STEP 2

Next we need to generate a similar file for the positive images, but this one is a little more complicated. It needs to contain not only the image paths, but also the bounding box coordinates for each object we want to detect in each image. Rather than annotate these manually, or write a script ourselves, let's use OpenCV annotation program which is designed specifically for creating this file.

Unfortunately this simple opencv_annotation.exe command line program isn't included with pip installed OpenCV, and it isn't included in any installation of version 4.2.0. Instead we must install OpenCV version 3.4 to get access to this and other Cascade Classifier programs we will need.

I recommend downloading the newest version of OpenCV 3.4 from the pre-built Windows binaries. For me that was version 3.4.11. This file is a self-extacting ZIP, and you can save the contents anywhere that's convenient for you. Once extracting, you should find the executables we need in ```[your save location]/opencv/build/x64/vc15/bin/```. The programs we'll be using should all be in that folder: opencv_annotation.exe, opencv_createsamples.exe, and opencv_traincascade.exe.

Even though we'll be preparing our samples and training our model with these programs from OpenCV 3.4, the resulting classifier will still be usable in our newer version of OpenCV.

Now we can run the annotation program.

This program will open each image in your positive folder one at a time in an OpenCV window. In each image you should draw a box around the objects within it that you want to be able to detect. You click once to set the upper left corner, then again to set the lower right corner. You'll see a red box enclosing your object. Press 'c' to confirm this selection. If you don't like the box you've drawn, you can click again elsewhere to draw a different box. You can also press 'd' to undo the previous confirmation. When done with an image, click 'n' to move to the next one. You can press 'esc' to exit early, or it will exit automatically when you've annotated all of the images.

```C:\YandeCode\project\downloaded_softwares\opencv\build\x64\vc15\bin\opencv_annotation.exe --annotations=pos.txt --images=positive/```

## STEP 3

When you're done, review the pos.txt output file. You will likely need to change the direction of the slashes or else opencv_createsamples.exe will complain that it can't find your files in the next step.

Next we need to create a vector file from all of our positive annotations.

There are a few arguments here to pay attention to. Value for -num should be greater than or equal to the number of rectangles you drew, so that all of them get turned into vectors. If you drew 100 rectangles and set this to 1000, it will still output only 100 vectors, so you can just make this any large number. The -w and -h is the detection window size you want to use. You won't be able to detect objects smaller than this size, and the larger you make this the longer it will take to train your model. 20 or 24 are common.

If you get an error like:
```OpenCV: terminate handler is called! The last OpenCV error is: OpenCV(3.4.11) Error: Assertion failed (0 <= roi.x && 0 <= roi.width && roi.x + roi.width <= m.cols && 0 <= roi.y && 0 <= roi.height && roi.y + roi.height <= m.rows) in cv::Mat::Mat, file C:\build\3_4_winpack-build-win64-vc15\opencv\modules\core\src\matrix.cpp, line 466```

This usually means opencv_createsamples.exe can't find the image files. Check the paths in the pos.txt file. Don't use spaces in the filepath, and fix the slashes. I had trouble using absolute paths here on Windows, so I recommend making the paths relative to your project folder, cd-ing into your project directory in your terminal, and running the .exe from there using the full absolute path on the .exe itself (like my commands demonstrate above).

When the create samples program completes successfully, it will tell you how many samples it created, which should be the same as how many rectangles you drew around objects in the annotation step.

```C:\\YandeCode\\project\\downloaded_softwares\\opencv\\build\\x64\\vc15\\bin\\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec```

## STEP 4

Finally, we're ready to train our cascade classifier model!

Create a /cascade folder to hold the outputs from the training. Then you can run opencv_traincascade.exe.

```C:\\YandeCode\\project\\downloaded_softwares\\opencv\\build\\x64\\vc15\\bin\\opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -numPos 150 -numNeg 100 -numStages 10 -w 24 -h 24```

```C:\YandeCode\project\downloaded_softwares\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 150 -numNeg 90 -numStages 12 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.999```

There are many arguments here to talk about.

The -numPos needs to be some amount lower than the number of samples created by createsamples.
If you get errors that look like: Can not get new positive sample. Then you need to either lower your -numPos or lower the -minHitRate (default 0.995).
A popular suggestion for -numNeg is to use half of -numPos. This is a good place to start, but you'll want to try many different values here. Using twice the number of negative to positive, or even more, can sometimes yield better results.
The -w and -h must match what was used for the createsamples step.
The more -numStages the longer it will take to train. Too many and you might overtrain.
If you run initially with 10 stages, you can later run it again with more stages, like 30, and it will pick up from where it left off. As you get deeper into the stages, each one takes longer.
When you run the training, you'll get some useful insights in the terminal output. In the results table, HR means hit rate (the number of positive examples that were correctly identified), FA is false alarm (the number of negative samples that were incorrectly identified), and N = weak layer number (which Haar cascade layer the rates are for). A really small Neg acceptanceRatio can sometimes be an indication of overtraining, ie. if it has e-06. We'll talk more about overtraining in a little bit.

Now's a good time to explain what goes on when training a machine learning model.

The trainer will show your model a random image: either one of the objects you drew a box around, or a random cutout from one of your negative images.
The model will try to predict whether this image is from the positive or negative pile.
The trainer will tell your model whether that prediction was right or wrong.
The model will make adjustments to itself based on whether it was right or wrong.
Then the cycle repeats, thousands of times.
This process is sort of like learning with flashcards when you were a kid. Over time, with more an more training, the model begins to identify patterns that help it make more accurate predictions.

When opencv_traincascade.exe finishes, you'll find your trained model in cascade/cascade.xml. We can now use this model to find objects in new screenshots. Let's re-use the Vision class to draw the object detection rectangles on our output.

## Quick Commands

```c:/YandeCode/project/.env/Scripts/python.exe c:/YandeCode/project/train_cascade/gen_neg_des_file.py```

```C:\YandeCode\project\downloaded_softwares\opencv\build\x64\vc15\bin\opencv_annotation.exe --annotations=pos.txt --images=positive/```

```C:\\YandeCode\\project\\downloaded_softwares\\opencv\\build\\x64\\vc15\\bin\\opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec```

```C:\\YandeCode\\project\\downloaded_softwares\\opencv\\build\\x64\\vc15\\bin\\opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -numPos 150 -numNeg 100 -numStages 10 -w 24 -h 24```

```C:\YandeCode\project\downloaded_softwares\opencv\build\x64\vc15\bin\opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 150 -numNeg 200 -numStages 12 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.999```