from pymongo import MongoClient
import os

'''
     Anurag:  self.tables.group({
   "initial": {},
   "reduce": function(obj, prev) {
       prev.maximumvalueage = isNaN(prev.maximumvalueage) ? obj.age : Math.max(prev.maximumvalueage, obj.age);
        }
    });

'''

class DB:

    def __init__(self, db_name, table_name):
        self.db_name = db_name
        self.table_name = table_name
        self.client = MongoClient()
        self.db = self.client[db_name]
        # db.name gives the name of the database
        self.table = self.db[table_name]
        # self.table.name gives the table_name

        #self.conn = db.connect(db_name)
        #self.conn.text_factory = str
        #self.cursor = self.conn.cursor()

    # insertion data
    def insert(self, data):
        # data has to be supplied as array of dictionaries
        if self.table_name == 'TRIE' :
            self.table.insert_many(data)
        elif self.table_name == 'CLIENT_DATA' :
            self.table.insert_many(data)
        elif self.table_name == 'SLAVE_SERVER' :
            self.table.insert_many(data)
        elif self.table_name == 'MASTER_SERVER' :
            self.table.insert_many(data)

    def select_all(self, key) :
        cursor = self.table.find()
        return cursor

    def select_user(self, user_id) :
        cursor = self.table.find({"user_id": user_id})
        return cursor

    def select_slave_server(self, slave_server_id) :
        cursor = self.table.find({"slave_id": slave_server_id})
        return cursor

    def select_server_load(self, load, inequality) : # inequality can take values from '='
        if inequality == '<'  :
            cursor = self.table.find({"load": {"$lt": load}})
        elif inequality == '>' :
            cursor = self.table.find({"load": {"$gt": load}})
        else :
            cursor = self.table.find({"load": load})
        return cursor


    def select_server_load(self, load, inequality) : # inequality can take values from '='
        if inequality == '<'  :
            cursor = self.table.find({"load": {"$lt": load}})
        elif inequality == '>' :
            cursor = self.table.find({"load": {"$gt": load}})
        else :
            cursor = self.table.find({"load": load})
        return cursor

    def select_max_load(self) :
        cursor = self.table.find_one(sort=[("load", -1)])["load"]
        return cursor

    def select_max_uploaded_data(self) :
        cursor = self.table.find_one(sort=[("data_amount", -1)])["data_amount"]
        return cursor

    def select_max_file_count(self) :
        cursor = self.table.find_one(sort=[("file_count", -1)])["file_count"]
        return cursor
        

    def exists(self, key) :
        if (self.table_name == 'TRIE') :
            pass
        elif (self.table_name == 'CLIENT_DATA') :
            pass
        elif (self.table_name == 'SLAVE_SERVER') :
            pass

def main():
    db = DB('skynet', 'CLIENT_DATA')
    db.insert([{
            "master_id" : "m1_mac",
            "file_count" : 10,
            "data_amount" : 2.30    
        }, {
            "master_id" : "m2_mac",
            "file_count" : 6,
            "data_amount" : 15
        }])

    print db.select_max_uploaded_data()
    # dic = {file_id : }


if __name__ == "__main__" :
    main()
