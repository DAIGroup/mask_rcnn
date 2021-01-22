import signal

work = True


def signal_handler(sig, frame):
    global work
    print('User pressed Ctrl+C, quitting ...')
    work = False


signal.signal(signal.SIGINT, signal_handler)
