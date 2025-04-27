
import random
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import threading

def rpm_uret():
    return random.randint(700, 3000) #Idle to mid RPM

def hiz_uret():
    return random.randint(0,120) #km/h
    
class ECUApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simule ECU")

        self.running = True
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.counter = 0
        
        self.rpm = 800
        self.speed = 0
        self.accelerating = False
        self.braking = False

        self.rpm_data = []
        self.speed_data = []
        self.time_data = []
        self.start_time = time.time()
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack()

        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()

        self.gaz_btn = tk.Button(
            btn_frame,
            text="Gas",
            width=15,
            font=("Helvetica", 14, "bold"),
            bg="#4CAF50",
            fg="black",
            activebackground="#45A049",
            relief=tk.RAISED,
            command=self.toggle_gaz
        )
        self.gaz_btn.pack(side=tk.LEFT, padx=20)

        self.fren_btn = tk.Button(
            btn_frame,
            text="Brake",
            width=15,
            font=("Helvetica", 14, "bold"),
            bg="#f44336",
            fg="red",
            activebackground="#d32f2f",
            relief=tk.RAISED,
            command=self.toggle_fren
        )
        self.fren_btn.pack(side=tk.LEFT, padx=20)
    
        self.fig, (self.ax_rpm, self.ax_speed) = plt.subplots(2, 1, figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack()

        # Background data
        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.daemon = True
        self.update_thread.start()

    def toggle_gaz(self):
        self.accelerating = not self.accelerating
        if self.accelerating:
            self.gaz_btn.config(relief=tk.SUNKEN, text="Gaz basili")
        else:
            self.gaz_btn.config(relief=tk.RAISED, text="Gaz")

    def toggle_fren(self):
        self.braking = not self.braking
        if self.braking:
            self.fren_btn.config(relief=tk.SUNKEN, text="Fren basili")
        else:
            self.fren_btn.config(relief=tk.RAISED, text="Fren")

    def update_data(self):
        while self.running:
            current_time  = time.time() - self.start_time

            if self.accelerating:
                self.rpm = min(self.rpm + 200, 6000)
                self.speed = min(self.speed + self.rpm * 0.005, 250)
            elif self.braking:
                self.speed = max(self.speed - 5, 0)
                self.rpm = max(self.rpm - 300, 800)
            else:
                self.rpm = max(self.rpm - 100, 800)
                self.speed = max(self.speed - 1, 0)

            self.time_data.append(self.counter)
            self.counter += 1
            self.rpm_data.append(self.rpm)
            self.speed_data.append(self.speed)

            #Show last 20 data
            self.time_data = self.time_data[-20:]
            self.rpm_data = self.rpm_data[-20:]
            self.speed_data = self.speed_data[-20:]

            #Updates graphics
            self.ax_rpm.clear()
            self.ax_speed.clear()

            self.ax_rpm.plot(self.time_data, self.rpm_data, label="RPM", color="red")
            self.ax_speed.plot(self.time_data, self.speed_data, label="Speed", color="blue")

            self.ax_rpm.set_ylabel("RPM")
            self.ax_speed.set_ylabel("Speed (km/h)")
            self.ax_speed.set_xlabel("Time (second)")

            self.ax_rpm.legend()
            self.ax_speed.legend()
            self.canvas.draw()
            time.sleep(1)

    def on_closing(self):
        self.running = False   
        self.root.destroy() 

if __name__ == "__main__":
    root = tk.Tk()
    app = ECUApp(root)
    root.mainloop()

