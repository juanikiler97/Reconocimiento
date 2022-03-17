from matplotlib import pyplot as plt

def plot_single_image(img, title=None, size=(8, 8), cmap='viridis'):
	plt.figure(figsize=size)
	plt.xticks([])
	plt.yticks([])
	plt.grid(False)
	plt.imshow(img, cmap=cmap)
	if title:
		plt.title(title)
	plt.show()

def plot_multiple_images(imgs, size=(28, 18), cols=None, cmap='viridis', titles=None):
  plt.figure(figsize=size)
  count = len(imgs)
  if cols is None:
    cols = count
  rows = count // cols
  
  if count % cols != 0:
    rows += 1

  for index, img in enumerate(imgs):
    plt.subplot(rows, cols, index + 1)
    if titles:
      title = plt.title(titles[index], )
      plt.setp(title, color="white")
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(img, cmap=cmap)
  plt.show()