import asyncio
import fastapi
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import json

load_dotenv()
app = FastAPI()

# Setup CORS to allow all origins and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.route('/v1/{path:path}', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
async def handle(request: fastapi.Request):
    path = request.url.path.replace('/v1/v1', '/v1')  # fix double v1

    try:
        json_payload = await request.json()
    except:
        json_payload = {}

    text = 'Coming Soon. I am gonna love you'
    character = 10
    chunks = [text[i: i + character] for i in range(0, len(text), character)]

    # Create chunks for the mocked GPT-like JSON response
    async def response():
        response_template = 'data: {{"id": "mocked_id", "object": "chat.completion.chunk", "created": 0, "model": "gpt-mocked", "choices": [{{"index": 0, "delta": {0}, "finish_reason": {1}}}]}}\n\n'
        for chunk in chunks:
            delta = '{{"role": "assistant", "content": "{}"}}'.format(chunk)
            payload = response_template.format(delta, 'null')
            yield payload.encode()
            await asyncio.sleep(0.01)

        empty_delta = '{}'
        payload = response_template.format(empty_delta, '"stop"')
        yield payload.encode()

    return fastapi.responses.StreamingResponse(response(), media_type='text/event-stream')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=1025, ssl_keyfile="privkey.pem", ssl_certfile="cert.pem")
