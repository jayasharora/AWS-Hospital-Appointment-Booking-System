import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("FLASK_ENV", "development").lower() == "development"
    print(f"🚀 MediCare Server running on http://{host}:{port}")
    print("📊 Monitoring dashboard available at: /monitoring")
    print("🧪 Fault Injection Lab available at: /simulation")
    print("📋 SLA Compliance available at: /sla")
    app.run(host=host, port=port, debug=debug)
