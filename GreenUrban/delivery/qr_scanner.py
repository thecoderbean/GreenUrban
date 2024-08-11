import cv2
from pyzbar import pyzbar

def scan_qr_code():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        # Find and decode QR codes
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            order_id = obj.data.decode("utf-8")
            print(f"Order ID: {order_id}")

            # Draw a rectangle around the QR code
            (x, y, w, h) = obj.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, order_id, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Here you can call a function to update the order status
            update_order_status(order_id)

        # Display the frame
        cv2.imshow("QR Code Scanner", frame)

        # Exit the scanner when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and close windows
    cap.release()
    cv2.destroyAllWindows()

def update_order_status(order_id):
    import requests
    url = f"http://localhost:8000/update_order_status/{order_id}"
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'status': 3,
        'delivery_boy_id': '1',  # Replace with the actual delivery boy ID
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())

if __name__ == "__main__":
    scan_qr_code()