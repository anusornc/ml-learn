/**
 * Cloudflare Worker: Reverse Proxy for Jev AI Decision API
 * 
 * ใช้สำหรับข้ามข้อจำกัด Browser CORS เมื่อเปิดเว็บผ่าน GitHub Pages
 * (Cloudflare Workers มีโควตาฟรี 100,000 requests/วัน)
 * 
 * ขั้นตอนการติดตั้ง (ใช้เวลา ~1 นาที):
 * 1. ไปที่ https://dash.cloudflare.com -> Workers & Pages -> Create Application -> Create Worker
 * 2. คัดลอกโค้ดนี้ทั้งหมดไปวางแทนที่ในหน้าต่าง Code Editor ของ Cloudflare
 * 3. กด "Deploy"
 * 4. คัดลอก URL ของ Worker ที่ได้ (เช่น https://jev-proxy.username.workers.dev/api/v1/decisions)
 * 5. ไปที่เว็บ https://anusornc.github.io/ml-learn/lab-jev-decision/index.html
 *    คลิก "ตั้งค่า API Key" แล้วนำ URL ไปวางในช่อง "Custom API Proxy Endpoint"
 */

export default {
  async fetch(request, env, ctx) {
    // 1. ตอบกลับ Preflight CORS (OPTIONS) ล่วงหน้า
    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, Origin, User-Agent",
          "Access-Control-Max-Age": "86400",
        }
      });
    }

    const url = new URL(request.url);
    const targetUrl = `https://www.jevai.org${url.pathname}${url.search}`;

    // 2. ปรับแต่ง Headers เพื่อไม่ให้ติด Cloudflare WAF Error 1010
    const newHeaders = new Headers(request.headers);
    newHeaders.set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36");
    newHeaders.set("Host", "www.jevai.org");

    const proxyRequest = new Request(targetUrl, {
      method: request.method,
      headers: newHeaders,
      body: request.body,
      redirect: "follow"
    });

    try {
      const response = await fetch(proxyRequest);
      const resHeaders = new Headers(response.headers);
      
      // 3. แนบ CORS Header ขากลับ เพื่อให้เบราว์เซอร์ยอมรับข้อมูล
      resHeaders.set("Access-Control-Allow-Origin", "*");
      resHeaders.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
      resHeaders.set("Access-Control-Allow-Headers": "Authorization, Content-Type, Accept");

      return new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: resHeaders
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message, message: "Worker proxy failed to reach Jev API" }), {
        status: 502,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      });
    }
  }
};
