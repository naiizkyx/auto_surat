from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
import os
import json
import io

app = Flask(__name__, template_folder="templates_html")

# Load konfigurasi field dan template surat
with open("forms_config.json", "r") as f:
    FORM_CONFIG = json.load(f)

from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate
import os
import json
import io

# app = Flask(__name__, template_folder="templates_html")
app = Flask(__name__, template_folder="templates_html", static_folder="static")

# Load konfigurasi field dan template surat
with open("forms_config.json", "r") as f:
    FORM_CONFIG = json.load(f)

@app.route("/", methods=["GET", "POST"])
def index():
    jenis_surat = ""
    fields = []
    is_final_submit = False

    if request.method == "POST":
        jenis_surat = request.form.get("jenis_surat", "")
        fields = FORM_CONFIG.get(jenis_surat, {}).get("fields", [])

        # Cek apakah semua field sudah diisi dengan nilai (bukan kosong)
        if all(request.form.get(field["name"], "").strip() != "" for field in fields):
            is_final_submit = True

        if is_final_submit:
            context = {field["name"]: request.form.get(field["name"]) for field in fields}
            template_path = os.path.join("templates", FORM_CONFIG[jenis_surat]["template"])
            doc = DocxTemplate(template_path)
            doc.render(context)

            output_stream = io.BytesIO()
            doc.save(output_stream)
            output_stream.seek(0)

            filename = f"{jenis_surat}_{context.get('nama', 'pengguna')}.docx"
            return send_file(output_stream, as_attachment=True, download_name=filename)

    return render_template("index.html", config=FORM_CONFIG, jenis_surat=jenis_surat, fields=fields)

if __name__ == "__main__":
    app.run(debug=True)
