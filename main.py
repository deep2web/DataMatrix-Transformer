import treepoem
# Erzeugen eines rechteckigen DataMatrix-Codes
barcode = treepoem.generate_barcode(
    barcode_type='datamatrix',
    data=bytes.fromhex("444541850000000042A004CD8E35003338250B1252F2534633A2C54EA23ABCDB5CF04EF969C98F100000"),
    options={
        'format': 'rectangle',  # Erzwingt ein rechteckiges Format
        'columns': 48,         # Anzahl der Spalten (Breite)
        'rows': 16             # Anzahl der Zeilen (Höhe)
    }
)

# Speichern des Barcodes als PNG-Datei
barcode.save('datamatrix_16x48.png')
