import sqlite3

connection = sqlite3.connect("bytecat.db")
cursor = connection.cursor()

# Elimina tablas antiguas para reconstruir la BD limpia
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS web_users")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS suppliers")
cursor.execute("DROP TABLE IF EXISTS admin_notes")
cursor.execute("DROP TABLE IF EXISTS customers")

# Tabla de productos
cursor.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    image TEXT NOT NULL,
    supplier TEXT,
    cost_price REAL
)
""")

# Tabla de usuarios web
cursor.execute("""
CREATE TABLE web_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    department TEXT,
    active INTEGER DEFAULT 1,
    last_login TEXT,
    notes TEXT
)
""")

# Tabla de clientes web
cursor.execute("""
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    address TEXT,
    city TEXT,
    created_at TEXT
)
""")

# Tabla de pedidos simulados
cursor.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    total_price REAL NOT NULL,
    order_status TEXT,
    payment_method TEXT,
    created_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
)
""")

# Tabla de proveedores
cursor.execute("""
CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    contact_name TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    payment_terms TEXT,
    internal_notes TEXT
)
""")

# Tabla de notas internas
cursor.execute("""
CREATE TABLE admin_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_by TEXT,
    created_at TEXT,
    confidential INTEGER DEFAULT 1
)
""")


# Datos de productos
products = [
("Lenovo ThinkPad X1", "Portátiles", "i7 - 16GB RAM - SSD 512GB", 599.00, "img/thinkpad-x1.png", 8, "TechSupplier SL", 399.99),
("HP EliteBook 840", "Portátiles", "i5 - 8GB RAM - SSD 256GB", 399.00, "img/none.png", 10, "TechSupplier SL", 280.00),
("Dell Latitude 7490", "Portátiles", "i5 - 16GB RAM - SSD 512GB", 449.00, "img/none.png", 7, "ReTech Corp", 310.00),
("MacBook Air 2019", "Portátiles", "i5 - 8GB RAM - SSD 256GB", 699.00, "img/none.png", 5, "Apple Renew", 520.00),
("Asus ZenBook", "Portátiles", "i7 - 16GB RAM - SSD 1TB", 799.00, "img/none.png", 6, "Asus Renew", 600.00),

("Teclado mecánico RGB", "Periféricos", "Switch Blue - Retroiluminado", 79.00, "img/teclado.png", 15, "KeyTech", 39.99),
("Ratón gaming Logitech", "Periféricos", "16000 DPI - RGB", 49.00, "img/none.png", 20, "LogiDistrib", 25.00),
("Monitor Dell 24\"", "Monitores", "Full HD - HDMI", 119.00, "img/monitor.png", 6, "Dell Renew", 79.99),
("Monitor LG 27\"", "Monitores", "QHD - IPS", 189.00, "img/none.png", 5, "LG Distrib", 130.00),
("Auriculares HyperX", "Periféricos", "Sonido 7.1", 59.00, "img/none.png", 12, "Kingston Audio", 30.00),

("Router TP-Link AX50", "Redes", "WiFi 6 - Doble banda", 89.00, "img/router.png", 10, "NetDistrib", 49.99),
("Switch 8 puertos", "Redes", "Gigabit", 39.00, "img/none.png", 14, "NetDistrib", 20.00),
("Access Point Ubiquiti", "Redes", "Alta cobertura", 129.00, "img/none.png", 8, "Ubiquiti Spain", 90.00),
("Cable Ethernet CAT6", "Redes", "10m", 9.00, "img/none.png", 50, "CableTech", 3.00),
("Tarjeta red PCIe", "Redes", "Gigabit", 29.00, "img/none.png", 11, "NetDistrib", 15.00),

("SSD Kingston 1TB", "Componentes", "SATA III", 69.00, "img/ssd.png", 25, "Kingston", 44.99),
("SSD Samsung 970 EVO", "Almacenamiento", "NVMe 1TB", 79.00, "img/none.png", 18, "Samsung Renew", 60.00),
("Disco duro WD 2TB", "Almacenamiento", "7200 RPM", 59.00, "img/none.png", 9, "WD Distrib", 35.00),
("Pendrive 128GB", "Almacenamiento", "USB 3.0", 19.00, "img/none.png", 30, "FlashTech", 8.00),
("Tarjeta SD 64GB", "Almacenamiento", "Clase 10", 12.00, "img/none.png", 22, "FlashTech", 5.00),

("Cámara IP 1080p", "Domótica", "Visión nocturna", 49.00, "img/camara.png", 20, "SmartHome Inc", 19.99),
("Kit domótica Alexa", "Domótica", "Control voz", 129.00, "img/none.png", 10, "Amazon Distrib", 90.00),
("Sensor movimiento", "Domótica", "Detección", 25.00, "img/none.png", 16, "SmartHome Inc", 10.00),
("Bombilla inteligente", "Domótica", "RGB WiFi", 15.00, "img/none.png", 40, "SmartLight", 6.00),
("Enchufe inteligente", "Domótica", "Control remoto", 18.00, "img/none.png", 35, "SmartLight", 8.00),

("Tablet Samsung Tab A", "Tablets", "10\" 32GB", 199.00, "img/none.png", 7, "Samsung Renew", 140.00),
("iPad 7ª generación", "Tablets", "32GB WiFi", 299.00, "img/none.png", 5, "Apple Renew", 220.00),
("Surface Go", "Tablets", "Windows", 349.00, "img/none.png", 4, "Microsoft Renew", 260.00),
("Huawei MediaPad", "Tablets", "10\"", 179.00, "img/none.png", 6, "Huawei Distrib", 120.00),
("Lenovo Tab M10", "Tablets", "Android", 149.00, "img/none.png", 8, "Lenovo Distrib", 100.00),

("Impresora HP Laser", "Oficina", "B/N", 129.00, "img/none.png", 6, "HP Distrib", 90.00),
("Impresora Epson", "Oficina", "Color", 159.00, "img/none.png", 5, "Epson Distrib", 110.00),
("Escáner Canon", "Oficina", "Alta resolución", 99.00, "img/none.png", 4, "Canon Distrib", 70.00),
("Silla oficina", "Oficina", "Ergonómica", 139.00, "img/none.png", 9, "OfficeTech", 90.00),
("Mesa escritorio", "Oficina", "Ajustable", 199.00, "img/none.png", 3, "OfficeTech", 140.00)
]

