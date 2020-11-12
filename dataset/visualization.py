import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm


def visualize_df(tensor):
    """Basic 3D visualization for a distance field tensor.

    :param tensor: Distance Field (DF) tensor, np.array, shape = (32, 32, 32)
    :return: None
    """

    if len(tensor.shape) == 4:
        tensor = np.squeeze(tensor, 0)

    # The following portion attempts to extract the shape from the DF
    # display zero voxels in DF
    x, y, z = np.where(tensor <= 0.5)
    color = tensor[x, y, z]
    
    fig2 = plt.figure("Zero DF")
    ax2 = fig2.add_subplot(111, projection='3d')
    ax2.scatter(z, x, y, zdir='z', c=cm.jet(color), s=0.6)

def visualize_sdf(tensor):
    """Basic 3D visualization for a signed distance field tensor.

    :param tensor: Signed Distance Field (SDF) tensor, np.array, shape = (32, 32, 32)
    :return: None
    """

    if len(tensor.shape) == 4:
        tensor = np.squeeze(tensor, 0)

    # find voxels with finite sdf values
    finite_region = np.isfinite(tensor) * 1
    x, y, z = np.nonzero(finite_region)
    finite_color = tensor[x, y, z]

    # color mapping for finite regions
    norm = matplotlib.colors.Normalize(vmin=min(finite_color), vmax=max(finite_color))
    cmap = cm.hot
    m = cm.ScalarMappable(norm=norm, cmap=cmap)

    # plot finite SDF voxels
    fig = plt.figure("Finite SDF")
    ax = fig.add_subplot(111, projection='3d')
    color_list = []
    for i in range(len(x)):
        color_list.append(m.to_rgba(finite_color[i]))
    ax.scatter(z, x, y, zdir='z', c=color_list, s=0.6)



def visualize_df_voxel(tensor):
    """3D visualization for a distance field tensor, where each values on the boundary is 	       represented through solid shapes.

    :param tensor: Distance Field (DF) tensor, np.array, shape = (32, 32, 32)
    :return: None
    """

    if len(tensor.shape) == 4:
        tensor = np.squeeze(tensor, 0)

    volume = np.less_equal(tensor, 0.5)
    volumeTransposed = np.transpose(volume, (2, 0, 1))
    
    fig = plt.figure("Zero DF with voxels")
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(volumeTransposed)


def visualize_sdf_voxel(tensor):
    """3D visualization for a signed distance field tensor, where each values on the boundary is 	       represented through solid shapes.

    :param tensor: Signed Distance Field (SDF) tensor, np.array, shape = (32, 32, 32)
    :return: None
    """

    if len(tensor.shape) == 4:
        tensor = np.squeeze(tensor, 0)

    # find voxels with finite sdf values
    finite_region = np.isfinite(tensor)*1

    # extract finite values
    volume = np.greater(finite_region, 0)
    volumeTransposed = np.transpose(volume, (2, 0, 1))
    
    fig = plt.figure("Finite SDF with voxels")
    ax = fig.add_subplot(111, projection='3d')
    ax.voxels(volumeTransposed)


def show():
    """ Shows all constructed figures. Mainly for visualizing multiple 3D figures at once
    """
    plt.show()


def plot_curves(loss, iou, accuracy, metadata):
    """ Plots the curves for a model run, given the arrays loss, iou, accuracy arrays and 		corresponsding metadata

    Args:
        loss: nxi array of losses, where n - number of curves to compare (usually train vs 		validation) and i - number of iterations for the plot

        iou: nxi array of intersection over union values, where n - number of curves to compare 	(usually train vs validation) and i - number of iterations for the plot

        accuracy: nxi array of accuracy, where n - number of curves to compare (usually train vs 		validation) and i - number of iterations for the plot

	metadata: Array of n strings - what kind of data is present (usually "Train", "Validation")
    """
    plot_a_curve(loss, metadata, "Loss")
    plot_a_curve(iou, metadata, "IOU")
    plot_a_curve(accuracy, metadata, "Accuracy")

def plot_a_curve(data, metadata, curve_type):
    """ Plots the curves for a model run, given the arrays loss, iou, accuracy arrays and 		corresponsding metadata

    Args:
        loss: array of losses, where n - number of curves to compare (usually train vs 			validation) and i - number of iterations for the plot

	metadata: What kind of data is present (usually train, validation)

	curve_type: (Loss, IOU, Accuracy)
    """
    title = ""
    plt.title("Train vs Validation Error")
    n = len(data[0]) # number of epochs
    for i in range(len(metadata)):
      if i != 0:
        title += " vs "
      title += metadata[i]
      plt.plot(range(1,n+1), data[i], label=metadata[i])
    title = title + " " + curve_type
    plt.title(title)
    plt.xlabel("Epoch")
    plt.ylabel(curve_type)
    plt.legend(loc='best')
    plt.show()
