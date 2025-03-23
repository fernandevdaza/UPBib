docker compose down
move ./data ..
docker compose build backend
move "C:\Users\FDP18\PycharmProjects\data" .
docker compose up -d