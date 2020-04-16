import threading
import sys
from resources.tool import fr_logs
import time
from resources.face_activity.fr_activity import fr_activity

class camThread(threading.Thread):
    def __init__(self, thread_id, setting):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.setting = setting
    def kill(self):
        self.killed = True

    def run(self):
        # if self.setting == 'traffic':
        #     pass
        #     #trafficPreview(str(self.stream_id), self.stream_url)
        # elif self.setting == 'recognition':
        camPreview(str(self.thread_id), self.setting)

listThread = []

def createThread(thread_id, setting):
    thread = camThread(thread_id, setting)
    listThread.append(thread)

def startThread(thread_id):
    for i in listThread:
        if (i.thread_id == thread_id):
            i.start()
            i.run = True
            return 1
    return 0

def statusThread(thread_id):
    for i in listThread:
        if (i.thread_id == thread_id):
            if (i.isAlive()):
                return "true"
            else:
                return "false"

def stopThread(thread_id):
    for i in listThread:
        if (i.thread_id == thread_id):
            i.run = False
            listThread.remove(i)

# def trafficPreview(stream_id, stream_url):
#     t = threading.currentThread()
#     if stream_url == "0":
#         stream_url = int(stream_url)
#     matdoxe(stream_id,stream_url,t)

def camPreview(thread_id, setting):
    t = threading.currentThread()
    i = 0
    while getattr(t, "run", True):
        print("Working")
        i += 1 
        if i==10:
            break
        
def runTask(thread_id, setting):
    createThread(thread_id, setting)
    startThread(thread_id)
    print("So luong dang hoat dong: ", threading.activeCount())
    print("So doi tuong thread: ", threading.currentThread())
    print("Danh sanh cac luong: ", threading.enumerate())

    print(statusThread(thread_id))

def stopTask(thread_id):
    stopThread(thread_id)
    print("So luong dang hoat dong: ", threading.activeCount())
    print("So doi tuong thread: ", threading.currentThread())
    print("Danh sanh cac luong: ", threading.enumerate())

def statusStream():
    try:
        status_thraed = {
            'running': threading.activeCount(),
            'threadNumber': threading.currentThread(),
            'threadList': threading.enumerate(),
        }
        print(listThread)

        return status_thraed
    except:
        fr_logs.logger.error("----- statusStream")
        fr_logs.logger.error(sys.exc_info()[0])
        status_thraed = {
            'running': '0',
            'threadNumber': '0',
            'threadList': '0'
        }
        return status_thraed