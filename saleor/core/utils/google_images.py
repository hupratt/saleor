 
# In[ ]:
from google_images_download import google_images_download   #importing the library
from sqlite3 import Error
import sqlite3
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def select_all_books(conn):

    cur = conn.cursor()
    cur.execute("SELECT isbn FROM livre")
 
    rows = cur.fetchall()
    liste_isbn = []
    for row in rows:
        liste_isbn.append(row[0])
    return ",".join(liste_isbn)


database = "/home/hugo/Downloads/LPP-Master_2019_2019-06-30.db"

# create a database connection
conn = create_connection(database)
conn.text_factory = lambda x: str(x, 'latin1')
# conn.text_factory = str
with conn:
    isbn = select_all_books(conn)

    response = google_images_download.googleimagesdownload()   #class instantiation
    arguments = {"keywords":str(isbn), "limit":1, "print_urls":True,"format":"jpg", "size": '>800*600', "output_directory": "/home/hugo/Development/saleor/saleor/static/placeholders"}   #creating list of arguments
    paths, _ = response.download(arguments)   #passing the arguments to the function

    for isbn, image_path in paths.items():
        print(isbn, image_path[0])