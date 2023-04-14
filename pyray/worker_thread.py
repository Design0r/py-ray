from PySide6.QtCore import QThread, Signal
import time


class WorkerThread(QThread):
    finished_signal = Signal(str)
    progress_signal = Signal(tuple)

    def __init__(self, renderer):
        super().__init__()
        self.renderer = renderer
        self.stop_flag = False

    def run(self):
        samples = 1
        start_time = time.time()
        while not self.stop_flag:
            sample_time = time.perf_counter()
            self.renderer.calculate()

            self.progress_signal.emit((samples, time.perf_counter() - sample_time, time.time() - start_time))
            samples += 1
            self.msleep(10)
        message = "Thread finished"
        self.finished_signal.emit(message)

    def stop(self) -> None:
        self.stop_flag = True
