from PIL import Image, ImageDraw, ImageFont, ImageChops
import textwrap
import os




# gives the background image a grayscale to allow easier reading of txt
def apply_tint(im, tint_color):
	tinted_im = ImageChops.multiply(im, Image.new('RGB', im.size, tint_color))
	return tinted_im

# places the trademark logo at the bottom of the image (hardcoded placement)
def place_logo(bkg, logo):
	bkg.paste(logo, ((540-65/2), (1010-65)), logo)
	return bkg

# places the trademark logo at the bottom of the image (hardcoded placement)
def place_trademark(im, trademark, font):
	draw = ImageDraw.Draw(im)
	bbox =  im.getbbox()
	W = bbox[2]
	H = bbox[3]
	draw.text(((W-800/2)/2, 1010), trademark, font=font)
	return im

# places the txt in the centre of the image
def place_txt(im, txt, font):
	draw = ImageDraw.Draw(im)
	w, h = draw.textsize(txt, font=font)
	bbox =  im.getbbox()
	W = bbox[2]; H = bbox[3]

	# determine the number of lines needed to fit the txt on the image
	lines = textwrap.wrap(txt, width=24)
	n_lines = len(lines)
	pad = -10

 	# place the lines of the txts one on top of the other
	current_h = H/2 - (n_lines*h/2)
	for line in lines:
		w, h = draw.textsize(line, font=font)
		draw.text(((W - w) / 2, current_h), line, font=font)
		current_h += h + pad

# determine is the given path is an image
def is_img(path):
	ext = path[-4:]
	if (ext == ".jpg") or (ext == ".png") or (ext == "jpeg"):
		return True
	return False

# gets the paths of the images to be used
def get_im_paths(files):
	pic_paths = []
	for file in files:
		if is_img(file):
			pic_paths.append(file)
	return pic_paths

# reads the txts from the txts.txts file
def get_txts(file):
	with open(file) as f:
		content = f.readlines()
	return [x.strip() for x in content]

# creates and saves an image
def build_image(im_path, txt, im_count = '', logoify = True):
	W = 1920
	H = 1080
	im = Image.open(im_path).resize((W,H))
	im = apply_tint(im, (90,90,90))
	draw = ImageDraw.Draw(im)

	cap_font = ImageFont.truetype("utils/simplicity.otf",105)
	place_txt(im, txt, cap_font)

	# if the 'add trademark' option is selected then add the logo and trademark
	if (logoify):
		trademark = "Lifting.Motivations"
		tm_font = ImageFont.truetype("utils/BebasNeue.otf",62)
		place_trademark(im, trademark, tm_font)
		logo = Image.open("utils/logo.png").resize((65,65))
		place_logo(im, logo)

	im.save('out/' + str(im_count) + '.png')
	print "Output image saved as: " + 'out/' + str(im_count)  + '.png'

def creat_txt_image_sequances():
	dir_paths = os.listdir("../overlayer/in/raw")
	im_paths = get_im_paths(dir_paths)
	txts = get_txts("../overlayer/in/txt.txt")
	im_count = 0

	for txt in txts:
		print "Overlaying " + "..."
		build_image('in/raw/' + im_paths[0], txt, im_count, False) #logoify = False
		im_count = im_count + 1
