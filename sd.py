from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
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
        print('\033c', end='')
        gotoxy(2,1);print("█"+green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        gotoxy(2,4);dni= input("Ingrese dni: ")
        borrarPantalla()
        gotoxy(2,4);nombre= input("Ingrese Nombre: ")
        borrarPantalla()
        gotoxy(2,4);apellido= input("Ingrese Apellidos: ")
        borrarPantalla()
        gotoxy(2,4);valo =input("Ingrese Valor de Descuento: ")
        while not valo.strip():
            print("El valor de descuento no puede estar vacío.")
            time.sleep(1.5)
            borrarPantalla()
            gotoxy(2,4);valo =input("Ingrese Valor de Descuento: ")
        valor=float(valo)
        client = {"dni": dni,"nombre": nombre, "apellido": apellido,"valor": valor}
        if client['dni'] != "" and client['nombre'] != "" and client['apellido'] != "":
            gotoxy(2,4);valida= input("Guardar al Cliente presione (s/n)")
            if valida == "s":
                json_file = JsonFile(path+'/archivos/clients.json')
                cli = json_file.read()
                clin = cli
                clin.append(client)
                json_file = JsonFile(path+'/archivos/clients.json')
                json_file.save(clin)
            else:
                gotoxy(24,9);print("Accion Elimina")
                time.sleep(1)
        else:
            print("No se llenaron los datos")        
            time.sleep(1)
       
    def update(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualizar Cliente"+" "*35+"██")
        gotoxy(2,4);client_dni = input("Ingrese dni del cliente a actualizar: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        dato = json_file.read()
        clients = json_file.find("dni", client_dni)
        
        if not clients:
            print(f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)
            return
        
        client_index = None
        
        for idx, client in enumerate(dato):
            if client["dni"] == client_dni:
                client_index = idx
                break
        
        if client_index is not None:
            client = dato[client_index]
            print(f"Cliente {client['nombre']} {client['apellido']} encontrado")
            time.sleep(1)
            new_nombre = input("Ingrese el nuevo nombre (Deje vacío para mantener el mismo): ")
            new_apellido = input("Ingrese el nuevo apellido (Deje vacío para mantener el mismo): ")
            new_valor = input("Ingrese el nuevo valor de descuento (Deje vacío para mantener el mismo): ")
            
            if new_nombre.strip():
                client["nombre"] = new_nombre
            
            if new_apellido.strip():
                client["apellido"] = new_apellido
                
            if new_valor.strip():
                client["valor"] = float(new_valor)
            
            dato[client_index] = client
            json_file.save(dato)
            print("Cliente actualizado exitosamente.")
            time.sleep(2)
        else:
            print(f"No se encontró al cliente con el DNI: {client_dni}")
            time.sleep(1)
            
    def delete(self):
        print('\033c', end='')
        gotoxy(2, 1); print("█" + green_color + "█" * 90)
        gotoxy(2, 2); print("██" + " " * 34 + "Eliminación de Cliente" + " " * 34 + "██")
        gotoxy(2, 4); client_dni = input("Ingrese DNI del cliente a eliminar: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        dato=json_file.read()
        clients = json_file.find("dni",client_dni)
        print(clients)
        time.sleep(2)
        for x in clients:
            if x["dni"] == client_dni:
                dato.remove(x)
                print(f"Cliente {x['nombre']} {x['apellido']} eliminado")
                time.sleep(1)
                break
        else:
            print(f"No se encontró al cliente con el DNI: {client_dni}")
        json_file.save(dato)
        
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        gotoxy(2,4);client= input("Ingrese dni: ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.find("dni",client)
        for dni in clients:
            if dni["dni"] == client:
                print(f"Cliente {dni['nombre']} {dni['apellido']} encontrado")
                time.sleep(1)
                break
        else:
            print(f"No se encontró al cliente con el DNI: {client}")
            time.sleep(1)
        
class CrudProducts(ICrud):
    def create(self):
        print('\033c', end='')
        gotoxy(2,1);print("█"+green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Crear Producto"+" "*35+"██")
        gotoxy(2,4);descripcion= input("Ingrese nombre del producto: ")
        
        gotoxy(2,5);precio= input("Ingrese Precio: ")
        while not precio.strip():
            print("El valor del Precio no puede estar vacío.")
            time.sleep(1.5)
            borrarPantalla()
            gotoxy(2,3);precio =input("Ingrese Valor del Precio: ")
        precios=float(precio)
        
        gotoxy(2,6);valo =input("Ingrese Valor del Stock: ")
        while not valo.strip():
            print("El valor del Stock no puede estar vacío.")
            time.sleep(1.5)
            borrarPantalla()
            gotoxy(2,3);valo =input("Ingrese Valor del Stock: ")
        valor=float(valo)
        borrarPantalla()
        
        # FALTA AGREGAR ID
        product = {"descripcion": descripcion, "precio": precios,"stock": valor}
        if product['descripcion'] != "" and product['precio'] != "" and product["stock"]:
            gotoxy(2,4);valida= input("Guardar el Producto presione (s/n)")
            if valida == "s":
                json_file = JsonFile(path+'/archivos/products.json')
                prod = json_file.read()
                produ = prod
                produ.append(product)
                json_file = JsonFile(path+'/archivos/products.json')
                json_file.save(produ)
            else:
                gotoxy(24,9);print("Accion Elimina")
                time.sleep(1)
        else:
            print("No se llenaron los datos")        
            time.sleep(1)
    
    def update(self):
        pass
    
    def delete(self):
       pass
   
    def consult(self):
        pass

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(blue_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
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
            gotoxy(15,9+line);
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
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
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
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Actualización de Factura"+" "*35+"██")
        gotoxy(2,4);invoice_number = input("Ingrese el número de factura a actualizar: ")
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
                                print(f"Producto {i}:")
                                for d_key, d_value in detalle.items():
                                    print(f"\t{d_key}: {d_value}")
                        else:
                            print(f"{key}: {value}")
                    print("\n¿Qué desea actualizar?")
                    print("1. Fecha")
                    print("2. Cliente")
                    print("3. Subtotal")
                    print("4. Descuento")
                    print("5. Iva")
                    print("6. Total")
                    print("7. Detalle (Agregar/Actualizar/Eliminar)")
                    print("8. Cancelar")
                    print('Seleccione una opcion:')
                    opcion = validar.solo_numeros("Error: Solo numeros", 23, 24)


                    if opcion == '1':
                        nueva_fecha = input("Ingrese la nueva fecha (YYYY-MM-DD): ")
                        invoice["Fecha"] = nueva_fecha
                    elif opcion == '2':
                        print("Ingrese el nuevo cliente: ")
                        nuevo_cliente = validar.solo_letras("Error: Solo letras") 
                        invoice["cliente"] = nuevo_cliente
                    elif opcion == '3':
                        print("Ingrese el nuevo subtotal: ")
                        nuevo_subtotal = validar.solo_decimales("Error: Solo numeros") 
                        invoice["subtotal"] = float(nuevo_subtotal)
                    elif opcion == '4':
                        print("Ingrese el nuevo descuento: ")
                        nuevo_descuento = validar.solo_decimales("Error: Solo numeros") 
                        invoice["descuento"] = float(nuevo_descuento)
                    elif opcion == '5':
                        print("Ingrese el nuevo IVA: ")
                        nuevo_iva = validar.solo_decimales("Error: Solo numeros") 
                        invoice["iva"] = float(nuevo_iva)
                    elif opcion == '6':
                        print("Ingrese el nuevo total: ")
                        nuevo_total = validar.solo_decimales("Error: Solo numeros")
                        invoice["total"] = float(nuevo_total)
                    elif opcion == '7':
                        subopcion = input("¿Qué desea hacer en el detalle? ( 1)agregar / 2)actualizar / 3)eliminar): ")
                        if subopcion == '1':
                            # Agregar nuevo producto al detalle
                            producto_nuevo = input("Ingrese el nombre del producto: ")
                            precio_nuevo = float(input("Ingrese el precio del producto: "))
                            cantidad_nueva = int(input("Ingrese la cantidad del producto: "))
                            nuevo_detalle = {"poducto": producto_nuevo, "precio": precio_nuevo, "cantidad": cantidad_nueva}
                            invoice["detalle"].append(nuevo_detalle)
                            # print(invoice["detalle"])
                            # print(nuevo_detalle)
                            print(invoice["detalle"])
                            subtotal, discount, iva, total = sale.cal(invoice["detalle"])
                            invoice["subtotal"] = round(subtotal, 2)
                            invoice["descuento"] = round(discount, 2)
                            invoice["iva"] = round(iva, 2)
                            invoice["total"] = round(total, 2)
                            # invoice["subtotal"] = 6
                            # print(invoice["subtotal"])
                            print("Producto agregado al detalle.")
                        elif subopcion == '2':
                            # Mostrar detalle actual y permitir actualizar precio o cantidad
                            subopcion_update = input('Qué producto quiere actualizar (Ingrese el nombre): ').lower()
                            invoice["detalle"]
                            for product in invoice["detalle"]:
                                if product["poducto"].lower() == subopcion_update:
                                    print('ok, ingresa los nuevos datos:\n')
                                    product["poducto"] = input('Ingresa el nuevo nombre:')
                                    product["precio"] = float(input('Ingresa el nuevo precio:'))
                                    product["cantidad"] = int(input('Ingresa la nuevo cantidad:'))
                                    subtotal, discount, iva, total = sale.cal(invoice["detalle"])
                                    invoice["subtotal"] = round(subtotal, 2)
                                    invoice["descuento"] = round(discount, 2)
                                    invoice["iva"] = round(iva, 2)
                                    invoice["total"] = round(total, 2)
                                
                        elif subopcion == '3':
                            # Mostrar detalle actual y permitir eliminar un producto
                            subopcion_update = input('Qué producto quiere eliminar (Ingrese el nombre): ').lower()
                            for i, product in enumerate(invoice["detalle"]):
                                if product["poducto"].lower() == subopcion_update:
                                    del invoice["detalle"][i]
                                    subtotal, discount, iva, total = sale.cal(invoice["detalle"])
                                    invoice["subtotal"] = round(subtotal, 2)
                                    invoice["descuento"] = round(discount, 2)
                                    invoice["iva"] = round(iva, 2)
                                    invoice["total"] = round(total, 2)
                                    print("Producto eliminado.")
                                    break
                            else:
                                print("Producto no encontrado.")
                        else:
                            print("Opción no válida.")
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
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Eliminación de Factura"+" "*35+"██")
        gotoxy(2,4);invoice_number = input("Ingrese el número de factura a eliminar: ")
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
                            for x in value:
                                print(x)
                        else:
                            print(f"{key}: {value}")
                    confirmacion = input("¿Seguro que deseas eliminar esta factura (si/no)?: ").lower()
                    if confirmacion == 'si':
                        invoices.remove(invoice)
                        json_file.save(invoices)
                        print("Factura eliminada exitosamente.")
                    else:
                        print("Operación de eliminación cancelada.")
                    break

            if not invoice_found:
                print(f"No se encontró la factura con el número {invoice_number}.")
        else:
            print("Por favor, ingrese un número de factura válido.")

        input("Presione una tecla para continuar...")
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu("Menu Facturacion",["1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()  
            clients = CrudClients()
            menu_clients = Menu("Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
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
            menu_products = Menu("Menu Productos",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                products.create()
            elif opc2 == "2":
                pass
            elif opc2 == "3":
                pass
            elif opc2 == "4":
                pass
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu("Menu Ventas",["1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()
                
            elif opc3 == "2":
                sales.consult()
                time.sleep(2)
                
            elif opc3 == "3":
                sales.update()
                time.sleep(2)
                
            elif opc3 == "4":
                sales.delete()
                time.sleep(2)
                
            elif opc3 == "5":
                print("Regresando al menu Clientes...")
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

