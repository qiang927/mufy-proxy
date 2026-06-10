Deno.serve(async (req) => {
  const incomingUrl = new URL(req.url);

  const targetUrl =
    "https://chat.mufy.ai" +
    incomingUrl.pathname +
    incomingUrl.search;

  const headers = new Headers(req.headers);

  headers.set(
    "Origin",
    "https://chat.mufy.ai"
  );

  headers.set(
    "Referer",
    "https://chat.mufy.ai/"
  );

  headers.delete("host");

  try {
    const response = await fetch(targetUrl, {
      method: req.method,
      headers,
      body:
        req.method === "GET" ||
        req.method === "HEAD"
          ? undefined
          : req.body,
      redirect: "follow"
    });

    const responseHeaders =
      new Headers(response.headers);

    responseHeaders.set(
      "Access-Control-Allow-Origin",
      "*"
    );

    responseHeaders.set(
      "Access-Control-Allow-Methods",
      "*"
    );

    responseHeaders.set(
      "Access-Control-Allow-Headers",
      "*"
    );

    return new Response(
      response.body,
      {
        status: response.status,
        headers: responseHeaders
      }
    );

  } catch (error) {

    return new Response(
      `Proxy Error: ${error}`,
      {
        status: 500
      }
    );
  }
});
