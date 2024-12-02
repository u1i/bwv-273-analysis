import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Read and display the image
img = mpimg.imread('bach.png')
plt.figure(figsize=(12, 8))
plt.imshow(img)
plt.axis('off')
plt.show()
