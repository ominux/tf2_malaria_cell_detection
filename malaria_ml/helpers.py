import cv2
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

class Helpers(object):

    @staticmethod
    def imresize(im, shape):
        """Resizes an image by using a bi-cubic interpolation if the shape
        parameter is passed, returns the image as is otherwise.

        Parameters
        ----------
        im : np.array
            (X, Y, 3)-shaped representation of an image.
        shape : False|tuple
            Width and height values.

        Returns
        -------
        np.ndarray"""
        if shape:
            return cv2.resize(im, dsize=shape, interpolation=cv2.INTER_CUBIC)
        return im

    @staticmethod
    def reads_imdir(path, ext, slices=(None, 1000), resize=False, skip_paths=False):
        """Reads the images from a given directory and returns a
        list of numpy arrays representing each image:
        [
            array([....]),
            array([....]),
            ...
        ]

        Parameters
        ----------
        path : str
            Full or relative path to the directory containing the images.
        ext : str
            The extension of the images, jpg, png, etc...
        slices : tuple
            Fetch a selection of the images, say the first 1000, pass (None, 1000).
        resize : tuple|False
            Pass a tuple if you want to resize the images
        skip_paths : bool
            Return the paths to the images or not."""
        imlist = glob(f"{path}/*.{ext}")
        if not skip_paths:
            return [Helpers.read_im(i, resize) for i in imlist[slices[0]:slices[1]]]
        return [Helpers.read_im(i, resize) for i in imlist[slices[0]:slices[1]]], np.array(imlist)

    @staticmethod
    def read_im(path, resize):
        return Helpers.imresize(cv2.imread(path), resize)

    @staticmethod
    def show_images(images, rows=1, figsize=(1, 1), titles=[]):
        """That's just lazy writing.

        Parameters
        ---------
        images : list|np.ndarray
            list or array of images to plot

        rows : int
            Self explanatory.
        figsize : tuple
            matplotlib figsize

        Returns
        -------
        None
        """
        fig = plt.figure(figsize=figsize)
        for n, image in enumerate(images):
            fig.add_subplot(rows, np.ceil(images.shape[0] / float(rows)), n + 1)
            if image.ndim == 2:
                plt.gray()
            try:
                plt.title(titles[n])
            except IndexError:
                pass
            plt.imshow(image)
        fig.set_size_inches(np.array(fig.get_size_inches()) * images.shape[0])
        plt.show()

