function server() {
        pipenv run python main.py
}

until server; do
    echo "Server crashed with exit code $?.  Respawning.." >&2
    sleep 1
done