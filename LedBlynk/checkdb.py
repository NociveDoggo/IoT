import sqlite3

def print_full_log():
    conn = sqlite3.connect('led_control.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM led_log ORDER BY timestamp DESC')
    
    print("\nRegistro completo:")
    for row in cursor.fetchall():
        print(row)
    
    conn.close()

print_full_log()