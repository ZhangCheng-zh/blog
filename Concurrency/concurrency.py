# Coarse-grained locking
import threading

class TicketBooking:
    def __init__(self):
        self._lock = threading.lock()
        self._seatOwners = {}

    def bookSeat(self, seatId, visitorId):
        with self._lock:
            if seatId in self.seatOwner:
                return False
            self._seatOwners[seatId] = visitorId
            return True
        

# Read-write locks
# Also called shared-exclusive lock. It has two modes: read(shared) and write(exclusive)
# they're just reading and can't corrupt each other's view. But the write lock is exclusive.
# When a thread wants to write, it waits for all readers to finish, then blocks everyone else
# until the write completes.

## read preference lock
import threading

class Cache:
    def __init__(self):
        self.dataLock = threading.Lock() # against write
        self.readCount = 0
        self.readCountLock = threading.Lock() # 
        self.data = {}
    
    def get(self, key):
        with self.readCountLock: # very short read lock
            self.readCount += 1
            if self.readCount == 1:
                self.dataLock.acquire()
        # read count lock release, but count remain
        try:
            return self.data.get(key)
        finally:
            # create read count lock again after finish read to update readCount
            with self.readCountLock:
                self.readCount -= 1
                if self.readCount == 0: # not more read, release write lock
                    self.dataLock.release()

    def put(self, key, value):
        with self.dataLock:
            self.data[key] = value

## write preference lock
# Condition = Lock + “wait queue” + “notify”.
class ReadWriteLock:
    def __init__(self):
        self.mu = threading.Lock()
        self.cond = threading.condition(self.mu)
        self.readerCount = 0
        self.writerActive = False
        self.writeWaiting = 0
    
    def acquireRead(self):
        with self.cond:
            # read wait afte active writer
            while self.writerActive or self.writerWaiting > 0:
                self.cond.wait() # wait write
            # no write active and no write waiting, start read
            self.readerCount += 1
    
    def releaseRead(self):
        with self.cond:
            # release one read
            self.readerCount -= 1
            # if all read be released, release rwlock
            if self.readerCount == 0:
                self.cond.notify_all()
    
    def acquireWrite(self):
        with self.cond:
            # put write into wait
            self.writerWaiting += 1
            # if lock used by a write or a read, keep waiting
            while self.writerActive or self.readerCount > 0:
                self.cond.wait()
            # wait end, wait -= 1 and active writing
            self.writerWaiting -= 1
            self.writerActive = True
    
    def releaseWrite(self):
        with self.cond:
            # release active write, then release rwlock, priority to next write, then read
            self.writeActive = False
            self.cond.notify_all()

class Cache:
    def __init__(self):
        self.rwLock = ReadWriteLock()
        self.data = {}

    def get(self, key):
        self.rwLock.acquireRead()
        try:
            return self.data.get(key)
        finally:
            self.rwLock.releaseRead()
    
    def put(self, key, value):
        self.rwLock.acquireWrite()
        try:
            self.data[key] = value
        finally:
            self.rwLock.releaseWrite()
    