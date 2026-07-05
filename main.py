import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()

TARGET = "https://chat.mufy.ai"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"])
async def proxy(path: str, request: Request):
    url = f"{TARGET}/{path}"
    if request.url.query:
        url += f"?{request.url.query}"

    headers = dict(request.headers)
    headers.update(HEADERS)
    for h in ["host", "x-forwarded-for", "x-real-ip"]:
        headers.pop(h, None)
    headers["host"] = "chat.mufy.ai"

    body = await request.body()

    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.request(
            method=request.method,
            url=url,
            headers=headers,
            content=body,
        )

    proxy_host = str(request.base_url).rstrip("/")
    resp_headers = dict(resp.headers)
    for h in ["content-encoding", "transfer-encoding", "content-length"]:
        resp_headers.pop(h, None)

    content = resp.content
    try:
        text = content.decode("utf-8")
        text = text.replace("https://chat.mufy.ai", proxy_host)
        text = text.replace("http://chat.mufy.ai", proxy_host)
        content = text.encode("utf-8")
    except Exception:
        pass

    return Response(
        content=content,
        status_code=resp.status_code,
        headers=resp_headers,
        media_type=resp.headers.get("content-type"),
    )
