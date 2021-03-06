import sqlite3
import datetime

class TutorialPipeline(object):

    def __init__(self, sqlite_file, sqlite_table):
	self.ids = set()
        self.sqlite_file = sqlite_file
        self.sqlite_table = sqlite_table

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_file = crawler.settings.get('SQLITE_FILE'),
            sqlite_table = crawler.settings.get('SQLITE_TABLE', 'items')
        )

    def process_item(self, item, spider):
        if item['seccode'] in self.ids:
            if item['flag'] == '2':
                self.conn.execute('update product set trustFee = ?,manageFee = ?,updateDate = ? where seccode = ? and comeFrom = ?',
                          (item['trustFee'], item["manageFee"], datetime.datetime.now().date(), item["seccode"], item["comeFrom"]))
            elif item['flag'] == '1':
                self.conn.execute('update product set accumulatedUnitnv = ?,unitnv = ?,updateDate = ? where seccode = ? and comeFrom = ?',
                          (item["accumulatedUnitnv"], item["unitnv"], datetime.datetime.now().date(), item["seccode"], item["comeFrom"]))
        else:
            self.ids.add(item['seccode'])
            self.conn.execute('replace into product values(?,?,?,?,?,?,?)',
                          (item["seccode"], item["trustFee"], item["manageFee"], item["accumulatedUnitnv"], item["unitnv"], item["comeFrom"], datetime.datetime.now().date()))
        return item

    def open_spider(self,spider):
	print("111111111111111111111111111111111111111111111111111111")
	self.conn = self.create_table(self.sqlite_file)

    def close_spider(self,spider):
	if self.conn is not None:
            self.conn.commit()
            self.conn.close()

    def create_table(self, filename):
        conn = sqlite3.connect(filename)
        conn.execute("""create table if not exists product
                     (seccode text not null,
                      trustFee text,
                      manageFee text,
                      accumulatedUnitnv text,
                      unitnv text,
                      comeFrom int not null,
                      updateDate text,
                      primary key(seccode,comeFrom)
                      )""")
        conn.commit()
        return conn
