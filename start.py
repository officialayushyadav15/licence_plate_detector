import cv2
import imutils

image = cv2.imread('result.jpeg')

# now we resize and standardize our image to 500
image = imutils.resize(image , width = 500)

cv2.imshow("Original Image",image)
cv2.waitKey(0)

# Now we will convert image to grey scale as it will reduce the dimension and complexity of the ima ge also there are few algorithm like canny,  etc which only works on grayscale images
gray =  cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Scale Image",gray)
cv2.waitKey(0)

#now we will reduce noise from our image and make it smooth
gray = cv2.bilateralFilter(gray , 11 ,17, 17)
cv2.imshow("Smoother Image", gray)
cv2.waitKey(0)

# Now we find the edge of image
edged = cv2.Canny(gray, 170,200)
cv2.imshow("Canny edge",edged)
cv2.waitKey(0)

# Now we will find the contours based on the images
cnrs, new = cv2.findContours(edged.copy() , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Here cnrs is contours which means that it is like the curve joining all the contiour points and new is the hierarchy - relationship, RETR_LIST retrieves all the contours but doesn't create any parent-child relationship and CHAIN_APPROX_SIMPLE removes all the redundant points and compress the contour by saving memory

# Now we will create a copy of our original image to draw all the contours
image1 = image.copy()
cv2.drawContours(image1, cnrs , -1, (0,255,0), 3)
cv2.imshow("Canny after contouring",image1)
cv2.waitKey(0)

# Now we dont wat all of the contours as we are just intrested in number plate but can't select randomly so we need to sort them on the basis of their areas. So we will select those areas which are maximum so we will select top 30 areas but since it gives in min to max so we have to reverse the order of sorting
cnrs = sorted(cnrs, key = cv2.contourArea, reverse = True)[:30]
NumberPlateCount = None

# Since we dont have any contour or we can say that it will show number of plates there are present in image. To draw 30 contours we will make copy of original image and use it as we don't want to edit anything in our original image
image2 = image.copy()
cv2.drawContours(image2, cnrs, -1, (0,255,0),3)
cv2.imshow("Top 30 Contours",image2)
cv2.waitKey(0)

# Now we will run loop on our contours to find the best possible contours of our expected number plate
c = 0
n = 1 #name of cropped image
for i  in cnrs:
    perimeter = cv2.arcLength(i, True) # perimeter is also called as arcLength and we can find it directly in python using arcLength function
    approx = cv2.approxPolyDP(i, 0.02*perimeter, True) # we have used approxPolyDP because it approximates the curve of ploygon with the precision
    if (len(approx) == 4): # 4 beecause that will be our number plate most probabllyy as our numberplate will have 4 sides and 4 corners
        NumberPlateCount = approx

        # Now we will crop our number plate
        x, y, w, h = cv2.boundingRect(i)
        crp_img = image[y:y+h , x:x+w]
        cv2.imwrite(str(n)+ ".png",crp_img)
        n=n+1
        break

cv2.drawContours(image,[NumberPlateCount], -1, (0,255,0),3)
cv2.imshow("Final Image",image)
cv2.waitKey(0)

crop_img_loc = "1.png"
cv2.imshow("Cropped Image",cv2.imread(crop_img_loc))
cv2.waitKey(0)

