"""
Implement a Simple Log Reader
You are given a very large log file on disk (can be GBs). Loading the whole file into memory is not allowed.

Design a class LogReader that supports the following operations efficiently:
1) tail(n) -> str
Return the last n lines of the log file as a string.

Requirements:
Must work for very large files.
Should not read the entire file unless necessary.
You may assume lines are separated by \n.
Use a fixed block_size (default 4096 bytes) and read the file from the end backward.

2) search(phrase) -> bool
Return True if the given UTF-8 string phrase appears anywhere in the file, otherwise False.

Requirements:
Must scan the file in chunks of size block_size.
Must correctly handle the case where the phrase spans across two chunks (cross-boundary matching).
lr = LogReader("app.log")

print(lr.tail(5))          # prints last 5 lines
print(lr.search("ERROR"))  # True/False

lr.close()
"""

import os
class LogReader:
    def __init__(self, filename, blocksize = 4096):
        self.filename = filename
        self.blocksize = blocksize
        self.file = open(filename, 'rb')

    def tail(self, n):
        if n <= 0:
            return ''
        
        f = self.file 
        f.seek(0, os.SEEK_END)
        pos = f.tell()

        newlines = 0

        while pos > 0 and newlines <= n:
            chunk = min(pos, self.blocksize)
            
            pos -= chunk
            f.seek(pos)

            data = f.read(chunk)
            for i in range(chunk - 1, -1, -1):
                if data[i] == ord('\n'):
                    newlines += 1
                if newlines == n + 1:
                    res = pos + i + 1
                    f.seek(res)
                    return f.read().decode('utf-8')
        
        f.seek(0)
        return f.read().decode('utf-8')
    
    def search(self, phrase):
        f = self.file
        if phrase == '':
            return True
        # convert str into bytes
        target = phrase.encode('utf-8')
        
        m = len(target)

        prevTail = b''
        f.seek(0)

        while True:
            data = f.read(self.blocksize)
            if not data:
                return False 
            data = prevTail + data 
            if data.find(target) != -1:
                return True
            
            keep = m - 1
            prevTail = data[-keep:] if keep > 0 else b''

    def close(self):
        self.file.close()



import tempfile
def writeTempLog(text: str) -> str:
    if text and not text.endswith("\n"):
        text += "\n"

    fd, path = tempfile.mkstemp()
    os.close(fd)
    with open(path, "wb") as f:
        f.write(text.encode("utf-8"))
    return path

# tail: always ends with newline
path = writeTempLog("a\nb\nc\nd\ne")
lr = LogReader(path, 4)  # small block forces backward multi-read
assert lr.tail(2).splitlines() == ["d", "e"]
assert lr.tail(5).splitlines() == ["a", "b", "c", "d", "e"]
assert lr.tail(10).splitlines() == ["a", "b", "c", "d", "e"]
assert lr.tail(0) == ""
lr.close()
os.remove(path)

# tail: single line + newline
path = writeTempLog("onlyOneLine")
lr = LogReader(path, 3)
assert lr.tail(1).splitlines() == ["onlyOneLine"]
lr.close()
os.remove(path)

# tail: empty file (no newline)
path = writeTempLog("")
lr = LogReader(path, 8)
assert lr.tail(3) == ""
lr.close()
os.remove(path)

# search: basic present/absent
path = writeTempLog("hello world\nERROR here\nbye")
lr = LogReader(path, 8)
assert lr.search("ERROR") is True
assert lr.search("MISSING") is False
lr.close()
os.remove(path)

# search: cross-boundary match (phrase spans chunks)
path = writeTempLog("abcde")  # with block=4, "abcd" + "e\n"
lr = LogReader(path, 4)
assert lr.search("cde") is True
assert lr.search("de\n") is True
assert lr.search("de") is True
assert lr.search("ab") is True
assert lr.search("cdef") is False
lr.close()
os.remove(path)