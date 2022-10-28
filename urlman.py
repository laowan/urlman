# -*- coding: UTF-8 -*-
import os
import sys
import math
import random
import codecs
import chardet

DB = None

class Url:
    def __init__(self):
        self.title = ''
        self.path = ''
        self.tags = []
        self.description = ''
        self.times = 0

    def __str__(self):
        s = '<' + str(self.times) + '>'
        s += '[' + self.title + ']'
        s += '(' + self.path + ')'
        #s += 'desc: ' + self.description + '\n'
        #s += 'tags: '
        #for tag in self.tags:
        #    s += tag + ','
        #s += '\n'
        #s += 'times: ' + str(self.times)
        return s.encode('gbk')

    def db_str(self):
        split_char = ';'
        s = self.title + split_char
        s += self.path + split_char
        s += self.description + split_char
        tag_count = len(self.tags)
        if tag_count > 0:
            n = 1
            for tag in self.tags:
                suffix = ',' if n < tag_count else ''
                s += tag + suffix
        s += split_char
        s += str(self.times)
        s += '\n'
        return s

class Database:
    def __init__(self):
        self.db_path = ''
        self.items = []

    def open(self, path):
        db = codecs.open(path, 'a+', 'utf-8')
        if not db:
            return False
        self.db_path = path
        db.seek(0)

        lines = db.readlines()
        for line in lines:
            items = line.rstrip().split(';')
            url = Url()
            url.title, url.path, url.description = items[0], items[1], items[2]
            url.tags.append(items[3])
            url.times = int(items[4])
            #for n in range(3, len(items)):
            #    if len(items[n]) > 0:
            #        url.tags.append(items[n])
            self.items.append(url)

        db.close()
        return True

    def save(self):
        assert len(self.db_path) > 0
        db = codecs.open(self.db_path, 'w', 'utf-8')
        if not db:
            return False

        for url in self.items:
            s = url.db_str()
            db.write(s)

        db.close()
        return True

    # return: id of this url
    def add(self, path, title = '', desc = '', tag = []):
        url = Url()
        url.title = title.decode('gbk')#.encode('utf8')
        url.path = path
        url.tag = tag
        url.description = desc
        self.items.append(url)
        return len(self.items)

    def modify(self, idx, target, content):
        assert idx >= 0 and idx < len(self.items)
        url = self.items[idx]
        if target == 'title':
            url.title = content
        elif target == 'desc':
            url.description = content
        elif target == 'tag':
            url.tags.append(content)
        elif target == 'cleartags':
            url.tags = []

    def remove(self, idx):
        assert idx >= 0 and idx < len(self.items)
        self.items.remove(self.items[idx])

    def random(self):
        assert len(self.items) > 0
        idx = random.randint(0, len(self.items) - 1)
        url = self.items[idx]
        url.times += 1
        return url

    def dump(self):
        count = 0
        for url in self.items:
            count += 1
            print '{}:{}'.format(count, url)

def main(argv):
    n = len(argv)
    print n, argv
    func = 'open'
    if n > 1:
        func = argv[1]

    db = Database()
    opened = db.open('url_db.txt')
    if not opened:
        print 'open db failed'
        return False

    if func == 'add':
        assert n > 2
        path = argv[2]
        title = argv[3] if n > 3 else ''
        db.add(path, title)
        db.save()
    elif func == 'remove':
        idx = int(argv[2]) - 1
        db.remove(idx)
        db.save()
    elif func == 'random':
        url = db.random()
        db.save()
        print url
    elif func == 'open':
        url = db.random()
        db.save()
        print url

        import webbrowser
        webbrowser.open(url.path)
    elif func == 'modify':
        idx = int(argv[2]) - 1
        target = argv[3]
        content = argv[4]
        db.modify(idx, target, content)
        db.save()
    elif func == 'dump' or func == 'list':
        db.dump()
    elif func == 'help':
        print 'add [url_path], add a url path to database'
        print 'random, random return a url in database'

    return True


if __name__ == "__main__":
    main(sys.argv)

