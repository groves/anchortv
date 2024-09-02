while true; do
    if ss -tln | grep -q ":8000 "; then
        break
    fi
    sleep 1
done

exec firefox --kiosk http://localhost:8000
