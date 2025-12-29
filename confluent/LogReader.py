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



# import os
# class LogReader:
#     # a very large log file on disk, need read into memory by chunk
#     def __init__(self, filename, blockSize = 4096):
#         self.filename = filename
#         self.blockSize = blockSize

#         self.file = open(filename, 'rb')
    
#     def tail(self, n):
#         # f.seek, f.tell, f.read
#         f = self.file 
#         # end position
#         f.seek(0, os.SEEK_END)
#         pos = f.tell()

#         newlines = 0 # record the '/n' count
#         result = 0 # record return position

#         while pos > 0 or newlines <= n: # scan from tail to head, reach head or find the n + 1 '/n', then stop
#             # start of each chunk
#             chunk = min(pos, self.blockSize)
#             # got to chun head
#             pos -= chunk
#             f.seek(pos)
            
#             # read the chunk
#             data = f.read(chunk) # data is list of chunk file

#             for i in range(chunk - 1, -1, -1):
#                 if data[i] == ord('\n'):
#                     newlines += 1
#                 if newlines == n + 1:
#                     result = pos + i + 1
#                     f.seek(result)
#                     return f.read().decode('utf-8')
#         # not find enough newlines in whole file, return whole file directly
#         f.seek(0)
#         return f.read().decode('utf-8')

#     def search(self, phrase):
#         f = self.file
#         f.seek(0)

#         phrase = phrase.encode('utf-8')
#         m = len(phrase)

#         # pick previous chunk's tail as head of next chunk
#         # to find cross chunk phrase
#         prevTail = b''

#         while True:
#             chunk = f.read(self.blockSize)
#             if not chunk: # no more file
#                 break

#             data = prevTail + chunk

#             idx = data.find(phrase)
#             if idx != -1:
#                 return True # find target
            
#             prevTail = data[-(m + 1):]
#         return False
    
#     def close(self):
#         self.file.close()
            


import os
class LogReader:
    def __init__(self, filename, blocksize = 4096):
        self.filename = filename
        self.blocksize = blocksize
        self.file = open(filename, 'rb')
    
    def tail(self, n):
        f = self.file 

        f.seek(0, os.SEEK_END)
        pos = f.tell() # get the position of file end

        newlines = 0 # record the count of '\n'
        result = 0 # store the head of return file

        while pos > 0 and newlines <= n:
            chunk = min(pos, self.blocksize) # size of next chunk

            pos -= chunk # head point to head of chunk
            f.seek(pos)

            data = f.read(chunk)
            for i in range(chunk - 1, -1, -1):
                if data[i] == ord('\n'):
                    newlines += 1
                if newlines == n + 1:
                    result = pos + i + 1
                    f.seek(result)
                    return f.read().decode('utf-8')
        
        f.seek(0)
        return f.read().decode('utf-8')

    def search(self, phrase):
        f = self.file 

        phrase = phrase.encode('utf-8')
        m = len(phrase)

        prevTail = b''

        f.seek(0)
        pos = f.tell() # start scan from head

        while True:
            chunk = self.blocksize

            data = f.read(chunk)
            if not data:
                break # already scan all file
            data = prevTail + data

            idx = data.find(phrase)
            if idx >= 0:
                return True
            
            prevTail = data[-(m + 1):]
            pos += chunk
        
        return False


lr = LogReader('./log.txt')
print(lr.tail(5))
# print(lr.tail(100))
print(lr.search('k'))
print(lr.search('t'))
print(lr.search('s'))
