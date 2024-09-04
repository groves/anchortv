unclutter -idle 2 -root &
while true; do
    if ss -tln | grep -q ":8000 "; then
        break
    fi
    sleep 1
done

exec firefox --remote-debugging-port 9222 --kiosk http://localhost:8000
