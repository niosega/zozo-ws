build: Dockerfile
	@sudo docker build -t zozo-ws .

run:
	@sudo docker run --rm -p5000:5000 -e RENAULT_PASS='${RENAULT_PASS}' -e RENAULT_USER="${RENAULT_USER}" zozo-ws
