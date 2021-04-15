from PIL import Image
from random import randrange
from math import sqrt

#6 possible colors that the groups can be. If you want more than 6 groups,
#add more colors to this list in RGB
colors = [(255,0,0), (0,0,255), (0,255,0), (255,255,0), (0,255,255), (255,0,255) ]

#Opens an image called 'Data.png' in folder 'photos'
#Makes sure the colors are in RGB
#Take the image dimensions - used to calculate x,y coordinates
image = Image.open(r"photos\Data.png")
image = image.convert("RGB")
width, height = image.size

#Amount of groups. Change this number accordingly
k_mean_amt = 3

#Default: Data points are black
#Change this color if your data points are different colors
datapoint_color = (0,0,0)

#Takes a 1D list and turns it into 2D
#Group len is the width of the image
#Purpose: Allows getting coordinates in image_read(image) easier
def split_list(mylist, grouplen):
		newlist = []
		running_idx= 0
		for i in range( len(mylist) // grouplen):
				newlist.append(mylist[running_idx:running_idx+grouplen])
				running_idx += grouplen

		return newlist

#looks at the image and returns a list of the data points' coordinates
def image_read(image):
	d_points = []

	pixel_values = list(image.getdata())

	ordered_values = split_list(pixel_values, width)

	for idxr, row in enumerate(ordered_values):
		for idxc, pixel in enumerate(row):
			if pixel == (0,0,0):
				d_points.append([idxc,idxr])

	return d_points

#Initializing where the k means are randomly
#Makes sure that the two points can't be the same
def set_k_coords(k_mean_amt):
	k_means = []
	for i in range(k_mean_amt):
		x_val = randrange(width)
		y_val = randrange(height)

		if [x_val, y_val] in k_means:
			return set_k_coords(k_mean_amt)

		k_means.append([x_val,y_val])

	return k_means

#Takes in the data points and k means and finds out which
#group to assign each data point to using euclidean distance
#Returns a list of groups (Which k mean the data point is closest to)
#with the same length and order of the list of datapoints.
def closeness(d_points, k_coords):
	distances =[]
	groups = []

	for point in d_points:
		for k_coord in k_coords:
			distance = sqrt((point[0] - k_coord[0])**2 + (point[1] - k_coord[1])**2)
			distances.append(distance)
		
		#get the closest distance, find out which group that refers to
		#adds that group to groups
		best_distance = min(distances)
		dist_idx = distances.index(best_distance)
		k_mean = k_coords[dist_idx]
		groups.append(k_mean)
		distances = []

	return groups

#Looks at which data point is in which group
#and calculates the average of those data points
#to return a new k_mean and groups
def k_coords_mean(groups, pixels, k_coords):
	pixel_idx = []
	new_k_coords = []
	x = 0
	y = 0

	for k_coord in k_coords:
		pixel_idx = []
		x = 0
		y = 0

		for idx, point in enumerate(groups):
			if point == k_coord:
				pixel_idx.append(idx)
				x += pixels[idx][0]
				y += pixels[idx][1]

		#If the group is empty, keep the k mean in the same location
		try:
			x = x/len(pixel_idx)
			y = y/len(pixel_idx)
		except ZeroDivisionError:
			x,y = k_coord[0], k_coord[1]

		new_k_coords.append([x,y])

	new_groups = closeness(pixels, new_k_coords)

	#repeat this until the k mean stops moving
	if new_k_coords == k_coords:
		return new_k_coords, new_groups
	else:
		return k_coords_mean(new_groups, pixels, new_k_coords)

#Colors in the groups of data points and displays the image
#now colored
def color_groups(pixels, colors, groups, k_coords, image):
	imgpixels = image.load()

	for color, k_point in enumerate(k_coords):
		for idx, group in enumerate(groups):
			if group == k_point:
				x = pixels[idx][0]
				y = pixels[idx][1]
				imgpixels[x, y] = colors[color]

	image = image.resize((round(image.size[0]*15),round(image.size[1]*15)), Image.NONE)
	image.show()


pixels = image_read(image)
k_coords = set_k_coords(k_mean_amt)
groups = closeness(pixels, k_coords)

k_coords, groups = k_coords_mean(groups, pixels, k_coords)

color_groups(pixels, colors, groups, k_coords, image)




		
