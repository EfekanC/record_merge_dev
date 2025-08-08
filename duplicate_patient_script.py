import mysql.connector 
import os
from dotenv import load_dotenv

load_dotenv()
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')


def update_table(table_name, old_value, new_value):
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )

        cursor = connection.cursor()

        sql_query = f"UPDATE {table_name} SET {table_name}.patient = %s WHERE {table_name}.patient = %s;"
        cursor.execute(sql_query, (new_value, old_value))
        connection.commit()

        print(f"Rows updated in {table_name}: {cursor.rowcount}")

    except mysql.connector.Error as error:
        print(f"Error: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def update_invoice_items_customer_id(patient):
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DB')
        )

        cursor = connection.cursor()

        sql_query = """
            UPDATE invoice_items
            JOIN users ON users.patient = invoice_items.patient
            JOIN customers ON customers.user = users.id
            SET invoice_items.customer = customers.id
            WHERE invoice_items.patient = %s
            AND invoice_items.invoice IS NULL;
        """
        cursor.execute(sql_query, (patient,))
        connection.commit()

        print(f"Customer IDs updated in invoice_items: {cursor.rowcount}")
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    old_value = input("Enter the old value: ")
    new_value = input("Enter the new value: ")

    tables_to_update = ['notes', 'prescriptions', 'tasks', 'appointments', 'invoices', 'invoice_items', 'formcollections', 'adultadhdinfreport1of2', 'adultadhdinfreport2of2', 'adultadhdselfreport1of4', 'adultadhdselfreport2of4', 'adultadhdselfreport3of4', 'adultadhdselfreport4of4', 'adhdcardiac', 'adhdtxmonitoring', 'bloodpressurewtht', 'adhd12mfu', 'adultadhdinfreports', 'adultadhdselfreports', 'asrs', 'camhsdevelopmentalhistoryform', 'camhsreportonschoolfunctioning', 'rcadschild', 'rcadsparent', 'sdqparent', 'sdqself', 'sdqteacher', 'snapiv26parent', 'snapiv26teacher', 'cf2_staffrrmform', 'cf2_adhdform', 'cf2_aq10', 'cf2_aq29', 'cf2_asdinfreport', 'cf2_asdselfreport1', 'cf2_asdselfreport2', 'cf2_bragamberform', 'cf2_camhsdevelopmentalhistoryformv2', 'cf2_camhsscreeningform', 'cf2_eotrform', 'cf2_gad7', 'cf2_groupbookingtcs', 'cf2_patientrrmform', 'cf2_patienttriageupdate', 'cf2_phq9', 'cf2_pretitration', 'cf2_psychotherapyquestionnaire', 'cf2_screeningform', 'cf2_triageoutcomes', 'cf2_welfarearticle', 'cf2_welfarearticleview', 'cf2_welfareassessmentform', 'cf2_wenderutah', 'cf2_wfirs']

    for table in tables_to_update:
        update_table(table, old_value, new_value)
    
    update_invoice_items_customer_id(new_value)
