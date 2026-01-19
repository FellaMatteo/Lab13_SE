from database.DB_connect import DBConnect
from model.gene import Gene

class DAO:

    @staticmethod
    def get_geni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, funzione, essenziale, cromosoma
                    FROM gene"""

        cursor.execute(query)

        for row in cursor:
            gene = Gene(
                id = row['id'],
                funzione = row['funzione'],
                essenziale = row['essenziale'],
                cromosoma =row['cromosoma']
            )
            result.append(gene)

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_correlazione():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                        SELECT g1.id AS gene1, g2.id AS gene2, i.correlazione
                        FROM gene g1, gene g2, interazione i 
                        WHERE  g1.id = i.id_gene1 and g2.id = i.id_gene2 
                               and g2.cromosoma != g1.cromosoma
                               and g2.cromosoma>0
                               and g1.cromosoma>0
                        GROUP BY g1.id, g2.id
                        """

        cursor.execute(query)

        for row in cursor:
            result.append((row['gene1'], row['gene2'], row['correlazione']))

        cursor.close()
        conn.close()
        return result
