# 2do_examen_topicos
Examen: Generar una api similar a parkimovil
Endpoints:
GET /zones → lista zonas.
POST /vehicles → { plate } crea vehículo del usuario.
GET /vehicles → lista vehículos del usuario.
POST /sessions/start → { plate, zone_id } crea sesión (si no hay activa por placa).
POST /sessions/stop → { session_id } calcula minutos, costo y aplica reglas.
GET /sessions/{id} → detalle (incluye minutes, cost, status, y cost_total si multa).
POST /wallet/deposit → { amount } aumenta balance.
Puedes acceder a la documentación al iniciar la api con fastapi dev y llendo a la ruta: http://127.0.0.1:8000/docs