from flask import Flask, request, jsonify
import os
from pathlib import Path
from app.cli import make_report

app = Flask(__name__)

OUT_DIR = os.environ.get('OUT_DIR', '/work/out')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'apk' not in request.files:
        return jsonify({'error': 'no apk file provided'}), 400
    f = request.files['apk']
    save_dir = Path(OUT_DIR)
    save_dir.mkdir(parents=True, exist_ok=True)
    apk_path = save_dir / f.filename
    f.save(apk_path)
    report_path = make_report(str(apk_path), str(save_dir))
    return jsonify({'report': report_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
