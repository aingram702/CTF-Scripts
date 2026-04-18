# Barcode Decoder built custom for BTLO "Barcode World" CTF
# custom built by Andrew Ingram
from pyzbar import pyzbar
import cv2

# image decoder function
def decode(image):
    # decodes all barcodes from an image
    decoded_objects = pyzbar.decode(image)
    for obj in decoded_objects:
        # draw the barcode
        # print("detected barcode:", obj)
        image = draw_barcode(obj, image)
        # print barcode type & data
        # print("Type:", obj.type)
        # print("Data:", obj.data)
        # print()

    return image


# draw barcode function
def draw_barcode(decoded, image):
    # n_points = len(decoded.polygon)
    # for i in range(n_points):
    #     image = cv2.line(image, decoded.polygon[i], decoded.polygon[(i+1) % n_points], color=(0, 255, 0), thickness=5)
    # uncomment above and comment below if you want to draw a polygon and not a rectangle
    image = cv2.rectangle(image, (decoded.rect.left, decoded.rect.top), 
                            (decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
                            color=(0, 255, 0),
                            thickness=5)
    return image


# build final string function
def build_final_string(image_paths):
    """Return a single string of all decoded barcode values across
    one or more images, concatenated in read order (top-to-bottom,
    left-to-right)."""
    all_values = []
    for path in image_paths:
        img = cv2.imread(path)
        decoded_objects = pyzbar.decode(img)
        # sort each image's barcodes in read order
        decoded_objects = sorted(decoded_objects, key=lambda o: (o.rect.top, o.rect.left))
        if decoded_objects:
            for obj in decoded_objects:
                all_values.append(obj.data.decode("utf-8"))
        else:
            # unreadable barcode – use '_' as placeholder
            all_values.append("_")
    return "".join(all_values)


# now main function
if __name__ == "__main__":
    from glob import glob
    import re

    # match any PNG files containing digits
    barcodes = [f for f in glob("*.png") if re.search(r'\d+', f)]
    
    def get_num(f):
        m = re.search(r'\d+', f)
        return int(m.group()) if m else 0
        
    # sort by numerical value in the filename
    barcodes.sort(key=get_num)
    for barcode_file in barcodes:
        # load the image to opencv
        img = cv2.imread(barcode_file)
        # decode detected barcodes & get the image
        # that is drawn
        img = decode(img)
        # show the image
        # cv2.imshow("img", img)
        # cv2.waitKey(0)

    # print the final concatenated string of all decoded values
    final = build_final_string(barcodes)
    print("Final string:", final)

    # decode space-separated decimals to ascii
    decoded_message = []
    for token in final.split():
        if token.isdigit():
            decoded_message.append(chr(int(token)))
        else:
            decoded_message.append(token)
            
    decoded_str = "".join(decoded_message)
    print("\nDecoded message:")
    print(decoded_str)
    
    with open("decoded_flag.txt", "w") as f:
        f.write(decoded_str)