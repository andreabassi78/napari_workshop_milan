
from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square, remove_small_objects
from skimage.color import label2rgb
import matplotlib.pyplot as plt

coins = data.coins()
thresh = threshold_otsu(coins)
closing_size = 4
bw = closing(coins > thresh, square(closing_size))
cleared = remove_small_objects(clear_border(bw), 20)
label_image = label(cleared)
image_label_overlay = label2rgb(label_image, image=coins, bg_label=0)

fig, axes = plt.subplots(1, 2, figsize=(8, 3), sharey=True)
axes[0].imshow(coins, cmap=plt.cm.gray)
axes[0].contour(label_image, [0.5], linewidths=1.2, colors='y')
axes[1].imshow(image_label_overlay)


plt.tight_layout()

plt.show()