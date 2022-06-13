from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pykafka import KafkaClient

app = FastAPI()

def get_kafka_client():
    return KafkaClient(hosts='127.0.0.1:9092')

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    return templates.TemplateResponse("bus.html", {"request": request})

#Consumer API
@app.get("/bus/{topic_name}")
def get_message(topic_name: str):
    client = get_kafka_client()
    def events():
        for i in client.topics[topic_name].get_simple_consumer():
            yield 'data:{0}\n\n'.format(i.value.decode())
    return Response(events(), mimetype="test/event-stream")
