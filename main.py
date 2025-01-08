import unicodedata


class Asiento:
    def __init__(self, numero, fila):
        self.__numero = numero
        self.__fila = fila
        self.__reservado = False
        self.__precio = 0.0
        self.__descuentos_aplicados = []
        self.__dia_reserva = None  # Nuevo atributo para almacenar el día de la reserva

    # Getters
    def get_numero(self):
        return self.__numero

    def get_fila(self):
        return self.__fila

    def is_reservado(self):
        return self.__reservado

    def get_precio(self):
        return self.__precio

    def get_descuentos_aplicados(self):
        return self.__descuentos_aplicados

    def get_dia_reserva(self):
        return self.__dia_reserva

    # Métodos para operar
    def reservar(self, precio, descuentos, dia_reserva):
        if self.__reservado:
            raise Exception(f"El asiento {self.__fila}-{self.__numero} ya está reservado.")
        self.__reservado = True
        self.__precio = precio
        self.__descuentos_aplicados = descuentos
        self.__dia_reserva = dia_reserva  # Guardar el día de la reserva

    def cancelar_reserva(self):
        if not self.__reservado:
            raise Exception(f"El asiento {self.__fila}-{self.__numero} no está reservado.")
        self.__reservado = False
        self.__precio = 0.0
        self.__descuentos_aplicados = []
        self.__dia_reserva = None  # Limpiar el día de la reserva

    # Método especial para representar el asiento como texto
    def __str__(self):
        estado = "Reservado" if self.__reservado else "Disponible"
        texto = f"Asiento {self.__fila}-{self.__numero}: {estado}"
        if self.__reservado:
            texto += f", Precio: {self.__precio:.2f}€, Día de reserva: {self.__dia_reserva}"
            if self.__descuentos_aplicados:
                texto += "\n   Descuentos aplicados: " + ", ".join(self.__descuentos_aplicados)
        return texto


class SalaCine:
    def __init__(self, precio_base):
        self.__asientos = []
        self.__precio_base = precio_base

    # Getters
    def get_precio_base(self):
        return self.__precio_base

    # Agregar un asiento a la sala
    def agregar_asiento(self, numero, fila):
        if self.buscar_asiento(numero, fila):
            raise Exception(f"El asiento {fila}-{numero} ya está registrado.")
        nuevo_asiento = Asiento(numero, fila)
        self.__asientos.append(nuevo_asiento)

    # Buscar un asiento por número y fila
    def buscar_asiento(self, numero, fila):
        for asiento in self.__asientos:
            if asiento.get_numero() == numero and asiento.get_fila() == fila:
                return asiento
        return None

    # Calcular el precio final y los descuentos aplicados
    def calcular_precio(self, dia, edad):
        descuentos = []
        descuento_total = 0.0
        if dia == "miercoles":  # Normalizamos el texto antes
            descuentos.append("20% descuento día del espectador")
            descuento_total += 0.20
        if edad >= 65:
            descuentos.append("30% descuento para mayores de 65")
            descuento_total += 0.30
        precio_final = self.__precio_base * (1 - descuento_total)
        return precio_final, descuentos

    # Reservar un asiento
    def reservar_asiento(self, numero, fila, dia, edad):
        asiento = self.buscar_asiento(numero, fila)
        if not asiento:
            raise Exception(f"El asiento {fila}-{numero} no existe.")
        precio_final, descuentos = self.calcular_precio(dia, edad)
        asiento.reservar(precio_final, descuentos, dia)  # Agregar el día de la reserva
        return precio_final, descuentos, dia

    # Cancelar una reserva
    def cancelar_reserva(self, numero, fila):
        asiento = self.buscar_asiento(numero, fila)
        if not asiento:
            raise Exception(f"El asiento {fila}-{numero} no existe.")
        asiento.cancelar_reserva()

    # Mostrar el estado de los asientos
    def mostrar_asientos(self):
        print("\nEstado de los asientos:")
        for asiento in self.__asientos:
            print(asiento)


class CineApp:
    def __init__(self):
        self.sala = None

    def inicializar_sala(self, precio_base):
        self.sala = SalaCine(precio_base)
        filas = ["A", "B", "C"]
        for fila in filas:
            for numero in range(1, 6):  # 5 asientos por fila
                self.sala.agregar_asiento(numero, fila)

    def normalizar_texto(self, texto):
        texto = texto.lower()
        texto = unicodedata.normalize("NFD", texto).encode("ascii", "ignore").decode("utf-8")
        return texto

    def mostrar_menu(self):
        print("\nMenú:")
        print("1. Mostrar asientos")
        print("2. Reservar asiento")
        print("3. Cancelar reserva")
        print("4. Salir")

    def procesar_opcion(self, opcion):
        if opcion == "1":
            self.sala.mostrar_asientos()
        elif opcion == "2":
            try:
                fila = input("Ingresa la fila del asiento (ej. A, B): ").upper()
                numero = int(input("Ingresa el número del asiento: "))
                dia = input("Ingresa el día (ej. lunes, miércoles): ")
                dia = self.normalizar_texto(dia)  # Normalizamos el día ingresado
                edad = int(input("Ingresa la edad del espectador: "))
                precio_final, descuentos_aplicados, dia_reserva = self.sala.reservar_asiento(numero, fila, dia, edad)
                precio_sin_descuento = self.sala.get_precio_base()
                print("\n" + "*" * 40)
                print(f"Día de reserva: {dia_reserva}")
                print(f"Precio sin descuento: {precio_sin_descuento:.2f}€")
                if descuentos_aplicados:
                    print("Descuentos aplicados:")
                    for desc in descuentos_aplicados:
                        print(f"- {desc}")
                print(f"Precio final: {precio_final:.2f}€")
                print("*" * 40 + "\n")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "3":
            try:
                fila = input("Ingresa la fila del asiento (ej. A, B): ").upper()
                numero = int(input("Ingresa el número del asiento: "))
                self.sala.cancelar_reserva(numero, fila)
                print(f"Reserva del asiento {fila}-{numero} cancelada correctamente.")
            except Exception as e:
                print(f"Error: {e}")
        elif opcion == "4":
            print("Saliendo del sistema. ¡Hasta luego!")
            return False
        else:
            print("Opción inválida. Inténtalo de nuevo.")
        return True


def main():
    app = CineApp()
    app.inicializar_sala(precio_base=10.0)
    continuar = True
    while continuar:
        app.mostrar_menu()
        opcion = input("Selecciona una opción: ")
        continuar = app.procesar_opcion(opcion)


if __name__ == "__main__":
    main()
