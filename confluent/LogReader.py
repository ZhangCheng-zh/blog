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
import tempfile
class LogReader:
    def __init__(self, filename, blocksize = 4096):
        self.filename = filename
        self.blocksize = blocksize # 4kb per time
        self.file = open(filename, 'rb') # open in read and binary mode

    def tail(self, n):
        if n <= 0:
            return ''
        
        f = self.file # f point to the same file object
        f.seek(0, os.SEEK_END) # move the file cursor to the very end of the file
        pos = f.tell() # return the current cursor position an an integer, now pos is the file size in bytes

        newlines = 0

        # if pos >= 0, the lopp will infinite
        while pos > 0 and newlines <= n:
            chunk = min(pos, self.blocksize) # if left file part smaller than blocksize, chunk equal left file part
            pos -= chunk # move curosr of head of target chunk file
            f.seek(pos)

            data  = f.read(chunk)
            for i in range(chunk - 1, -1, -1):
                if data[i] == ord('\n'): # ord('\n') is 10
                    newlines += 1
                    if newlines == n + 1: # find the n + 1 '\n' in reverse order
                        res = pos + i + 1
                        f.seek(res) # move cursor to next code after (n + 1)th '\n'
                        return f.read().decode('utf-8') # read out all content start from cursor
        f.seek(0)
        return f.read().decode('utf-8')
         
    
    def search(self, phrase):
        # f.read() return bytes, not a python str
        target = phrase.encode('utf-8')
        m = len(target)
        if m == 0:
            return True
        
        f = self.file
        f.seek(0) # set cursor to head of file object
        
        prevTail = b''

        while True:
            data = f.read(self.blocksize)
            if not data:
                return False 
            data = prevTail + data
            if data.find(target) != -1:
                return True
            
            prevTail = data[-(m - 1):]
        

    def close(self):
        self.file.close()


import os
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
assert lr.search("cdef") is False
lr.close()
os.remove(path)

# search: UTF-8 phrase spanning chunks
path = writeTempLog("aa你好吗bb")
lr = LogReader(path, 5)
assert lr.search("你好吗") is True
assert lr.search("好吗b") is True
assert lr.search("不存在") is False
lr.close()
os.remove(path)
