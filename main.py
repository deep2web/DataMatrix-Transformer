import io
from flask import send_file
from PIL import Image
from pylibdmtx.pylibdmtx import decode

def main(request):
    # Behandlung von GET-Anfragen: Rückgabe des HTML-Upload-Formulars
    if request.method == 'GET':
        html = """
        <html>
          <head>
            <meta charset="utf-8">
            <title>Datei verarbeiten</title>
          </head>
          <body>
            <h1>Datei hochladen</h1>
            <form method="POST" enctype="multipart/form-data">
              <input type="file" name="file"><br><br>
              <button type="submit">Datei senden und verarbeiten</button>
            </form>
          </body>
        </html>
        """
        return html, 200

    # Behandlung von POST-Anfragen: Datei einlesen, verarbeiten und zurücksenden
    elif request.method == 'POST':
        if 'file' not in request.files:
            return 'Keine Datei hochgeladen', 400

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            return 'Keine Datei ausgewählt', 400

        # Dateiinhalt als Bytes einlesen
        file_content = uploaded_file.read()

        dm_texts = read_data_matrix_from_image(file_content)

        try:
            # Annahme: Die Datei ist eine UTF‑8–codierte Textdatei
            text = file_content.decode('utf-8')
        except UnicodeDecodeError:
            return 'Fehler beim Dekodieren der Datei. Bitte sicherstellen, dass es sich um eine UTF‑8 codierte Textdatei handelt.', 400

        # Beispielhafte Verarbeitung: Text in Großbuchstaben umwandeln
        processed_text = text.upper()
        processed_bytes = processed_text.encode('utf-8')

        # Bytes in einen in-memory Puffer packen
        buffer = io.BytesIO(processed_bytes)
        buffer.seek(0)

        # Rückgabe als Download mit angepasstem Dateinamen
        return send_file(
            buffer,
            as_attachment=True,
            download_name='processed_' + uploaded_file.filename,
            mimetype='application/octet-stream'
        )
    
    # Für alle anderen HTTP-Methoden wird ein Fehler zurückgegeben
    else:
        return 'Methode nicht erlaubt', 405

def read_data_matrix_from_image(file_content):
    image = Image.open(io.BytesIO(file_content))
    results = decode(image)
    return [r.data.decode('utf-8') for r in results] if results else []
