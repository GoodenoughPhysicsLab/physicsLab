# ./cmd/del_pycache.sh
find ./physicsLab -name "__pycache__" -type d -exec rm -rf {} \; >/dev/null 2>&1