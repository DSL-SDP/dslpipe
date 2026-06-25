from dslpipe.utils.logging import get_logger

logger = get_logger(__name__)

import socket

class Progress(object):

    def __init__(self, length, step=None, prog_msg=None, comm=None):
        if length <= 0:
            raise ValueError(
                "Progress length must be a positive integer, got %r." % length
            )

        if not prog_msg is None:
            self.msg = prog_msg
        else:
            self.msg = 'Progress: %d of ' +  ('%d%s in %s...' % (length, ' for process %s' % comm.rank if comm else '', socket.gethostname()))

        if step is None:
            if length < 10:
                step = 1
            elif length < 10000:
                step = length // 10
            else:
                step = length // 100

        if step <= 0:
            raise ValueError(
                "Progress step must be a positive integer, got %r." % step
            )

        num = length // step + 1
        self.cnts = [ i * step for i in range(num) ]

    def show(self, cnt):
        if cnt in self.cnts:
            logger.info(self.msg % cnt)


if __name__ == '__main__':
    from caput import mpiutil
    comm = mpiutil.world
    # comm = None

    lg = 7
    if mpiutil.rank0:
        pg = Progress(lg, step=2, comm=comm)
    for i in range(lg):
        if mpiutil.rank0:
            pg.show(i)

    lg = 7
    pg = Progress(lg, step=2, comm=comm)
    for i in range(lg):
        pg.show(i)

    pg1 = Progress(lg, step=None, comm=comm)
    for i in range(lg):
        pg1.show(i)

    lg = 20
    pg2 = Progress(lg, step=None, comm=comm)
    for i in range(lg):
        pg2.show(i)

    lg = 23
    pg3 = Progress(lg, step=None, comm=comm)
    for i in range(lg):
        pg3.show(i)

    lg = 10106
    pg4 = Progress(lg, step=None, comm=comm)
    for i in range(lg):
        pg4.show(i)
