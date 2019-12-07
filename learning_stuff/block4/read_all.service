[Unit]
Description=AstroPlant Explorer Read All Sensors
After=network-online.target

[Service]
ExecStart=/usr/bin/python3 -u read_all.py
WorkingDirectory=/home/pi/Explorer/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target

