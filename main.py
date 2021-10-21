### Ex-1.
### Submitted by Tzlil Ovadia, ID: 311317689


import matplotlib.pyplot as plt
import numpy as np
import skimage.color



YIQ_MATRIX = np.array([[0.299, 0.587, 0.114],[0.596, -0.275, -0.321],[0.212, -0.523, 0.311]])
RGB_MATRIX = np.array([[1, 0.956, 0,621],[1, -0.272, -0.647],[1, -1.106, 1.703]])
GRAY_SCALE = 1
RGB = 2


x = np.hstack([np.repeat(np.arange(0,50,2),10)[None, :], np.array([255]*6)[None, :]])
grad = np.tile(x, (256,1))

# 3.2 - Read Image
def read_image(filename, representation):
    """
    filename - the filename of an image on disk (could be grayscale or RGB).
    representation - representation code, either 1 or 2 defining whether the output should be a:
    grayscale image (1)
    or an RGB image (2).
    NOTE: If the input image is grayscale, we won’t call it with represen- tation = 2.
    :param filename: String - the address of the image we want to read
    :param representation: Int - as described above
    :return: an image in the correct representation
    """
    if representation != RGB and representation != GRAY_SCALE:
        return "Invalid Input. You may use representation <- {1, 2}"
    tempImage  = plt.imread(filename)[:,:,:3]
    resultImage = tempImage
    if representation == GRAY_SCALE:
        resultImage = skimage.color.rgb2gray(tempImage)
    elif representation == RGB:
        resultImage = tempImage

    return resultImage


def TEST_imdisplay(imageToShow):
    """
    For self-testing purpose.
    :param imageToShow: an image Object recieved from read_image() func.
    """
    plt.figure()
    plt.imshow(imageToShow, cmap = "gray")
    plt.show()

# 3.3 - Display Image
def imdisplay(filename, representation):
    """
    filename and representation are the same as those defined in read_image’s interface.
    :param filename:
    :param representation:
    """
    if representation != GRAY_SCALE and representation != RGB:
        return "Invalid Input. You may use representation <- {1, 2}"
    imageToShow = read_image(filename, representation)
    plt.figure()
    plt.imshow(imageToShow, cmap = "gray")
    plt.show()


# 3.4.1 - Transforming an RGB image to YIQ color space
def rgb2yiq(imRGB):
    """
    Transforming an RGB image to YIQ color space
    :param imRGB:  An RGB image
    :return:
    """
    return skimage.color.rgb2yiq(imRGB)
    # result = np.dot(YIQ_MATRIX, imRGB.T)
    # return result


# 3.4.2 - Transforming an YIQ image to RGB color space
def yiq2rgb(imYIQ):
    """
    Transforming an YIQ image to RGB color space
    :param imYIQ:
    :return:
    """
    # result = np.dot(RGB_MATRIX, imYIQ.T)
    # return result
    return skimage.color.yiq2rgb(imYIQ)

def getNumOfPixel(image):
    """
    Helper function to get number of pixels in image (assuming that image is valid)
    :param image: an image file read with read_image() function
    :return: Integer, ∑(pixels)
    """
    return len(image)*len(image[0])

def checkIfNormalizedValid(histogram):
    """

    :param histogram:
    :return:
    """
    return histogram.max() == 255 and histogram.min() == 0



def checkImageFormat(image):
    """

    :param image: an Image
    :return:
    """
    if len(image.shape) == 2:
        return GRAY_SCALE
    elif len(image.shape) == 3:
        return RGB
    else:
        return 0

def getHistogram(image):
    hist,bins = np.histogram(image.flatten(), 256, [0, 1])
    return hist


# 3.5 - Histogram equalization

