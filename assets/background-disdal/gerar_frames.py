import asyncio,http.server,threading,functools,sys,os
from playwright.async_api import async_playwright
class Q(http.server.SimpleHTTPRequestHandler):
  def log_message(self,*a): pass
srv=http.server.ThreadingHTTPServer(('127.0.0.1',8812),functools.partial(Q,directory='.')); threading.Thread(target=srv.serve_forever,daemon=True).start()
N=int(sys.argv[1]); W=int(sys.argv[2]); H=int(sys.argv[3]); q=sys.argv[4]; out=sys.argv[5]; only=sys.argv[6:] 
os.makedirs(out,exist_ok=True)
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg=await b.new_page(viewport={'width':W,'height':H})
    pg.on('pageerror',lambda e:print('ERR',e))
    await pg.goto('http://127.0.0.1:8812/holo_anim.html'+q); await pg.wait_for_function('window.__pronto===true', timeout=180000)
    idx=[int(x) for x in only] if only else range(N)
    for i in idx:
      await pg.evaluate(f'window.__frame({i}/{N})'); await pg.screenshot(path=f'{out}/f{i:04d}.png')
    await b.close(); print('ok')
asyncio.run(main())
