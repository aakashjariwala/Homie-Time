import sqlite3
from datetime import datetime

class PreparedStatementHandler():
    
    def __init__(self, user):
        self.user = user
        return 

    def insertDefaultUsers(self):
        
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        
        default_george = [("Curious"),
                          ("George"),
                          ("curiousgeorge"),
                          ("george123"),
                          ("curiousgeorge@gmail.com"),
                          ("A very curious monkey")]
        
        default_johnwick = [("John"),
                            ("Wick"),
                            ("johnwick"),
                            ("johnwick123"),
                            ("johnwick@gmail.com"),
                            ("I love my dog")]
        
        default_jamesbond = [("James"),
                             ("Bond"),
                             ("jamesbond"),
                             ("jamesbond123"),
                             ("jamesbond@gmail.com"),
                             ("They call me 007")]
        
        cursor.execute("""
        INSERT INTO hometime_user ('firstname', 'lastname', 'username', 'passwordHash', 'email', 'bio')
        VALUES (?, ?, ?, ?, ?, ?)""", default_george)
        
        cursor.execute("""
        INSERT INTO hometime_user ('firstname', 'lastname', 'username', 'passwordHash', 'email', 'bio')
        VALUES (?, ?, ?, ?, ?, ?)""", default_johnwick)
        
        cursor.execute("""
        INSERT INTO hometime_user ('firstname', 'lastname', 'username', 'passwordHash', 'email', 'bio')
        VALUES (?, ?, ?, ?, ?, ?)""", default_jamesbond)
        
        cursor.close()
        return

    def deletePastEvents(self):
        
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        currentTime = datetime.now().time()
        currentDay = datetime.now().date()
        
        cursor.execute("""
        DELETE FROM hometime_event
        WHERE Event.day = currentDay
        AND Event.end_time < currentTime""")
        
        cursor.close()
        return