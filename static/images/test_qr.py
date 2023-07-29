import qrcode
img = qrcode.make('www.google.com')
type(img)  # qrcode.image.pil.PilImage
img.save("test2_file.png")