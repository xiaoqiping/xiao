import time
import signal


def test(i):
    time.sleep(i % 4)
    print ("%d within time" % (i))
    return i


if __name__ == '__main__':
    def handler(signum, frame):
        raise AssertionError

for i in range(1, 10):
    try:
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(3)
        test(i)
    except AssertionError:
        print ("%d timeout" % (i))
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)