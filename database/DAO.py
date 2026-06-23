from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllYears():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(datetime) as year from sighting"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])

        cursor.close()
        cnx.close()
        result.sort(reverse=True)
        return result

    @staticmethod
    def getShapes(year):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape
                       FROM sighting s 
                       WHERE year(s.datetime) = %s 
                       AND s.shape IS NOT NULL 
                       AND s.shape != '' 
                       AND s.shape != '?'"""
            cursor.execute(query, (year,))

            for row in cursor:
                result.append(row["shape"])

        cursor.close()
        cnx.close()
        result.sort()
        return result

    @staticmethod
    def getSightings(anno, forma):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from sighting s 
                    where year(s.datetime)=%s and s.shape = %s"""

        cursor.execute(query, (anno,forma))

        for row in cursor:
            results.append(Sighting(**row))

        cursor.close()
        conn.close()
        return results