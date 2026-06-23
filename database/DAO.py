from database.DB_connect import DBConnect
from model.order import Order

from model.store import Store


class DAO():
    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(s):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct *
                    from orders o
                    where o.store_id = %s"""

        cursor.execute(query, (s,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(k,s):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct o1.order_id as or1, o2.order_id as or2, (oi1.quantity + oi2.quantity) as quantita, DATEDIFF(o1.order_date, o2.order_date) as giorni
                    from orders o1, orders o2, order_items oi1, order_items oi2
                    where o1.order_id = oi1.order_id 
                    and o2.order_id = oi2.order_id
                    and o1.order_id < o2.order_id 
                    and abs(DATEDIFF(o1.order_date, o2.order_date)) <= %s 
                    and abs(DATEDIFF(o1.order_date, o2.order_date)) > 0
                    and o1.store_id = %s
                    and o2.store_id = o1.store_id
                    group by o1.order_id , o2.order_id"""
        cursor.execute(query, (k,s))
        for row in cursor:
            result.append((row["or1"], row["or2"], row["quantita"], row["giorni"]))
        cursor.close()
        conn.close()
        return result


