from PIL import Image, ImageDraw, ImageOps
import FileUtils


def addBorder(image, thickness, color):
    img = Image.open(image)
    img = ImageOps.crop(img, thickness)
    img = ImageOps.expand(img, border=thickness, fill=color)
    img.show()


def addDivider(image, rows, cols, thickness, color):
    img = Image.open(image)
    width, height = img.size
    numRows = height // rows
    numCols = width // cols

    draw = ImageDraw.Draw(img)

    # Printing the rows
    counter = 1
    while counter < rows:
        draw.line((0, numRows * counter) + (width, numRows * counter),
                  fill=(color), width=thickness)
        counter += 1
    # Printing the columns
    counter = 1
    while counter < cols:
        draw.line((numCols * counter, 0) + (numCols * counter, height),
                  fill=color, width=thickness)
        counter += 1

    img.show()


def createImageFromBinary(sourceFileName, targetFileName):
    data = open(sourceFileName, "r")
    line = data.read()
    # Width/height in binary format
    binaryWidth = line[0:32]
    binaryHeight = line[32:64]
    # Converting width/height to integer format
    width = int(binaryWidth, 2)
    height = int(binaryHeight, 2)
    # This is the first number after the width/height
    startingNum = 64
    # Creating a blank new white image
    img = Image.new("RGB", (width, height), white)

    # Looping through width and height - Starting with going across the x axis
    for y in range(0, height):
        for x in range(0, width):
            # Variable storing 32 bits
            tempPixel = line[startingNum:startingNum + 32]
            # Breaking up the 32 bits into 8 bits (alpha, red, green, blue)
            # alpha = tempPixel[0:8]
            red = int(tempPixel[8:16], 2)
            green = int(tempPixel[16:24], 2)
            blue = int(tempPixel[24:32], 2)
            # Creating the RGB value
            rgb = (red, green, blue)
            # print(str(rgb))
            img.putpixel((x, y), rgb)
            # Incrementing to get the next 32 bits
            startingNum += 32
    img.show()
    img.save(targetFileName)


def saveImageAsBinary(sourceFileName, targetFileName):
    # Opening the image and a new file to write to
    image = Image.open(sourceFileName, "r")
    txtFile = open(targetFileName, "w")
    # Getting the images width/height then converting to binary with 32 bits
    width, height = image.size
    binaryWidth = str(bin(width))[2:].zfill(32)
    binaryHeight = str(bin(height))[2:].zfill(32)
    # Starting the binary string with the width and height at the beginning
    binaryImage = binaryWidth + binaryHeight
    # Getting the RGB ints for each pixel in a list
    pixelValues = list(image.getdata())
    # Looping through the list storing the values in different RGB variables
    for i in range(0, len(pixelValues)):
        alpha = "11111111"
        red = str(bin(pixelValues[i][0]))[2:].zfill(8)
        green = str(bin(pixelValues[i][1]))[2:].zfill(8)
        blue = str(bin(pixelValues[i][2]))[2:].zfill(8)
        # Concatenating the variables and adding it to the main string
        rgb = alpha + red + green + blue
        binaryImage += rgb
    # Writing the binary string to the text file
    txtFile.write(binaryImage)


imgSpace = "space.png"
white = (255, 255, 255)

# ** PART 1 **
# addBorder(imgSpace, 15, white)

# ** PART 2 **
# addDivider(imgSpace, 10, 10, 5, white)

# ** PART 3 **
# createImageFromBinary("pixels_small.txt", "Lab4Small.jpeg")
# createImageFromBinary("pixels_big.txt", "Lab4Big.jpeg")

# ** PART 4 **
# saveImageAsBinary("Lab4Small.jpeg", "Lab4Teapot.txt")
# saveImageAsBinary("road.jpeg", "Lab4Road.txt")

# ** TESTING PART 4 **
# createImageFromBinary("Lab4Teapot.txt", "Lab4Teapot.jpeg")
# createImageFromBinary("Lab4Road.txt", "Lab4Road.jpeg")
