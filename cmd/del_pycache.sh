# ./cmd/del_pycache.sh
find ./physicsLab -type d -name "__pycache__" -exec echo "Deleting {}" \;
find ./physicsLab -type d -name "__pycache__" -exec rm -rf {} \; 2>/dev/null