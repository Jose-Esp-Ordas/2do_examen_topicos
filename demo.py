from db.models import User, Zone

usuario_demo = User(email="demo@iberopuebla.mx", 
                    api_key="testkey", balance=300.0)

zona_demo_a = Zone(name="A", rate_per_min=1.5, max_minutes=120)
zona_demo_b = Zone(name="B", rate_per_min=1.0, max_minutes=180)