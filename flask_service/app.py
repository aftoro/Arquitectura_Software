from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.post("/api/v2/funcionalidad")
def calcular_cotizacion_cita():
    try:
        payload = request.get_json(silent=True) or {}

        precio_base = payload.get("precio_base")
        tipo = payload.get("tipo", "normal")

        if precio_base is None:
            return jsonify({"error": "precio_base es requerido"}), 400

        try:
            precio_base = float(precio_base)
        except (TypeError, ValueError):
            return jsonify({"error": "precio_base debe ser numérico"}), 400

        if precio_base <= 0:
            return jsonify({"error": "precio_base debe ser mayor a 0"}), 400

        multiplicadores = {
            "normal": 1.0,
            "premium": 1.35,
            "vip": 1.6,
        }

        if tipo not in multiplicadores:
            return jsonify({"error": "tipo inválido: usa normal, premium o vip"}), 400

        total = round(precio_base * multiplicadores[tipo], 2)

        return jsonify(
            {
                "mensaje": "Cotización calculada",
                "tipo": tipo,
                "precio_base": precio_base,
                "total": total,
            }
        ), 200
    except Exception:
        return jsonify({"error": "Error interno del microservicio"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
