import os
import glob
import argparse
import matplotlib

# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
import skimage.measure as sk

from DenseDepth.layers import BilinearUpSampling2D
from DenseDepth.utils import predict, load_images, display_images
from matplotlib import pyplot as plt

import numpy as np


# Output depth map size - 260 * 320

class DepthExtractor:
    def __init__(self, modelPath):
        # Custom object needed for inference and training
        custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}
        
        print('Loading model...')
        self.model = self.loadModel(modelPath, custom_objects)

        print("Depth extractor initiated")

    def loadModel(self, modelPath, custom_objects):
        print('\nModel loaded ({0}).'.format(modelPath))
        return load_model(modelPath, custom_objects=custom_objects, compile=False)

    def getDepthMap(self, image, inputs=None):
        if inputs is None:
            im = np.clip(np.asarray(image, dtype=float), 0, 1)
            inputs = np.stack([im], axis=0) 
        
        outputs = predict(self.model, inputs)
        return outputs[0][:,:,0]

    def maxPool(self, img):
        # for i in range(1):
        #     img = sk.block_reduce(img, (9, 8), np.max)

        return img

    def showImg(self, outputs, imgName='test.png'):
        viz = display_images(outputs.copy())
        # self.toCsv(outputs)
        plt.figure(figsize=(10,5))
        plt.imshow(viz)
        plt.savefig('../TestImgs/'+imgName)
        plt.show()

    def saveCsv(self, outputs, fileName='test'):
        # outputs = outputs[0][:,:,0]
        np.savetxt('../TestImgs/'+fileName+'.csv', outputs, delimiter=',')
        np.save('../TestImgs/'+fileName+'.npy', outputs)

import time
d = DepthExtractor('DenseDepth/nyu.h5')
imgs = ['00001.png', '00002.png','00003.png', '00004.png','00005.png', '00006.png', '00007.png', '00008.png', '00009.png', '00010.png']

# for i in range(7, 11):
for i in range(1, 2):
    inputs = load_images( glob.glob('DenseDepth/examples/'+imgs[i-1]) )
    t0 = time.time()
    res = d.getDepthMap(None, inputs)
    print("Time used: ",time.time()-t0)
    d.showImg(d.maxPool(res), 'test'+str(i)+'.png')
    d.saveCsv(d.maxPool(((res * 1666.7) - 66.7)/100), 'test'+str(i))

    # print(np.shape(res))
    # print(np.shape(d.maxPool(res)))
    # input("Enter to continue")


