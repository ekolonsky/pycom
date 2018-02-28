import _thread
import time




class Buffer:

    def __init__(self, startwith=[]):
        self._queue = startwith
        _thread.start_new_thread(self._loop, [3]) # ever loop with small delay
        pass

    def push(self, message):
        self._queue.append(message)
        print('in <-', message)
        pass

    def pull(self):
        self._busy = True
        n = len(self._queue)
        if n > 0:
            message = self._queue.pop(0)
            print('out->', message)

    def _loop(self, delay):
        while True:
              self.pull()
              time.sleep(delay)


queue = Buffer(startwith=[1,2,3,4,5])
