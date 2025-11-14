#Feito por Francisco Emerson e Kaua Muniz
import sqlite3 as sq


connect = sq.connect("Steam.db")
cursor = connect.cursor()


cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")


tabelas = cursor.fetchall()


for sql in tabelas:
    print(sql[0])
    print("-" * 80)

connect.close()
print("✅ Schema exibido com sucesso!")
