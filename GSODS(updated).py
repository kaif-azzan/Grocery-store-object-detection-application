import cv2
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image, ImageTk
from fpdf import FPDF

# ======================== CONSTANTS AND CONFIGURATION ========================
PATHS = {
    'model_config': 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt',
    'frozen_model': 'frozen_inference_graph.pb',
    'labels': 'coco_labels.txt',
    'cost_data': 'cost.txt',
    'icon': 'Graphicloads-Flat-Finance-Global.ico',
    'video_source': 'd.mp4'
}

class App:
    def __init__(self, master=None):
        # ======================== MAIN APPLICATION WINDOW ========================
        self.window = tk.Tk()
        self.window.title("Grocery Store Object Detection")
        self.window.configure(bg='black')
        self.window.geometry("1500x720")
        self.window.resizable(0, 0)
        
        # Initialize video capture and object detection model
        self.video_source = PATHS['video_source']
        self.vid = VideoCapture(self.video_source)
        self.detected_items = []
        self.item_names = []
        
        self._setup_ui()
        self._initialize_object_detection()
        self.update()
        self.window.mainloop()

    def _setup_ui(self):
        """Set up the main user interface components"""
        # Header
        tk.Label(self.window, text="Grocery Store Object Detection", font=15,
                bg='blue', fg='white', pady=10).pack(fill='x')
        
        # Video canvas
        self.canvas = tk.Canvas(self.window, height=600, width=self.vid.width)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH)
        
        # Control buttons
        button_frame = tk.Frame(self.window, bg='black')
        button_frame.pack(fill='x', pady=10)
        
        tk.Button(button_frame, text="Exit", bg="maroon", width=20,
                 command=self.window.destroy).pack(side=tk.LEFT, padx=20)
        tk.Button(button_frame, text="Checkout", bg="dark green", width=20,
                 command=self._open_checkout).pack(side=tk.RIGHT, padx=20)

    def _initialize_object_detection(self):
        """Initialize the object detection model"""
        self.model = cv2.dnn_DetectionModel(PATHS['frozen_model'], PATHS['model_config'])
        self.model.setInputSize(320, 320)
        self.model.setInputScale(1.0/127.5)
        self.model.setInputMean((127.5, 127.5, 127.5))
        self.model.setInputSwapRB(True)
        
        # Load class labels
        with open(PATHS['labels'], 'rt') as f:
            self.class_labels = f.read().rstrip('\n').split('\n')

    def update(self):
        """Update the video feed and object detection"""
        ret, frame = self.vid.get_frame()
        
        if ret:
            # Perform object detection
            class_ids, confidence, bboxes = self.model.detect(frame, confThreshold=0.64)
            self._process_detections(frame, class_ids, bboxes)
            
            # Display frame
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(750, 300, image=self.photo, anchor=tk.CENTER)
            
        self.window.after(1, self.update)

    def _process_detections(self, frame, class_ids, bboxes):
        """Process detected objects and draw bounding boxes"""
        font_scale = 1
        font = cv2.FONT_HERSHEY_PLAIN
        
        if class_ids is not None:
            self.detected_items = []
            self.item_names = []
            
            for class_id, box in zip(class_ids.flatten(), bboxes):
                item_name = self.class_labels[class_id-1]
                self.detected_items.append(class_id)
                self.item_names.append(item_name)
                
                # Draw bounding box and label
                cv2.rectangle(frame, box, (255, 0, 0), 1)
                cv2.putText(frame, item_name, (box[0]+10, box[1]+20), 
                            font, fontScale=font_scale, 
                            color=(255, 255, 255), thickness=1)

            # Remove duplicates
            self.detected_items = list(set(self.detected_items))

    def _open_checkout(self):
        """Open the checkout/payment window"""
        CheckoutWindow(self.detected_items, self.item_names)

