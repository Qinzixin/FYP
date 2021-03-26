from generate_test_set import generate_test_set

image_list = ["image/E/E.png","image/A/A.png","image/L/L.png"]
density = 0.00079432

if __name__ == "__main__":
    # sample points from images
    for l in image_list:
        generate_test_set(l,density)