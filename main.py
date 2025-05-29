from multiprocessing import Process, Queue
from keyboard import keyboard
from gray_img import blink

if __name__ == '__main__':
    # Queue for inter-process communication
    blink_queue = Queue()

    # Start the keyboard process
    keyboard_process = Process(target=keyboard, args=(blink_queue,))
    keyboard_process.start()

    # Start the blink detection process
    blink_process = Process(target=blink, args=(blink_queue,))
    blink_process.start()

    keyboard_process.join()
    blink_process.join()