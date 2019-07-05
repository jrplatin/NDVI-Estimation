import math
import rasterio
import matplotlib.pyplot as plt
import numpy
from PIL import Image
import numpy 
from matplotlib import colors

def ndvi_estimation():
    image_file = "m_3910505_nw_13_1_20150919_crop.tif"
    image_data = rasterio.open(image_file)

    width_in_projected_units = image_data.bounds.right - image_data.bounds.left
    height_in_projected_units = image_data.bounds.top - image_data.bounds.bottom

    #denote the upper left pixel
    row_min = 0
    col_min = 0

    #denote the lower right pixel
    row_max = image_data.height - 1
    col_max = image_data.width - 1

    #transform the coordinates
    topleft = image_data.transform * (row_min, col_min)
    botright = image_data.transform * (row_max, col_max)

    #read in the for bands (including the near-infared)
    b, g, r, n = image_data.read()

    filename = image_file
    with rasterio.open(filename) as src:
        band_blue = src.read(3)
    with rasterio.open(filename) as src:
        band_red = src.read(1)
    with rasterio.open(filename) as src:
        band_nir = src.read(4)

    numpy.seterr(divide='ignore', invalid='ignore')

    #calculate both the approximate and actual ndvi
    ndvi_approx = (2* band_red.astype(float) - band_blue.astype(float)) / band_blue
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

    print("The minimum NDVI approximatied is " + str(numpy.nanmin(ndvi_approx))) 
    print("The maximum NDVI approximatied is " + str(numpy.nanmax(ndvi_approx)))


    min=numpy.nanmin(ndvi_approx)
    max=numpy.nanmax(ndvi_approx)

    #set a midpoint for our analysis
    mid=0.1

    #set a normal color-scheme
    colormap = plt.cm.RdYlGn 
    norm = MidpointNormalize(vmin=min, vmax=max, midpoint=mid)
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)

    cbar_plot = ax.imshow(ndvi, cmap=colormap, vmin=min, vmax=max, norm=norm)

    #create the plot to show the NDVI estimation 
    ax.axis('off')
    ax.set_title('Normalized Difference Vegetation Index', fontsize=17, fontweight='bold')
    cbar = fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)
    fig.savefig("ndvi-image.png", dpi=200, bbox_inches='tight', pad_inches=0.7)

    # let's visualize
    plt.show()

#define a midpoint normalization class
class MidpointNormalize(colors.Normalize):   
    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
       
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return numpy.ma.masked_array(numpy.interp(value, x, y), numpy.isnan(value))


if __name__ == '__main__':
    #run the function
    ndvi_estimation()