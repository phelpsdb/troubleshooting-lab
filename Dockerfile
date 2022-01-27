FROM python:3.10.2-alpine3.15
WORKDIR /opt/pyserver/
ADD . .
CMD ["./start_scenario.sh"]
