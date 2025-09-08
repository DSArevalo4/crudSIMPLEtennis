# 1. Obtener todos los torneos
curl -X GET http://localhost:5000/api/torneos

# 2. Obtener un torneo por ID (reemplaza open2024 por el ID real)
curl -X GET http://localhost:5000/api/torneos/open2024

# 4. Crear un nuevo torneo
curl -X POST http://localhost:5000/api/torneos \
  -H "Content-Type: application/json" \
  -d '{
    "id": "open2024",
    "nombre": "Open 2024",
    "superficie": "arcilla",
    "nivel": "ATP 250",
    "fecha": "2024-09-10"
  }'

# 6. Actualizar un torneo existente (reemplaza open2024 por el ID real)
curl -X PUT http://localhost:5000/api/torneos/open2024 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Open 2024 Actualizado",
    "superficie": "dura",
    "nivel": "ATP 500",
    "fecha": "2024-09-15"
  }'

# 8. Eliminar un torneo existente (reemplaza open2024 por el ID real)
curl -X DELETE http://localhost:5000/api/torneos/open2024
