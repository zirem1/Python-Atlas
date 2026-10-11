from flask import Blueprint, jsonify, render_template, request

from app.database import init_db, lead_ekle, tum_leadler
from app.services.ai_service import AIService


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
def index():
    """Ana sayfayı gösterir."""
    return render_template("index.html")


@main.route("/dashboard", methods=["GET"])
def dashboard():
    """Kayıt panelini gösterir."""
    return render_template("dashboard.html")


@main.route("/health", methods=["GET"])
def health():
    """Sunucunun çalışıp çalışmadığını kontrol eder."""
    return jsonify({
        "status": "ok",
        "message": "Atlas API çalışıyor."
    }), 200


@main.route("/api/sohbet", methods=["POST"])
def sohbet():
    """Kullanıcı mesajına Atlas asistanından yanıt döndürür."""
    data = request.get_json(silent=True) or {}
    mesaj = data.get("mesaj", "")

    if not isinstance(mesaj, str) or not mesaj.strip():
        return jsonify({
            "error": "Lütfen boş olmayan bir mesaj gönder."
        }), 400

    try:
        yanit = AIService.yanit_uret(mesaj.strip())
        return jsonify({"yanit": yanit}), 200
    except Exception:
        return jsonify({
            "error": "Mesaj işlenirken beklenmeyen bir hata oluştu."
        }), 500


@main.route("/api/leads", methods=["POST"])
def lead_olustur():
    """Yeni bir kayıt oluşturur."""
    data = request.get_json(silent=True) or {}

    name = data.get("name")
    email = data.get("email", "")
    company = data.get("company", "")
    message = data.get("message")

    if not isinstance(name, str) or not name.strip():
        return jsonify({"error": "İsim alanı zorunludur."}), 400

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Mesaj alanı zorunludur."}), 400

    if not all(isinstance(value, str) for value in (email, company)):
        return jsonify({"error": "E-posta ve şirket alanları metin olmalıdır."}), 400

    try:
        new_id = lead_ekle(
            name.strip(),
            email.strip(),
            company.strip(),
            message.strip(),
        )
        return jsonify({
            "message": "Kayıt başarıyla oluşturuldu.",
            "id": new_id,
        }), 201
    except Exception:
        return jsonify({
            "error": "Kayıt oluşturulurken bir hata oluştu."
        }), 500


@main.route("/api/leads", methods=["GET"])
def leadleri_listele():
    """Kayıtları JSON formatında listeler."""
    try:
        return jsonify({"leads": tum_leadler()}), 200
    except Exception:
        return jsonify({
            "error": "Kayıtlar listelenirken bir hata oluştu."
        }), 500