def histogram_equalize(im_orig):
    """
    Given an image, this function will perform an histogram equalization.
    NOTE: If an RGB image is given, the following equalization procedure should only operate on the Y channel of
    :param im_orig: is the input grayscale or RGB float64 image with values in [0, 1].
    :return: a list [im_eq, hist_orig, hist_eq] where:
            - im_eq - is the equalized image. grayscale or RGB float64 image with values in [0, 1]
            - hist_orig - is a 256 bin histogram of the original image (array with shape (256,) ).
            - hist_eq - is a 256 bin histogram of the equalized image (array with shape (256,) ).
    """

    """ 
    Important Things To Complete:
    1. Ask if it is possible to make use of skimage.color.rgb2yiq and yiq2rgb
    2. Figure out how to perform a linear stretch
    3. Add some end-cases where the algorithm could fail e.g where we have only 2-color image.
    4. Remove unnecessary junk from code
    5. Make sure that the values returned are by the requested format
    """

    # Step No. 0 - Check if the given image is an RGB/GrayScale Format:
    swappedToYIQ = False # Used to help us know if yiq2rgb is needed
    format = checkImageFormat(im_orig)
    if format == RGB:
        im_orig = rgb2yiq(im_orig)[:,:,0]
        swappedToYIQ = True

    # im_orig =  grad/255
    # Step No. 1 - Compute the image histogram:

    hist_orig,bins = np.histogram(im_orig.flatten(), 256, [0, 1])
    # Step No. 2 - Compute the cumulative histogram:
    hist_cdf = np.array(hist_orig.cumsum(), dtype=np.float64)
    # Step No. 3 - Normalize the cumulative histogram:
    N = getNumOfPixel(im_orig)
    hist_cdf /= N
    # Step No 4. - Multiply the normalized histogram by the maximal gray level value (Z-1):
    hist_cdf *= 255
    # Step No 5. - Verify that the minimal value is 0 and that the maximal is Z-1, otherwise
    # stretch the result linearly in the range [0,Z-1]:
    # print(f"max GC: {hist_cdf.max()} \n min GC: {hist_cdf.min()}")
    if not checkIfNormalizedValid(hist_cdf):
        #Linear Stretch here
        pass
    im_orige = np.array(im_orig.flatten())
    im_orige = np.floor(im_orige*255)
    # LUT:
    lookUpTable = np.floor((hist_cdf - hist_cdf.min())/(hist_cdf[255]-hist_cdf.min())*255)
    flat_im_eq = lookUpTable[np.array(im_orige, dtype=int)]
    #
    im_eq = np.reshape(np.asarray(flat_im_eq), im_orig.shape)
    # if swappedToYIQ:
    #     im_orig = yiq2rgb(im_orig)
    # print(T_k)
    TEST_imdisplay(im_eq)
    hist_eq, bins_eq = np.histogram(flat_im_eq, 256, [0, 256])
    # plt.plot(hist_eq)
    # plt.show()

    return hist_orig, im_eq, hist_eq

def initQuants(hist_seg):
    quants = []
    z_curr = 0
    idx_curr = 0
    for i in hist_seg:
        if i == 0:
            continue
        quants.append( int(z_curr+(i-z_curr)/2))
        idx_curr += 1
        z_curr = i
    return quants

def updateSegmentIndex(q1, q2):
    return (q1+q2)/2

def updateQuantIndex(seg_i, histogram):
    """

    :param seg_i: Is an range which represents a segment of 256 array.
    :param histogram:
    :return:
    """
    seg_i_arr = np.array(seg_i) ##

    hist_seg_i = histogram[seg_i_arr] ##

    enumrtator = sum(list(map(lambda z, h_z: z * h_z, seg_i, hist_seg_i)))

    denomenator = sum(hist_seg_i)

    return enumrtator/denomenator


# 3.6 Optimal image quantization
def quantize (im_orig, n_quant, n_iter):
    """
    :param im_orig: is the input grayscale or RGB image to be quantized (float64 image with values in [0, 1])
    :param n_quant: is the number of intensities your output im_quant image should have.
    :param n_iter: is the maximum number of iterations of the optimization procedure (may converge earlier.)
    :return: [im_quant, error] where:
             im_quant: is the quantized output image. (float64 image with values in [0, 1]).
             error: is an array with shape (n_iter,) (or less) of the total intensities error for each iteration of the
    """
    seg_size = int(256/n_quant)
    hist = getHistogram(im_orig)
    seg_help = range(0,256,seg_size)

    hist_seg_indices = list(map(lambda x: x - 1, np.array(seg_help)))
    ## get the initial q values that agrees with the current ((z_i) + 1, z_i+1] segment:

    quants = initQuants(hist_seg_indices)
    hist_seg = []

    ## get the initial uniform distributed segments of z_i from the algorithm we learned
    for seg in range(n_quant):
        hist_seg.append(hist[seg : (seg+1)*seg_size])

    for iteration in range(n_iter):
        # Computing q - the values to which each of the segments’ intensities will map.
        #               q is also a one dimensional array, containing n_quant elements:
        seg_idx = iteration % len(hist_seg_indices)
        quants_idx = quants_idx = iteration%len(quants)

        quants[quants_idx] = updateQuantIndex(range(hist_seg_indices[iteration],
                                                               hist_seg_indices[iteration+1]),hist)

        # Computing z - the borders which divide the histograms into segments.
        #               z is an array with shape (n_quant+1,). The first and last elements are 0 and 255 respectively:

        hist_seg_indices[seg_idx] = updateSegmentIndex(quants[quants_idx], quants[quants_idx])


        pass



if __name__ == '__main__':
    seg_size = int(256/8)
    seg_help = range(0,257,seg_size)

    hist_seg = list(map(lambda x: x-1 ,np.array(seg_help)))
    hist_seg[0]=0
    print(hist_seg)


    # test_im = read_image("/Users/tzlilovadia/Desktop/testt.png",1)
    # print(test_im.shape)
    # TEST_imdisplay(test_im)
    # # print(test_im.shape)
    # histogram_equalize(read_image("/Users/tzlilovadia/Desktop/testt.png", 2))
    # quantize()
    # TEST_imdisplay(grad)