# ======================== CHECKOUT WINDOW CLASS ========================
class CheckoutWindow:
    def __init__(self, item_ids, item_names):
        self.window = tk.Toplevel()
        self.window.title("Payment Information")
        self.window.geometry('800x600')
        
        self.item_ids = item_ids
        self.item_names = item_names
        self.total = self._calculate_total()
        
        self._setup_ui()

    def _calculate_total(self):
        """Calculate total cost from detected items"""
        with open(PATHS['cost_data'], 'r') as f:
            prices = [int(line.strip()) for line in f]
        
        return sum(prices[item_id-1] for item_id in self.item_ids)

    def _setup_ui(self):
        """Set up the checkout interface"""
        # Payment form elements
        form_frame = tk.Frame(self.window)
        form_frame.pack(pady=20)
        
        # Card number fields
        tk.Label(form_frame, text="Card Number:").grid(row=0, column=0, sticky='w')
        self.card_entries = [tk.Entry(form_frame, width=4) for _ in range(4)]
        for i, entry in enumerate(self.card_entries):
            entry.grid(row=0, column=i+1, padx=2)
        
        # CVV field
        tk.Label(form_frame, text="CVV:").grid(row=1, column=0, sticky='w', pady=10)
        self.cvv_entry = tk.Entry(form_frame, width=5)
        self.cvv_entry.grid(row=1, column=1, sticky='w')
        
        # Expiration date
        tk.Label(form_frame, text="Exp Date (MM/YY):").grid(row=2, column=0, sticky='w')
        self.mm_entry = tk.Entry(form_frame, width=3)
        self.yy_entry = tk.Entry(form_frame, width=3)
        self.mm_entry.grid(row=2, column=1, sticky='w')
        tk.Label(form_frame, text="/").grid(row=2, column=2)
        self.yy_entry.grid(row=2, column=3, sticky='w')
        
        # Total display
        total_frame = tk.Frame(self.window)
        total_frame.pack(pady=20)
        tk.Label(total_frame, text=f"Total Amount: ${self.total}", 
                font=('Arial', 14, 'bold')).pack()
        
        # Action buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Pay", bg='green', fg='white',
                 command=self._process_payment).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cancel", bg='red', fg='white',
                 command=self.window.destroy).pack(side=tk.LEFT, padx=10)

    def _process_payment(self):
        """Validate and process payment information"""
        # Get input values
        card_number = '-'.join([entry.get() for entry in self.card_entries])
        cvv = self.cvv_entry.get()
        exp_date = f"{self.mm_entry.get()}/{self.yy_entry.get()}"
        
        # Simple validation
        if (all(len(entry.get()) == 4 for entry in self.card_entries) and \
           len(cvv) == 3 and \
           len(self.mm_entry.get()) == 2 and \
           len(self.yy_entry.get()) == 2:
            
            self._save_transaction(card_number, exp_date)
            self._generate_receipt()
            messagebox.showinfo("Success", "Payment processed successfully!")
            self.window.destroy()
        else:
            messagebox.showerror("Error", "Please check your payment information")

    def _save_transaction(self, card_number, exp_date):
        """Save transaction details to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('transactions.txt', 'a') as f:
            f.write(f"{timestamp} | {card_number} | {exp_date} | ${self.total}\n")

    def _generate_receipt(self):
        """Generate PDF receipt"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Header
        pdf.cell(0, 10, "XYZ Super Market", 0, 1, 'C')
        pdf.ln(5)
        
        # Transaction details
        pdf.cell(0, 10, f"Date: {datetime.now().date()}", 0, 1)
        pdf.cell(0, 10, f"Time: {datetime.now().time().strftime('%H:%M:%S')}", 0, 1)
        pdf.ln(10)
        
        # Items list
        pdf.cell(0, 10, "Items Purchased:", 0, 1)
        for item in set(self.item_names):
            count = self.item_names.count(item)
            pdf.cell(0, 10, f"{item} x{count}", 0, 1)
        
        # Total
        pdf.ln(10)
        pdf.cell(0, 10, f"Total Amount: ${self.total}", 0, 1)
        
        pdf.output("receipt.pdf")

# ======================== VIDEO CAPTURE CLASS ========================
class VideoCapture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)
        
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        ret, frame = self.vid.read()
        if ret:
            return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# ======================== LOGIN WINDOW ========================
class LoginWindow:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Login")
        self.window.configure(bg='black')
        self._setup_ui()
        self.window.mainloop()

    def _setup_ui(self):
        """Set up login interface"""
        tk.Label(self.window, text="WELCOME", bg='black', fg='red').pack(pady=10)
        
        # Login form
        form_frame = tk.Frame(self.window, bg='black')
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Username:", bg='black', fg='white').grid(row=0, column=0)
        self.username = tk.Entry(form_frame)
        self.username.grid(row=0, column=1)
        
        tk.Label(form_frame, text="Password:", bg='black', fg='white').grid(row=1, column=0)
        self.password = tk.Entry(form_frame, show='*')
        self.password.grid(row=1, column=1)
        
        # Login button
        tk.Button(self.window, text="Login", bg='green', fg='white',
                 command=self._check_credentials).pack(pady=20)

    def _check_credentials(self):
        """Validate login credentials"""
        # In a real application, implement proper authentication
        if self.username.get() == "" and self.password.get() == "":
            self.window.destroy()
            App()
        else:
            messagebox.showerror("Error", "Invalid credentials")

# ======================== MAIN ENTRY POINT ========================
if __name__ == "__main__":
    LoginWindow()
