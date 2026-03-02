# ─────────────────────────────────────────────
#  RIZK Banque – Backend Python (Flask + SMTP)
#  Gmail SMTP – Login & Registration with email
# ─────────────────────────────────────────────

from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from your HTML frontend

   
   
    

# ──────────────────────────────────────────────
#  CONFIGURATION — Fill in your Gmail credentials
# ──────────────────────────────────────────────
CONFIG = {
    "GMAIL_USER": "ayayessad004l@gmail.com",       # ← Your Gmail address
    "GMAIL_PASS": "AYA 004",         # ← Gmail App Password (NOT your normal password)
                                                  #   Generate at: myaccount.google.com/apppasswords
    "PORT": 3000
}

# ──────────────────────────────────────────────
#  In-memory user store (replace with a real DB)
# ──────────────────────────────────────────────
users = []


# ──────────────────────────────────────────────
#  Email sender
# ──────────────────────────────────────────────
def send_confirmation_email(firstname, lastname, email, phone, card):
    date_str = datetime.now().strftime("%d %B %Y")
    masked_card = "**** **** **** " + card[-4:]  # Show only last 4 digits

    html_content = f"""
<!DOCTYPE html>
<html lang="fr">
<head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f5f3ee;font-family:'Segoe UI',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f3ee;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#ffffff;border-top:4px solid #c9a84c;">

        <!-- Header -->
        <tr>
          <td style="background:#0b1f3a;padding:24px 36px;text-align:center;">
            <table cellpadding="0" cellspacing="0" align="center">
              <tr>
                <td style="background:#c9a84c;width:46px;height:46px;border-radius:50%;text-align:center;vertical-align:middle;">
                  <span style="font-size:20px;font-weight:700;color:#0b1f3a;">R</span>
                </td>
                <td style="padding-left:12px;">
                  <span style="font-size:20px;font-weight:700;color:#ffffff;letter-spacing:3px;">RIZK</span><br>
                  <span style="font-size:9px;color:#c9a84c;letter-spacing:2px;text-transform:uppercase;">Banque · Finance · Avenir</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Body -->
        <tr>
          <td style="padding:36px 40px;">
            <h2 style="color:#0b1f3a;font-size:22px;margin:0 0 8px;">Bienvenue, {firstname} !</h2>
            <p style="color:#5a5a5a;font-size:14px;margin:0 0 24px;line-height:1.6;">
              Votre compte RIZK Banque a été créé avec succès. Voici un récapitulatif de vos informations d'inscription.
            </p>

            <!-- Summary box -->
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f3ee;border-left:4px solid #c9a84c;margin-bottom:24px;">
              <tr><td style="padding:20px 24px;">
                <p style="margin:0 0 6px;font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#0b1f3a;">
                  Récapitulatif de votre inscription
                </p>
                <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:12px;">
                  <tr>
                    <td style="font-size:13px;color:#5a5a5a;padding:5px 0;width:40%;">Prénom :</td>
                    <td style="font-size:13px;color:#2c2c2c;font-weight:600;padding:5px 0;">{firstname}</td>
                  </tr>
                  <tr>
                    <td style="font-size:13px;color:#5a5a5a;padding:5px 0;">Nom :</td>
                    <td style="font-size:13px;color:#2c2c2c;font-weight:600;padding:5px 0;">{lastname}</td>
                  </tr>
                  <tr>
                    <td style="font-size:13px;color:#5a5a5a;padding:5px 0;">E-mail :</td>
                    <td style="font-size:13px;color:#2c2c2c;font-weight:600;padding:5px 0;">{email}</td>
                  </tr>
                  <tr>
                    <td style="font-size:13px;color:#5a5a5a;padding:5px 0;">Téléphone :</td>
                    <td style="font-size:13px;color:#2c2c2c;font-weight:600;padding:5px 0;">{phone}</td>
                  </tr>
                  <tr>
                    <td style="font-size:13px;color:#5a5a5a;padding:5px 0;">Carte bancaire :</td>
                    <td style="font-size:13px;color:#2c2c2c;font-weight:600;padding:5px 0;">{masked_card}</td>
                  </tr>
                  <tr>
                    <td style="font-size:13px;color:#5a5a5a;padding:5px 0;">Date d'inscription :</td>
                    <td style="font-size:13px;color:#2c2c2c;font-weight:600;padding:5px 0;">{date_str}</td>
                  </tr>
                </table>
              </td></tr>
            </table>

            <p style="color:#5a5a5a;font-size:13.5px;line-height:1.7;margin-bottom:24px;">
              Si vous n'êtes pas à l'origine de cette inscription, veuillez contacter notre service clientèle immédiatement au <strong style="color:#0b1f3a;">3030</strong>.
            </p>

            <!-- CTA -->
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="background:#0b1f3a;padding:12px 28px;border-radius:2px;">
                  <a href="#" style="color:#c9a84c;font-size:13px;font-weight:700;text-decoration:none;letter-spacing:1px;text-transform:uppercase;">
                    Accéder à mon espace client →
                  </a>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <!-- Footer -->
        <tr>
          <td style="background:#f5f3ee;padding:18px 40px;text-align:center;border-top:1px solid #ddd8cc;">
            <p style="font-size:11px;color:#999;margin:0;">
              © 2025 RIZK Banque. Agrément Banque d'Algérie N° 001-B.<br>
              Cet e-mail est automatique, merci de ne pas y répondre.
            </p>
          </td>
        </tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Confirmation de votre inscription – RIZK Banque"
    msg["From"]    = f"RIZK Banque <{CONFIG['GMAIL_USER']}>"
    msg["To"]      = email

    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(CONFIG["GMAIL_USER"], CONFIG["GMAIL_PASS"])
            server.sendmail(CONFIG["GMAIL_USER"], email, msg.as_string())
        print(f"✓ Confirmation email sent to {email}")
    except Exception as e:
        print(f"✗ Email error: {e}")


# ──────────────────────────────────────────────
#  ROUTES
# ──────────────────────────────────────────────

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    firstname = data.get("firstname", "").strip()
    lastname  = data.get("lastname", "").strip()
    email     = data.get("email", "").strip()
    phone     = data.get("phone", "").strip()
    password  = data.get("password", "")
    card      = data.get("card", "").replace(" ", "").strip()

    # Basic validation
    if not all([firstname, lastname, email, phone, password]):
        return jsonify({"message": "Tous les champs sont requis."}), 400

    if len(password) < 8:
        return jsonify({"message": "Le mot de passe doit contenir au moins 8 caractères."}), 400

    # Card number validation
    if not card.isdigit() or len(card) != 16:
        return jsonify({"message": "Numéro de carte invalide (16 chiffres requis)."}), 400

    # Check duplicate email
    if any(u["email"] == email for u in users):
        return jsonify({"message": "Un compte avec cet e-mail existe déjà."}), 409

    # Check duplicate card
    if any(u["card"] == card for u in users):
        return jsonify({"message": "Cette carte bancaire est déjà associée à un compte."}), 409

    # Save user (in production: save to DB with hashed password using bcrypt)
    users.append({
        "firstname": firstname,
        "lastname":  lastname,
        "email":     email,
        "phone":     phone,
        "password":  password,
        "card":      card,
        "created_at": datetime.now().isoformat()
    })

    # Send confirmation email (non-blocking — won't fail registration if email fails)
    send_confirmation_email(firstname, lastname, email, phone, card)

    return jsonify({"message": "Compte créé avec succès."}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email    = data.get("email", "").strip()
    password = data.get("password", "")
    card     = data.get("card", "").replace(" ", "").strip()

    if not email or not password:
        return jsonify({"message": "E-mail et mot de passe requis."}), 400

    if not card:
        return jsonify({"message": "Numéro de carte requis."}), 400

    # Step 1: check email exists
    user_by_email = next((u for u in users if u["email"] == email), None)
    if not user_by_email:
        return jsonify({"message": "Identifiants incorrects. Veuillez réessayer."}), 401

    # Step 2: check password
    if user_by_email["password"] != password:
        return jsonify({"message": "Identifiants incorrects. Veuillez réessayer."}), 401

    # Step 3: check card number
    if user_by_email["card"] != card:
        return jsonify({"message": "Numéro de carte incorrect pour ce compte."}), 401

    user = user_by_email

    return jsonify({
        "message": "Connexion réussie.",
        "user": {
            "firstname": user["firstname"],
            "lastname":  user["lastname"],
            "email":     user["email"]
        }
    }), 200


# ──────────────────────────────────────────────
#  START
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print(f"\n🏦 RIZK Banque API running on http://localhost:{CONFIG['PORT']}")
    print("   POST /api/register")
    print("   POST /api/login\n")
    app.run(port=CONFIG["PORT"], debug=True)
