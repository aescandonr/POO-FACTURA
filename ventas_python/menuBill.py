from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color,white_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Ingresar Cliente")
        print("\033[1;35m" + "Ingrese el DNI: ".ljust(21) + "\033[0m", end="")
        dni = validar.cedula("Error: Cedula Invalida", 30, 3)
        json_file = JsonFile(path+'/archivos/clients.json')
        exists = json_file.find("dni",dni)
        if exists:
            gotoxy(25,7);print(white_color + "Usuario ya existente")
            time.sleep(2)
            return
        print("\033[1;35m" + "Ingrese su Nombre: ".ljust(21) + "\033[0m", end="")
        nombre = validar.solo_letras("Error: Solo Letras",22,4).lower().capitalize()
        print("\033[1;35m" + "Ingrese su Apellido: ".ljust(21) + "\033[0m", end="")
        apellido= validar.solo_letras("Error: Solo Letras",23,5).lower().capitalize()
        print("\033[1;35m" + "Ingrese Valor de Descuento: ".ljust(21) + "\033[0m", end="")
        valo =validar.solo_decimales("Error: Solo Numeros",29,6)
        valor=float(valo)
        client = {"dni": dni,"nombre": nombre, "apellido": apellido,"valor": valor}
        if client['dni'] != "" and client['nombre'] != "" and client['apellido'] != "":
            gotoxy(1,8); print("\033[1;31m" + "Guardar al Cliente presione (s/n)".ljust(21) + "\033[0m", end="")
            valida= validar.solo_letras_client("Error: Solo 's' o 'n' ",36,8)
            if valida == "s":
                cli = json_file.read()
                clin = cli
                clin.append(client)
                json_file.save(clin)
                gotoxy(48,10);print("Cliente Agregado Con Exito")
                time.sleep(2)
            else:
                gotoxy(24,10);print("Datos eliminados")
                time.sleep(1)
        else:
            print("No se llenaron los datos")        
            time.sleep(1)
       
    def update(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2); print(yellow_color + "Actualizar Cliente")
        print("\033[1;35m" + "Ingrese dni del cliente a actualizar: ".ljust(21) + "\033[0m", end="")
        client_dni = validar.solo_numeros("Error: Solo Numeros",39,3)
        json_file = JsonFile(path+'/archivos/clients.json')
        dato = json_file.read()
        clients = json_file.find("dni", client_dni)
        
        if not clients:
            gotoxy(30,4);print(f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(2)
            return
        
        client_index = None
        
        for idx, client in enumerate(dato):
            if client["dni"] == client_dni:
                client_index = idx
                break
        
        if client_index is not None:
            client = dato[client_index]
            valor_actual_nombre=client["nombre"]
            valor_actual_apellido=client["apellido"]
            valor_actual_valor=client["valor"]
            gotoxy(15,5);print("Cliente")
            gotoxy(35,5);print("Apellido")
            gotoxy(55,5);print("Valor")
            gotoxy(15,6);print(f"{client['nombre']:}")
            gotoxy(35,6);print(f"{client['apellido']}")
            gotoxy(55,6);print(f"{client['valor']}")
            print("\033[1;33m" + "Ingrese el nuevo nombre (Deje vacío para mantener el mismo):".ljust(21) + "\033[0m", end="")
            new_nombre = validar.solo_letras_and_espacios("Error: Solo Letras",62,7,valor_actual_nombre).lower().capitalize()
            print("\033[1;33m" + "Ingrese el nuevo apellido (Deje vacío para mantener el mismo): ".ljust(21) + "\033[0m", end="")
            new_apellido = validar.solo_letras_and_espacios("Error: Solo Letras",64,8,valor_actual_apellido).lower().capitalize()
            print("\033[1;33m" + "Ingrese el nuevo valor de descuento (Deje vacío para mantener el mismo): ".ljust(21) + "\033[0m", end="")
            new_valor = validar.solo_decimales_and_espacios("Error: Solo Numeros",74,9,valor_actual_valor)
            
            client["nombre"] = new_nombre

            client["apellido"] = new_apellido
                
            client["valor"] = new_valor
            
            dato[client_index] = client
            json_file.save(dato)
            gotoxy(30,12);print("Cliente actualizado exitosamente")
            time.sleep(2)
        else:
            print(f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)
            
    def delete(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Eliminación de Cliente")
        print("\033[1;35m" + "Ingrese DNI del cliente a eliminar: ".ljust(21) + "\033[0m", end="")
        client_dni = validar.solo_numeros("Error: Solo Numeros",37,3)
        json_file = JsonFile(path+'/archivos/clients.json')
        dato=json_file.read()
        clients = json_file.find("dni",client_dni)
        for x in clients:
            if x["dni"] == client_dni:
                dato.remove(x)
                gotoxy(15,5);print("DNI")
                gotoxy(35,5);print("Cliente")
                gotoxy(55,5);print("Apellido")
                gotoxy(75,5);print("Valor")
                gotoxy(16,6);print(f"{x['dni']:}")
                gotoxy(36,6);print(f"{x['nombre']:}")
                gotoxy(56,6);print(f"{x['apellido']}")
                gotoxy(76,6);print(f"{x['valor']}")
                gotoxy(37,9);print(f"Cliente Eliminado")
                time.sleep(2)
                break
        else:
            print(f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)
        json_file.save(dato)
        
    def consult(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Consulta de Cliente")
        print("\033[1;35m" + "Ingrese el DNI que desea consultar: ".ljust(21) + "\033[0m", end="")
        gotoxy(2,4);client= validar.solo_numeros("Error: Solo Numeros",37,3)
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.find("dni",client)
        for dni in clients:
            if dni["dni"] == client:
                gotoxy(15,5);print("DNI")
                gotoxy(35,5);print("Cliente")
                gotoxy(55,5);print("Apellido")
                gotoxy(75,5);print("Valor")
                gotoxy(15,6);print(f"{dni['dni']:}")
                gotoxy(36,6);print(f"{dni['nombre']:}")
                gotoxy(56,6);print(f"{dni['apellido']}")
                gotoxy(76,6);print(f"{dni['valor']}")
                time.sleep(2)
                break
        else:
            print(f"No se encontró al cliente con el DNI: {client}")
            time.sleep(1)
        
class CrudProducts(ICrud):
    def create(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Crear Producto")
        print("\033[1;35m" + "Ingrese nombre del producto: ".ljust(21) + "\033[0m", end="")
        descripcion=validar.solo_letras("Error: Solo Letras",30,3).lower().capitalize()
        print("\033[1;35m" + "Ingrese Precio: ".ljust(21) + "\033[0m", end="")
        precio= validar.solo_decimales("Error: Solo Numeros",18,4)
        print("\033[1;35m" + "Ingrese Valor del Stock: ".ljust(21) + "\033[0m", end="")
        valo = validar.solo_decimales("Error: Solo Numeros",26,5)
        json_file = JsonFile(path+'/archivos/products.json')
        dato = json_file.read()
        ids = [producto["id"] for producto in dato if "id" in producto]
        ultimo_id = max(ids)
        Product.next = ultimo_id + 1
        nuevo_id = Product.next
        product ={"id": nuevo_id, "descripcion": descripcion, "precio": precio,"stock": valo}
        gotoxy(35,7);print("ID")
        gotoxy(55,7);print("Descripcion")
        gotoxy(75,7);print("Precio")
        gotoxy(95,7);print("Stock")
        gotoxy(35,8);print(f"{product['id']:}")
        gotoxy(56,8);print(f"{product['descripcion']:}")
        gotoxy(76,8);print(f"{product['precio']}")
        gotoxy(96,8);print(f"{product['stock']}")
        time.sleep(2)
        if product['descripcion'] != "" and product['precio'] != "" and product["stock"]:
            gotoxy(2,11);print("\033[1;31m" + "Guardar el Producto presione (s/n)".ljust(21) + "\033[0m", end="")
            gotoxy(2,11);valida= validar.solo_letras("Error: Solo Letras",37,11).lower()
            if valida == "s" or valida == "si":
                prod = json_file.read()
                produ = prod
                produ.append(product)
                json_file = JsonFile(path+'/archivos/products.json')
                json_file.save(produ)
                gotoxy(24,13)
                print("El producto se guardo exitosamente")
                time.sleep(2)
            else:
                gotoxy(24,13);print("Datos eliminados")
                time.sleep(1)
        else:
            print("No se llenaron los datos")        
            time.sleep(1)
    
    def update(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Actualizar Cliente")
        print("\033[1;35m" + "Ingrese id del Producto a actualizar: ".ljust(21) + "\033[0m", end="")
        producto_id = validar.solo_numeros("Error: Solo Numeros",40,3)
        producto_id = int(producto_id)
        json_file = JsonFile(path+'/archivos/products.json')
        dato = json_file.read()
        product = json_file.find("id", producto_id)
        
        if not product:
            gotoxy(30,5);print(f"No se encontró el producto con el ID: {producto_id}")
            time.sleep(2)
            return
        
        producto_index = None
        
        for idx, products in enumerate(dato):
            if products["id"] == producto_id:
                producto_index = idx
                break
        
        if producto_index is not None:
            products = dato[producto_index]
            gotoxy(15,5);print("ID")
            gotoxy(35,5);print("Descripcion")
            gotoxy(55,5);print("Precio")
            gotoxy(75,5);print("Stock")
            gotoxy(16,6);print(f"{products['id']:}")
            gotoxy(36,6);print(f"{products['descripcion']:}")
            gotoxy(56,6);print(f"{products['precio']}")
            gotoxy(76,6);print(f"{products['stock']}")
            time.sleep(2)
            valor_actual_nombre=products["descripcion"]
            valor_actual_precio=products["precio"]
            valor_actual_stock=products["stock"]
            
            print("\033[1;35m" + "Ingrese el nuevo nombre (Deje vacío para mantener el mismo): ".ljust(21) + "\033[0m", end="")
            new_nombre = validar.solo_letras_and_espacios("Error: Solo Letras",62,7,valor_actual_nombre).lower().capitalize()
            print("\033[1;35m" + "Ingrese el nuevo precio (Deje vacío para mantener el mismo): ".ljust(21) + "\033[0m", end="")
            new_precio = validar.solo_decimales_and_espacios("Error: Solo Numeros",62,8,valor_actual_precio)
            print("\033[1;35m" + "Ingrese el nuevo stock (Deje vacío para mantener el mismo): ".ljust(21) + "\033[0m", end="")
            new_stock = validar.solo_decimales_and_espacios("Error: Solo Numeros",61,9,valor_actual_stock)
            
            products["descripcion"] = new_nombre
            
            products["precio"] = new_precio
                
            products["stock"] = new_stock
            
            dato[producto_index] = products
            json_file.save(dato)
            gotoxy(37,11);print("Producto actualizado exitosamente.")
            time.sleep(2)
        else:
            print(f"No se encontró el producto con el ID: {producto_id}")
            time.sleep(1)
    
    def delete(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color +"Eliminar un Producto")
        print("\033[1;35m" + "Ingrese nombre del producto: ".ljust(21) + "\033[0m", end="")
        producto= validar.solo_letras("Error: Solo Letras",30,3).lower().capitalize()
        json_file = JsonFile(path+'/archivos/products.json')
        dato=json_file.read()
        products = json_file.find("descripcion",producto)
        
        if products:
            product = products[0]
            gotoxy(25, 6);print("ID:           Descripción:           Precio:           Stock:")
            gotoxy(25, 7);print(f" {product['id']:<13}{product['descripcion']:<23} ${product['precio']:<16} {product['stock']}")
            time.sleep(2)
            dato.remove(product)
            gotoxy(30, 9);print(f"Producto {product["descripcion"]} eliminado")
            time.sleep(2)
        else:
            gotoxy(30,5); print(f"No se encontró el producto con el nombre: {producto}")
            time.sleep(2)
        json_file.save(dato)
   
    def consult(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Consulta del Producto")
        print("\033[1;35m" + "Ingrese nombre del producto: ".ljust(21) + "\033[0m", end="")
        producto= validar.solo_letras("Error: Solo Letras",30,3).lower().capitalize()
        json_file = JsonFile(path+'/archivos/products.json')
        products = json_file.find("descripcion",producto)
        
        if products:
            product = products[0]
            gotoxy(15, 6);print("ID:           Descripción:           Precio:           Stock:")
            gotoxy(15, 7);print(f" {product['id']:<13} {product['descripcion']:<23} ${product['precio']:<16} {product['stock']}")
            time.sleep(3)
        else:
            gotoxy(30,5); print(f"No se encontro el producto: {producto}")
            time.sleep(2)

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Registro de Venta")
        gotoxy(17,3);print(yellow_color + Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print("Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line)
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print("Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = validar.solo_letras("Error: Solo Letras",53,11).lower()
        if procesar == "s" or procesar == "si":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print("🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)       
    
    def update(self):
        validar = Valida()
        sale = Sale
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Actualización de Factura")
        print("\033[1;35m" +"Ingrese el número de factura a actualizar: ".ljust(21) + "\033[0m", end="")
        invoice_number = validar.solo_numeros("Error: Solo Numeros",44,3)
        if invoice_number.isdigit():
            invoice_number = int(invoice_number)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            invoice_found = False
            for invoice in invoices:
                if invoice["factura"] == invoice_number:
                    invoice_found = True

                    print(f"Impresion de la Factura#{invoice_number}")
                    for key, value in invoice.items():
                        if key == 'detalle':
                            print(f"{key}:")
                            for i, detalle in enumerate(value, start=1):
                                print(f"Detalle {i}:")
                                for d_key, d_value in detalle.items():
                                    print(f"\t{d_key}: {d_value}")
                        else:
                            print(f"{key}: {value}")
                    time.sleep(5)
                    borrarPantalla()
                    print('\033c', end='')
                    gotoxy(2,1);print("█"+white_color+"█"*92)
                    gotoxy(38,2);print(yellow_color +"Actualización de Factura") 
                    print("¿Qué desea actualizar?")
                    print(white_color + "1. Fecha")
                    print(white_color + "2. Cliente")
                    print(white_color + "3. Subtotal")
                    print(white_color + "4. Descuento")
                    print(white_color + "5. Iva")
                    print(white_color + "6. Total")
                    print(white_color + "7. Detalle (Agregar/Actualizar/Eliminar)")
                    print(white_color + "8. Cancelar")
                    print("\033[1;31m" +'Seleccione una opcion:'.ljust(21) + "\033[0m", end="")
                    opcion = validar.solo_numeros("Error: Solo numeros",24, 12)
                    if opcion == '1':
                        nueva_fecha = input("Ingrese la nueva fecha (YYYY-MM-DD): ")
                        invoice["Fecha"] = nueva_fecha
                    elif opcion == '2':
                        print("\033[1;33m" + "Ingrese el nuevo cliente: ".ljust(21) + "\033[0m", end="")
                        nuevo_cliente = validar.solo_letras("Error: Solo letras",28,13).lower().capitalize()
                        invoice["cliente"] = nuevo_cliente
                    elif opcion == '3':
                        print("\033[1;33m" + "Ingrese el nuevo subtotal: ".ljust(21) + "\033[0m", end="")
                        nuevo_subtotal = validar.solo_decimales("Error: Solo numeros",28,13) 
                        invoice["subtotal"] = float(nuevo_subtotal)
                    elif opcion == '4':
                        print("\033[1;33m" + "Ingrese el nuevo descuento: ".ljust(21) + "\033[0m", end="")
                        nuevo_descuento = validar.solo_decimales("Error: Solo numeros",28,13) 
                        invoice["descuento"] = float(nuevo_descuento)
                    elif opcion == '5':
                        print("\033[1;33m" + "Ingrese el nuevo IVA: ".ljust(21) + "\033[0m", end="")
                        nuevo_iva = validar.solo_decimales("Error: Solo numeros",28,13) 
                        invoice["iva"] = float(nuevo_iva)
                    elif opcion == '6':
                        print("\033[1;33m" + "Ingrese el nuevo total: ".ljust(21) + "\033[0m", end="")
                        nuevo_total = validar.solo_decimales("Error: Solo numeros",28,13)
                        invoice["total"] = float(nuevo_total)
                    elif opcion == '7':
                        subopcion = input("¿Qué desea hacer en el detalle? ( 1)agregar / 2)actualizar / 3)eliminar): ")
                        borrarPantalla()
                        print('\033c', end='')
                        gotoxy(2,1);print("█"+white_color+"█"*92)
                        gotoxy(38,2);print(yellow_color +"Actualización de Factura") 
                        if subopcion == '1':
                            # Agregar nuevo producto al detalle
                            print("\033[1;33m" + "Ingrese el nombre del producto: ".ljust(21) + "\033[0m", end="")
                            producto_nuevo = validar.solo_letras("Error: Solo Letras",33,3).lower().capitalize()
                            print("\033[1;33m" + "Ingrese el precio del producto: ".ljust(21) + "\033[0m", end="")
                            precio_nuevo = validar.solo_decimales("Error: Solo Numeros",33,4)
                            print("\033[1;33m" + "Ingrese la cantidad del producto: ".ljust(21) + "\033[0m", end="")
                            cantidad_nueva = validar.solo_numeros("Error: Solo Numeros",35,5)
                            nuevo_detalle = {"poducto": producto_nuevo, "precio": precio_nuevo, "cantidad": cantidad_nueva}
                            invoice["detalle"].append(nuevo_detalle)
                            print(invoice["detalle"])
                            subtotal, discount, iva, total = sale.cal(invoice["detalle"])
                            invoice["subtotal"] = round(subtotal, 2)
                            invoice["descuento"] = round(discount, 2)
                            invoice["iva"] = round(iva, 2)
                            invoice["total"] = round(total, 2)
                            print("Producto agregado al detalle.")
                            json_file.save(invoices)
                            break
                        elif subopcion == '2':
                            # Mostrar detalle actual y permitir actualizar precio o cantidad
                            print("\033[1;33m" + 'Qué producto quiere actualizar (Ingrese el nombre): '.ljust(21) + "\033[0m", end="")
                            subopcion_update = validar.solo_letras("Error: Solo Letras",54,3).lower().capitalize()
                            invoice["detalle"]
                            for product in invoice["detalle"]:
                                if product["poducto"] == subopcion_update:
                                    gotoxy(2,4);print("\033[1;33m" + 'ok, ingresa los nuevos datos:\n'.ljust(21) + "\033[0m", end="")
                                    gotoxy(2,5);print("\033[1;33m" + 'Ingresa el nuevo nombre:'.ljust(21) + "\033[0m", end="")
                                    product["poducto"] = validar.solo_letras("Error: Solo Numeros",26,5).lower().capitalize()
                                    gotoxy(2,6);print("\033[1;33m" + 'Ingresa el nuevo precio:'.ljust(21) + "\033[0m", end="")
                                    product["precio"] = validar.solo_decimales("Error: Solo Numeros",26,6)
                                    gotoxy(2,7);print("\033[1;33m" + 'Ingresa la nuevo cantidad:'.ljust(21) + "\033[0m", end="")
                                    product["cantidad"] = validar.solo_numeros("Error: Solo Numeros",29,7)
                                    subtotal, discount, iva, total = sale.cal(invoice["detalle"])
                                    invoice["subtotal"] = round(subtotal, 2)
                                    invoice["descuento"] = round(discount, 2)
                                    invoice["iva"] = round(iva, 2)
                                    invoice["total"] = round(total, 2)
                                    json_file.save(invoices)
                                    break
                            
                        elif subopcion == '3':
                            # Mostrar detalle actual y permitir eliminar un producto
                            print("\033[1;33m" + 'Qué producto quiere eliminar (Ingrese el nombre): '.ljust(21) + "\033[0m", end="")
                            subopcion_update = validar.solo_letras("Error: Solo letras",51,2).lower().capitalize()
                            for i, product in enumerate(invoice["detalle"]):
                                if product["poducto"] == subopcion_update:
                                    del invoice["detalle"][i]
                                    subtotal, discount, iva, total = sale.cal(invoice["detalle"])
                                    invoice["subtotal"] = round(subtotal, 2)
                                    invoice["descuento"] = round(discount, 2)
                                    invoice["iva"] = round(iva, 2)
                                    invoice["total"] = round(total, 2)
                                    print("Producto eliminado.")
                                    json_file.save(invoices)
                                    break
                            else:
                                print("Producto no encontrado.")
                                break
                        else:
                            print("Opción no válida.")
                            break
                    elif opcion == '8':
                        print("Operación de actualización cancelada.")
                        break
                    else:
                        print("Opción no válida.")
                        break
                    
                    json_file.save(invoices)
                    print("Factura actualizada exitosamente.")
                    break

            if not invoice_found:
                print(f"No se encontró la factura con el número {invoice_number}.")
        else:
            print("Por favor, ingrese un número de factura válido.")

        input("Presione una tecla para continuar...")
        
    def delete(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Eliminación de Factura")
        gotoxy(2,3);print("\033[1;35m" + "Ingrese el número de factura a eliminar: ".ljust(21) + "\033[0m", end="")
        gotoxy(2,4);invoice_number = validar.solo_numeros("Error: Solo Numeros",44,3)
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Eliminación de Factura")
        if invoice_number.isdigit():
            invoice_number = int(invoice_number)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            invoice_found = False
            for invoice in invoices:
                if invoice["factura"] == invoice_number:
                    invoice_found = True
                    gotoxy(30,4);print(f"Impresion de la Factura#{invoice_number}")
                    line=0
                    for key, value in invoice.items():
                        if key == 'detalle':
                            gotoxy(75,2);print(f"{key}:")
                            for x in value:
                                gotoxy(50,3);print(x)
                        else:
                            gotoxy(20,6+line);print(f"{key}: {value}")
                            line+=1
                    gotoxy(2,15);print("\033[1;31m" + "¿Seguro que deseas eliminar esta factura (si/no)?: ".ljust(21) + "\033[0m", end="")
                    confirmacion = validar.solo_letras("Error: Solo Letras",54,15).lower()
                    if confirmacion == 'si' or confirmacion == "s":
                        invoices.remove(invoice)
                        json_file.save(invoices)
                        print("Factura eliminada exitosamente.")
                    else:
                        gotoxy(45,17);print("Operación de eliminación cancelada.")
                        time.sleep(1)
                    break

            if not invoice_found:
                print(f"No se encontró la factura con el número {invoice_number}.")
        else:
            print("Por favor, ingrese un número de factura válido.")

        input("Presione una tecla para continuar...")
    
    def consult(self):
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print("█"+white_color+"█"*92)
        gotoxy(38,2);print(yellow_color + "Consulta de Venta")
        gotoxy(2,3);print("INGRESE EL NUMERO DE FACTURA O PRESIONE 'n' PARA CONSULTAR EL BANCO DE FACTURAS:",end="")
        gotoxy(2,3);invoice = validar.letra_y_numero("Error: ingrese de nuevo" ,82,3)
        if invoice is not None:
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.find("factura", invoice)
            if invoices:
                gotoxy(1, 5); print("-" * 109)
                gotoxy(38, 5); print(yellow_color + f"Impresion de la Factura # {invoice}")
                factura_info = invoices[0]
                gotoxy(2, 7); print(purple_color + "Factura")
                gotoxy(15, 7); print(purple_color + "Fecha")
                gotoxy(30, 7); print(purple_color + "Cliente")
                gotoxy(45, 7); print(purple_color + "Subtotal")
                gotoxy(60, 7); print(purple_color + "Descuento")
                gotoxy(75, 7); print(purple_color + "IVA")
                gotoxy(90, 7); print(purple_color + "Total")
                gotoxy(5, 8); print(white_color + f"{factura_info['factura']}")
                gotoxy(13, 8); print(white_color + f"{factura_info['Fecha']}")
                gotoxy(28, 8); print(white_color + f"{factura_info['cliente']}")
                gotoxy(46, 8); print(white_color + f"{factura_info['subtotal']}")
                gotoxy(62, 8); print(white_color + f"{factura_info['descuento']}")
                gotoxy(75, 8); print(white_color + f"{factura_info['iva']}")
                gotoxy(90, 8); print(white_color + f"{factura_info['total']}")
                gotoxy(1, 10); print("-" * 109)
                gotoxy(38, 10); print(yellow_color + f"Impresion de los detalles")
                detalles = factura_info['detalle']
                linea_x = 2
                linea_y = 12
                for idx, detalle in enumerate(detalles, 1):
                    gotoxy(linea_x, linea_y)
                    print(yellow_color + f"Detalle {idx}:")
                    gotoxy(linea_x, linea_y + 1)
                    print(white_color + f"Producto: {detalle['poducto']}")
                    gotoxy(linea_x, linea_y + 2)
                    print(white_color + f"Precio: {detalle['precio']}")
                    gotoxy(linea_x, linea_y +3)
                    print(white_color + f"Cantidad: {detalle['cantidad']}")
                    linea_x += 25
                gotoxy(1, 17); print("-" * 109)
                gotoxy(2, 40); print(purple_color + "Presione 's' para salir...")
                while True:
                    key = input()
                    if key.lower() == 's':
                        break
            else:
                print(white_color + "Factura no encontrada. Presione 's' para salir...")
                while True:
                    key = input()
                    if key.lower() == 's':
                        break
        else:
            json_file = JsonFile(path + '/archivos/invoices.json')
            invoices = json_file.read()
            gotoxy(1, 4); print("-" * 109)
            gotoxy(38, 4); print(yellow_color + f"BANCO DE FACTURAS")
            gotoxy(2, 5); print(purple_color + "Factura")
            gotoxy(17, 5); print(purple_color + "Fecha")
            gotoxy(32, 5); print(purple_color + "Cliente")
            gotoxy(45, 5); print(purple_color + "Subtotal")
            gotoxy(60, 5); print(purple_color + "Descuento")
            gotoxy(75, 5); print(purple_color + "IVA")
            gotoxy(90, 5); print(purple_color + "Total")
            for i, fac in enumerate(invoices, start=6):
                gotoxy(2, i)
                print(white_color + f"{fac['factura']}")
                gotoxy(15, i)
                print(white_color + f"{fac['Fecha']}")
                gotoxy(30, i)
                print(white_color + f"{fac['cliente']}")
                gotoxy(45, i)
                print(white_color + f"{fac['subtotal']}")
                gotoxy(60, i)
                print(white_color + f"{fac['descuento']}")
                gotoxy(75, i)
                print(white_color + f"{fac['iva']}")
                gotoxy(90, i)
                print(white_color + f"{fac['total']}")
            gotoxy(1, 15); print("-" * 109)
            gotoxy(38, 15); print(yellow_color + f"INFORMACION ADICIONAL")
            gotoxy(1,16); print(purple_color +f"FILTER CLIENTE"  )
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))
            gotoxy(2, 17); print(purple_color + "Factura")
            gotoxy(17, 17); print(purple_color + "Fecha")
            gotoxy(32, 17); print(purple_color + "Cliente")
            gotoxy(45, 17); print(purple_color + "Subtotal")
            gotoxy(60, 17); print(purple_color + "Descuento")
            gotoxy(75, 17); print(purple_color + "IVA")
            gotoxy(90, 17); print(purple_color + "Total")
            linea_actual = 18  # Empieza en la siguiente línea después de las etiquetas
            for facturafilter in total_client:
                gotoxy(2, linea_actual); print(white_color + f"{facturafilter["factura"]}")
                gotoxy(17, linea_actual); print(white_color +f"{facturafilter["Fecha"]}")
                gotoxy(32, linea_actual); print(white_color +f"{facturafilter["cliente"]}")
                gotoxy(45, linea_actual); print(white_color +f"{facturafilter["subtotal"]}")
                gotoxy(60, linea_actual); print(white_color +f"{facturafilter["descuento"]}")
                gotoxy(75, linea_actual); print(white_color +f"{facturafilter["iva"]}")
                gotoxy(90, linea_actual); print(white_color +f"{facturafilter["total"]}")
                linea_actual += 1
            gotoxy(1, 25); print("-" * 109)
            
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            sumared = reduce(lambda total, invoice: round(total+ invoice["total"],2),invoices,0)
            gotoxy(38, 26); print(yellow_color + f"TOTAL DE CADA FACTURA")
            gotoxy(46, 27); print(purple_color + "Total")
            linea_actual = 28 
            for total in totales_map:
                gotoxy(46, linea_actual); print(white_color + f"{total}")  
                linea_actual += 1 
            gotoxy(36, 26); print(yellow_color + f"MONTO TOTAL DE LAS FACTURAS")
            gotoxy(46,28); print(white_color + f"{sumared}")
            gotoxy(1, 32); print("-" * 109)
            max_invoice = max(totales_map)
            gotoxy(36, 26); print(yellow_color + f"MAXIMO GASTO DE UNA FACTURA")
            gotoxy(46,28); print(white_color + f"{max_invoice}")
            gotoxy(1, 32); print("-" * 109)
            min_invoice = min(totales_map)
            gotoxy(36, 26); print(yellow_color + f"MINIMO GASTO DE UNA FACTURA")
            gotoxy(46,28); print(white_color + f"{min_invoice}")
            gotoxy(1, 32); print("-" * 109)
            # tot_invoices = sum(totales_map)
            # print("filter cliente: ",total_client)
            # print(f"map Facturas:{totales_map}")
            # print(f"              max Factura:{max_invoice}")
            # print(f"              min Factura:{min_invoice}")
            # print(f"              sum Factura:{tot_invoices}")
            # print(f"              reduce Facturas:{suma}")
            x=input("presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("***MENU PRINCIPAL***",["CLIENTE","PRODUCTO","VENTA","SALIR"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()  
            clients = CrudClients()
            menu_clients = Menu("MENU CLIENTES",["INGRESAR","ACTUALIZAR","ELIMINAR","CONSULTAR","SALIR"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                clients.create()
            elif opc1 == "2":
                clients.update()
            elif opc1 == "3":
                clients.delete()
            elif opc1 == "4":
                clients.consult()
                time.sleep(2)
            elif opc1 == "5":
                print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            products = CrudProducts()
            menu_products = Menu("MENU PRODUCTOS",["INGRESAR","ACTUALIZAR","ELIMINAR","CONSULTAR","SALIR"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                products.create()
            elif opc2 == "2":
                products.update()
            elif opc2 == "3":
                products.delete()
            elif opc2 == "4":
                products.consult()
            elif opc2 == "5":
                print("Regresando al menu Productos...")
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("MENU VENTAS",["INGRESAR","ACTUALIZAR","ELIMINAR","CONSULTAR","SALIR"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.update()
                time.sleep(2)
                
            elif opc3 == "3":
                sales.delete()
                time.sleep(2)
                
            elif opc3 == "4":
                sales.consult()
                time.sleep(2)
                
            elif opc3 == "5":
                print("Regresando al menu Ventas...")
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

