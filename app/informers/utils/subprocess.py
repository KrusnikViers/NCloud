import logging
import multiprocessing
import os
import signal


class Subprocess:
    def __init__(self):
        self._process = None

    def _get_process_info(self):
        # Should be overriden in derivative class with this information:
        # { 'name': 'informer name',
        #   'target': Process target function
        #   'args': Target function arguments }
        assert False

    def start(self):
        info = self._get_process_info()
        self._process = multiprocessing.Process(target=info['target'], name=info['name'], args=info['args'])
        self._process.daemon = True
        self._process.start()
        logging.info('Subprocess for {} launched at {}'.format(info['name'], self._process.pid))

    def terminate(self):
        if not self._process:
            return
        os.kill(self._process.pid, signal.SIGKILL)
        while self._process.is_alive():
            pass
        logging.info('Subprocess for {} terminated.'.format(self._get_process_info()['name']))
