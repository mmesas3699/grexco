import pyexcel as pe


def index_columnas(cantidad_columas):
    n = 0
    while n < cantidad_columas:
        yield n
        n = n + 1


def verifica_formato_excel(archivo, formato):
    """
    Verifica que el archivo contenga todos los datos m
    Recibe como parametros:
        archivo = str('ruta/del/archivo/archico.xlsx')
        formato = (el formato del archivo. Una tupla de tuplas donde
                   cada tupla corresponde a una columna).

                Ej:
                formato = (
                    (Clase,   # La clase que deberia tener el dato (str, int)
                    True,    # True si es obligatorio si no False
                    Largo)   # Opcional. Solo si la Clase es 'str'.
                )

    Retorna un Lista de errados, si la Lista esta vacía es porque no hay
    ninguna fila errada
    """
    archivo = pe.get_sheet(file_name=archivo, start_row=1)
    formato = formato
    cantidad_columnas_formato = len(formato)
    cantidad_columnas_archivo = archivo.number_of_columns()

    # Si la cantidad de columnas en el archivo no es igual al número de
    # columnas en el formato retorna un mensaje de error
    if not cantidad_columnas_archivo == cantidad_columnas_formato:
        return {'error': 'La cantidad de columnas en el archivo no es igual a la del formato'}

    excel = archivo.array
    # errados = []
    for fila in excel:
        columna = 0
        for celda in fila:
            print('celda', celda)
            if formato[columna][0] == str:
                if isinstance(celda, str):
                    if len(celda) == 0 and formato[columna][1] is True:
                        fila.append(
                        'El valor de la columna {} no debe estar vacio'.format(columna))
                    else:
                        pass
                else:
                    fila.append(
                        'Los datos de la columna {} deben ser de tipo texto'.format(columna))
            elif formato[columna][0] == int:
                if isinstance(celda, int):
                    pass
                else:
                    fila.append('Los datos de la columna {} deben ser Numericos'.format(columna))

            if columna >= (cantidad_columnas_archivo - 1):
                pass
            else:
                columna += 1

    print(excel)
