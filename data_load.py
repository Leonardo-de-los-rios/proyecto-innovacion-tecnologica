import os, requests, psycopg2
from dotenv import load_dotenv
from bs4 import BeautifulSoup

def create_tables(conn):
    try:
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            product_name VARCHAR(100) NOT NULL,
            price INTEGER NOT NULL,
            quotas VARCHAR(100) NOT NULL,
            shipment VARCHAR(80) NULL,
            PRIMARY KEY (product_name, price, quotas)
        );
        ''')
        conn.commit()
        print("Tabla creada con éxito.")
    except Exception as e:
        print(f"Error creando la tabla! {e}")
        conn.rollback()
    finally:
        cur.close()

def format_name(name):
    lower = name.lower()
    words = lower.split()
    format = "-".join(w.capitalize() for w in words)
    return format

def scraping_ml(product_name):
    url = f"https://listado.mercadolibre.com.ar/{product_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content,'html.parser')
    productos = soup.find_all('div',class_="poly-card__content")

    lista_productos = []
    for prod in productos:
        try:
            nombre = prod.find('a',class_="poly-component__title").text
        except:
            nombre = prod.find('h2',class_="poly-box poly-component__title").text

        precio = prod.find('span',class_="andes-money-amount__fraction").text
        precio_sin_puntos = precio.replace(".", "") 
        precio = int(precio_sin_puntos) 
        try:
            cuotas = prod.find('span',class_="poly-price__installments poly-text-positive").text   
        except:
            cuotas = prod.find('span',class_="poly-price__installments poly-text-primary").text

        try:
            envio = prod.find('div',class_="poly-component__shipping").text
        except:
            lista_productos.append((nombre,precio,cuotas,None))
            continue   
        lista_productos.append((nombre,precio,cuotas, envio))

    productos_ordenados = sorted(lista_productos, key=lambda x: x[1])
    lista_productos = productos_ordenados[:10]
    return lista_productos


def insert_data(conn, nombre_producto, precio, cantidad_cuotas, envio):
    try:
        cur = conn.cursor()

        cur.execute('''
        INSERT INTO products (product_name, price, quotas, shipment) 
        VALUES (%s, %s, %s, %s);
        ''', (nombre_producto, precio, cantidad_cuotas, envio))

        print(f"Datos insertados del Producto: {nombre_producto}")
    
    except Exception as e:
        print(f"Error insertando los datos: {e}")
        conn.rollback()
    finally:
        cur.close()

def main():
    try:
        load_dotenv()
        conn_string = os.environ["NEON_DB"]
        conn = psycopg2.connect(conn_string)
        
        create_tables(conn)

        # Esta parte se debe iterar por producto buscado for product in products:
        product_name = input("Ingresa un nombre: ")         #Esta parte se debe cambiar, porque ya traemos el celu, y lo iteramos
        format = format_name(product_name)
        product_list = scraping_ml(format)
        for p in product_list:
            nombre,precio,cuotas, envio = p
            if envio != None:
                insert_data(conn, nombre, precio, cuotas, envio)
            else:
                insert_data(conn, nombre, precio, cuotas, None)

    except Exception as e:
        print(f"Error conectando a la base de datos: {e}")
    
    finally:
        if conn:
            conn.close()
            print("Conexión cerrada")

if __name__ == "__main__":
    main()