cursor.executemany("""
INSERT INTO products (name, category, description, price, image, stock, supplier, cost_price)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", products)

# Usuarios web vulnerables intencionadamente
web_users = [
    ("Laura", "Martín", "laura.martin@bytecatsolutions.com", "laura.martin", "Laura2026!", "admin", "Dirección", 1, None, "CEO con acceso completo al panel."),
    ("Iván", "Ortega", "ivan.ortega@bytecatsolutions.com", "ivan.ortega", "Ventas123", "ventas", "Comercial", 1, None, "Jefe de ventas. Puede consultar pedidos y clientes."),
    ("David", "Molina", "david.molina@bytecatsolutions.com", "david.molina", "Dev2026", "developer", "Desarrollo externo", 1, None, "Programador externo. Acceso temporal pendiente de revisar.")
]

# Clientes ficticios
customers = [
    ("Carlos", "Gómez", "carlos.gomez@example.com", "+34 611 100 201", "Calle Aurora 12", "Valencia", "2026-01-05"),
    ("Ana", "López", "ana.lopez@example.com", "+34 611 100 202", "Avenida del Mar 45", "Alicante", "2026-01-08"),
    ("Miguel", "Santos", "miguel.santos@example.com", "+34 611 100 203", "Calle Norte 8", "Madrid", "2026-01-18"),
    ("Paula", "Fernández", "paula.fernandez@example.com", "+34 611 100 204", "Calle Jardín 21", "Sevilla", "2026-02-02"),
    ("Javier", "Ruiz", "javier.ruiz@example.com", "+34 611 100 205", "Avenida Central 9", "Valencia", "2026-02-14"),
    ("Sofía", "Castro", "sofia.castro@example.com", "+34 611 100 206", "Calle Luna 17", "Barcelona", "2026-02-22"),
    ("Daniel", "Ortiz", "daniel.ortiz@example.com", "+34 611 100 207", "Calle Roble 4", "Málaga", "2026-03-01"),
    ("Natalia", "Herrera", "natalia.herrera@example.com", "+34 611 100 208", "Avenida Sol 30", "Murcia", "2026-03-10"),
    ("Raúl", "Sánchez", "raul.sanchez@example.com", "+34 611 100 209", "Calle Río 11", "Granada", "2026-03-16"),
    ("Elena", "Moreno", "elena.moreno@example.com", "+34 611 100 210", "Calle Mayor 77", "Zaragoza", "2026-04-04"),
    ("Pablo", "Navarro", "pablo.navarro@example.com", "+34 611 100 211", "Avenida Europa 6", "Bilbao", "2026-04-12"),
    ("Clara", "Domínguez", "clara.dominguez@example.com", "+34 611 100 212", "Calle Olivo 19", "Córdoba", "2026-05-01"),
    ("Hugo", "Martínez", "hugo.martinez@example.com", "+34 611 100 213", "Calle Sur 3", "Toledo", "2026-05-09"),
    ("Irene", "Vega", "irene.vega@example.com", "+34 611 100 214", "Avenida Verde 55", "Valencia", "2026-05-20"),
    ("Adrián", "Molina", "adrian.molina@example.com", "+34 611 100 215", "Calle Estrella 14", "Madrid", "2026-06-02")
]

cursor.executemany("""
INSERT INTO customers (first_name, last_name, email, phone, address, city, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", customers)

cursor.executemany("""
INSERT INTO web_users (first_name, last_name, email, username, password, role, department, active, last_login, notes)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", web_users)

# Pedidos ficticios 2026
orders = [
    (1, 1, 1, 599.00, "Completado", "Tarjeta terminada en 4242", "2026-01-15"),
    (2, 6, 1, 79.00, "Completado", "Bizum", "2026-02-03"),
    (3, 11, 1, 89.00, "Enviado", "PayPal", "2026-02-18"),
    (4, 21, 2, 98.00, "Completado", "Tarjeta terminada en 1111", "2026-03-07"),
    (5, 8, 1, 119.00, "Pendiente", "Bizum", "2026-03-29"),
    (6, 16, 1, 69.00, "Completado", "PayPal", "2026-04-11"),
    (7, 4, 1, 699.00, "Procesando", "Tarjeta terminada en 2222", "2026-05-02"),
    (8, 26, 1, 199.00, "Completado", "Bizum", "2026-06-14"),
    (9, 31, 1, 129.00, "Enviado", "PayPal", "2026-08-22"),
    (10, 35, 1, 199.00, "Pendiente", "Tarjeta terminada en 3333", "2026-10-06")
]

cursor.executemany("""
INSERT INTO orders (customer_id, product_id, quantity, total_price, order_status, payment_method, created_at)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", orders)


# Proveedores
suppliers = [
    ("TechReuse Iberia", "Alberto Ramos", "alberto.ramos@techreuse.example", "+34 900 111 222", "Polígono Norte 12, Valencia", "Pago a 30 días", "Proveedor principal de portátiles y monitores reacondicionados."),
    ("NetDistribuciones", "Sara Vidal", "sara.vidal@netdist.example", "+34 900 333 444", "Calle Red 5, Barcelona", "Pago a 15 días", "Descuento especial en routers por volumen."),
    ("HomeSecure Tech", "Nerea Costa", "nerea.costa@homesecure.example", "+34 900 555 666", "Avenida IoT 9, Madrid", "Pago a 30 días", "Proveedor de cámaras IP y dispositivos domóticos.")
]

cursor.executemany("""
INSERT INTO suppliers (name, contact_name, email, phone, address, payment_terms, internal_notes)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", suppliers)

# Notas internas sensibles ficticias
admin_notes = [
    ("Acceso temporal developer", "El usuario david.molina mantiene una contraseña temporal pendiente de cambio: Dev2026.", "laura.martin", "2026-04-11", 1),
    ("Ruta panel admin", "El panel de administración sigue disponible en /admin. Pendiente revisar permisos.", "david.molina", "2026-04-13", 1),
    ("Revisión de backups", "Comprobar que el backup diario no exponga credenciales de conexión a la base de datos.", "laura.martin", "2026-04-14", 1)
]

cursor.executemany("""
INSERT INTO admin_notes (title, content, created_by, created_at, confidential)
VALUES (?, ?, ?, ?, ?)
""", admin_notes)

connection.commit()
connection.close()

print("Base de datos ByteCat creada correctamente.")