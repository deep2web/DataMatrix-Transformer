from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import os
import tempfile
import io
import magic

from PIL import Image
from pylibdmtx.pylibdmtx import decode as dmtx_decode
import treepoem

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def get_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="de">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DataMatrix Transformer</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            margin: 0;
            padding: 0;
          }
          .container {
            max-width: 600px;
            margin: 50px auto;
            background-color: #fff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
          }
          h1 {
            text-align: center;
            color: #333;
          }
          form {
            display: flex;
            flex-direction: column;
            gap: 15px;
          }
          input[type="file"] {
            padding: 10px;
          }
          button {
            padding: 10px;
            border: none;
            background-color: #007BFF;
            color: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
          }
          button:hover {
            background-color: #0056b3;
          }
          label {
            font-weight: bold;
            color: #555;
          }
        </style>
      </head>
      <body>
        <div class="container">
          <h1>DataMatrix Transformer</h1>
          <form id="uploadForm" action="/uploadbarcode" method="post" enctype="multipart/form-data">
            <label for="file">Wähle ein Bild mit einem DataMatrix-Code (PNG, JPG, etc.):</label>
            <input type="file" id="file" name="file" required>
            <button type="submit">Hochladen und verarbeiten</button>
          </form>
        </div>
      </body>
    </html>
    """
    return html_content


@app.post("/uploadbarcode")
async def upload_barcode(file: UploadFile = File(...)):
    file_bytes = await file.read()  # Datei in Bytes laden

    # Prüfe, ob es sich um eine Bilddatei handelt
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Es können nur Bilddateien verarbeitet werden.")

    # Prüfe die Dateierweiterung
    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    if not any(file.filename.lower().endswith(ext) for ext in valid_extensions):
        raise HTTPException(status_code=400, detail="Ungültige Dateierweiterung. Erlaubt sind: .png, .jpg, .jpeg, .bmp, .gif")

    # Serverseitige Überprüfung des MIME-Typs mittels python-magic
    server_mime = magic.from_buffer(file_bytes, mime=True)
    if not server_mime.startswith("image/"):
        raise HTTPException(status_code=400, detail="Die Datei entspricht nicht dem erwarteten Bildformat.")

    # Öffne die Datei mit Pillow
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # pylibdmtx erwartet ein RGB-Bild
        image = image.convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Das hochgeladene Bild konnte nicht geöffnet werden.")

    # Verwenden von pylibdmtx zum Auslesen von DataMatrix-Codes
    decoded_codes = dmtx_decode(image)
    if not decoded_codes:
        raise HTTPException(status_code=400, detail="Kein DataMatrix-Code im Bild gefunden.")

    # Verwende den ersten gefundenen DataMatrix-Code
    barcode_data = decoded_codes[0].data

    try:
        # Erzeuge mit treepoem einen neuen DataMatrix-Code im rechteckigen Format
        dt_barcode = treepoem.generate_barcode(
            barcode_type='datamatrix',
            data=barcode_data,
            options={
                'format': 'rectangle',  # Erzwingt ein rechteckiges Format
                'columns': 48,          # Anzahl der Spalten (Breite)
            }
        )
        # Weitere Verarbeitung ...
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Rückgabe oder weitere Verarbeitung
    # Prüfe, ob es sich um eine Bilddatei handelt
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Es können nur Bilddateien verarbeitet werden.")
    
    # Prüfe die Dateierweiterung
    valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    if not any(file.filename.lower().endswith(ext) for ext in valid_extensions):
        raise HTTPException(status_code=400, detail="Ungültige Dateierweiterung. Erlaubt sind: .png, .jpg, .jpeg, .bmp, .gif")
    
    # Serverseitige Überprüfung des MIME-Typs mittels python-magic
    server_mime = magic.from_buffer(file_bytes, mime=True)
    if not server_mime.startswith("image/"):
        raise HTTPException(status_code=400, detail="Die Datei entspricht nicht dem erwarteten Bildformat.")
    
    # Öffne die Datei mit Pillow
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # pylibdmtx erwartet ein RGB-Bild
        image = image.convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Das hochgeladene Bild konnte nicht geöffnet werden.")
    
    # Verwenden von pylibdmtx zum Auslesen von DataMatrix-Codes
    decoded_codes = dmtx_decode(image)
    if not decoded_codes:
        raise HTTPException(status_code=400, detail="Kein DataMatrix-Code im Bild gefunden.")
    
    # Verwende den ersten gefundenen DataMatrix-Code
    barcode_data = decoded_codes[0].data

    try:
        # Erzeuge mit treepoem einen neuen DataMatrix-Code im rechteckigen Format
        dt_barcode = treepoem.generate_barcode(
            barcode_type='datamatrix',
            data=barcode_data,
            options={
                'format': 'rectangle',  # Erzwingt ein rechteckiges Format
                'columns': 48,          # Anzahl der Spalten (Breite)
                'rows': 16              # Anzahl der Zeilen (Höhe)
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fehler bei der Barcode-Erstellung: {e}")
    
    # Speichere das generierte Bild als PNG im temporären Verzeichnis
    temp_dir = tempfile.gettempdir()
    output_filename = os.path.join(temp_dir, f"datamatrix_{file.filename}.png")
    dt_barcode.convert("1").save(output_filename)
    
    return FileResponse(
        output_filename,
        media_type="image/png",
        filename=f"datamatrix_{file.filename}.png"
    )


