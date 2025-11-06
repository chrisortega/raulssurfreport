surfline rauls surf report 

docker build -t surf-report .

docker run -p 5000:5000 surf-report

for ngrok 

docker run -d --restart unless-stopped -e NGROK_AUTHTOKEN=xxxxxxxxxxxxxxxxxxxxxx --name ngrok-agent ngrok/ngrok http host.docker.internal:5000
