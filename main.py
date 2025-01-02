import cv2
import os
from pyzbar.pyzbar import decode

#Open the default camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera is not opened.")

print("Camera is open. Show the QR code to the camera to scan it. Press 'q' to exit.")

qr_link = None

while True:

    ret, frame = cap.read()


    # Detect QR codes in the frame
    detected_barcodes = decode(frame)
    for barcode in detected_barcodes:
        qr_data = barcode.data.decode("utf-8")
        qr_type = barcode.type

        # Check QR code content is already displayed
        if qr_link != qr_data or qr_link is None:
            qr_link = qr_data
            print(f"QR Code Detected: {qr_link}")  # Print the new QR code content to the terminal


        # Draw a rectangle around the QR code
        points = barcode.polygon
        if len(points) == 4:
            pts = [(point.x, point.y) for point in points]
            pts = pts + [pts[0]]
            for i in range(len(pts) - 1):
                cv2.line(frame, pts[i], pts[i + 1], (0, 255, 0), 2)


        # Display the QR code content on the frame
        rect = barcode.rect
        cv2.putText(frame, qr_data, (rect.left, rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)



    # Display the captured frame
    cv2.imshow("QR Code Scanner", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Release the capture
cap.release()
cv2.destroyAllWindows()


