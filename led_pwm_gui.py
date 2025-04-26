import RPi.GPIO as GPIO
import tkinter as tk
import threading
import time

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define LED pins
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

# Set up LED pins as PWM outputs
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

red_pwm = GPIO.PWM(RED_PIN, 1000)  # 1000Hz frequency
green_pwm = GPIO.PWM(GREEN_PIN, 1000)
blue_pwm = GPIO.PWM(BLUE_PIN, 1000)

red_pwm.start(0)  # Start with 0% duty cycle (off)
green_pwm.start(0)
blue_pwm.start(0)

# Function to update LED brightness
def update_red(value):
    red_pwm.ChangeDutyCycle(int(value))

def update_green(value):
    green_pwm.ChangeDutyCycle(int(value))

def update_blue(value):
    blue_pwm.ChangeDutyCycle(int(value))

# Timer function to automatically adjust brightness
def auto_timer():
    while True:
        red_pwm.ChangeDutyCycle(100)  # Set red to full brightness
        green_pwm.ChangeDutyCycle(50) # Set green to 50% brightness
        blue_pwm.ChangeDutyCycle(25)  # Set blue to 25% brightness
        time.sleep(5)  # Wait 5 seconds

        red_pwm.ChangeDutyCycle(10)
        green_pwm.ChangeDutyCycle(90)
        blue_pwm.ChangeDutyCycle(60)
        time.sleep(5)

# Exit the program safely
def exit_program():
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()
    window.destroy()

# Create GUI window
window = tk.Tk()
window.title("LED Brightness Controller")

# Create sliders
red_slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, label="Red Brightness", command=update_red)
red_slider.pack(pady=5)

green_slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, label="Green Brightness", command=update_green)
green_slider.pack(pady=5)

blue_slider = tk.Scale(window, from_=0, to=100, orient=tk.HORIZONTAL, label="Blue Brightness", command=update_blue)
blue_slider.pack(pady=5)

# Create exit button
exit_button = tk.Button(window, text="Exit", command=exit_program)
exit_button.pack(pady=20)

# Start the timer in a separate thread
timer_thread = threading.Thread(target=auto_timer, daemon=True)
timer_thread.start()

# Start GUI event loop
window.mainloop()
