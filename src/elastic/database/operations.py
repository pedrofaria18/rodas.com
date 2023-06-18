import psycopg2


def select_docs_for_processing(is_active, cur):
    try:
        sql = f'''
         SELECT url_hash,
               html_hash,
               html,
               id,
               last_processing_data,
               url
          FROM html_document
         WHERE (last_visit_on > last_processing_data or last_processing_data is null)
            AND is_active = %s
         LIMIT 2000
        '''

        cur.execute(sql, (is_active,))

        response = cur.fetchall()

        if response is not None:
            #print(response[0][2])
            return response
        else:
            return None

    except (Exception, psycopg2.Error) as e:
        print('Erro ao obter os documentos HTML do banco de dados.')
        raise e


def update_processing_date(cur, conn, records):
    try:

        values = [dr[3] for dr in records]
        values = str(values).replace("[", "(").replace("]", ")")

        sql = f'''                    
            UPDATE html_document
            SET last_processing_data = NOW()
            WHERE id in {values};
        '''

        cur.execute(sql)
        conn.commit()

    except (Exception, psycopg2.Error) as e:
        print('Erro ao atualizar as datas de processamento.')
        raise e


def close_connection(cur, conn):
    cur.close()
    conn.close()
