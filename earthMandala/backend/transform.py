from PIL import Image
 
im1 = Image.open("grid1.png").convert('RGB')
 
im2 = Image.open("grid2.png").convert('RGB')
 
frames = [im1,im1,im1,im1,im1] 
#100 frames of transform
for i in range(106):
  if(i>100):
    frames.append(im2)
  else:
    alpha = i/100
    im3 = Image.blend(im1, im2, alpha)
    frames.append(im3)

frames[0].save(
    "transform.gif",
    format="GIF",
    save_all=True,
    append_images=frames[1:],
    duration=20, 
    loop=0,
    optimize=False
)

