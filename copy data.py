import mariadb
import mysql.connector

# ps_image
# ps_image_lang
# ps_image_shop

# ps_stock
# ps_stock_mvt
# ps_stock_mvt_reason
# ps_stock_mvt_reason_lang



# Connection details for source (MariaDB) and destination (MySQL) databases
source_config = {
    'user': 'exampleuser',
    'password': 'examplepass',
    'host': 'localhost',
    'port': 3307,
    'database': 'exampledb'
}

dest_config = {
    'user': 'prestashop',
    'password': 'prestashop',
    'host': 'localhost',
    'port': 3306,
    'database': 'prestashop'
}
# ps_dpd_price_rule
# ps_dpd_price_rule_carrier
# ps_dpd_price_rule_payment
# ps_dpd_price_rule_shop
# ps_dpd_price_rule_zone
source_table = 'ps_dpd_price_rule_zone'
target_table = source_table

def get_table_names(conn):
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    return [row[0] for row in cur.fetchall()]

def clean_destination_table(dst_conn, table):
    dst_cur = dst_conn.cursor()
    dst_cur.execute(f"DELETE FROM `{table}`")
    dst_conn.commit()
    print(f"Cleaned destination table: {table}")
    dst_cur.close()

def copy_table_data(src_conn, dst_conn, table):
    src_cur = src_conn.cursor()
    dst_cur = dst_conn.cursor()
    src_cur.execute(f"SELECT * FROM `{table}`")
    rows = src_cur.fetchall()
    if not rows:
        print(f"No data found in source table {table}.")
        return
    columns = [desc[0] for desc in src_cur.description]
    placeholders = ','.join(['%s'] * len(columns))
    insert_sql = f"INSERT INTO `{table}` ({', '.join(columns)}) VALUES ({placeholders})"
    dst_cur.executemany(insert_sql, rows)
    dst_conn.commit()
    print(f"Transferred {len(rows)} rows from {table}.")
    src_cur.close()
    dst_cur.close()

def main():
    # Connect to MariaDB (source)
    src_conn = mariadb.connect(**source_config)
    # Connect to MySQL (destination)
    dst_conn = mysql.connector.connect(**dest_config)
    try:
        # Clean destination table before copying
        clean_destination_table(dst_conn, target_table)
        # Copy data
        copy_table_data(src_conn, dst_conn, source_table)
        print("Data copy completed.")
    finally:
        src_conn.close()
        dst_conn.close()

if __name__ == "__main__":
    main()