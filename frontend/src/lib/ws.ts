export function connectWS(url: string, onMessage: (msg: any) => void) {
    const ws = new WebSocket(url);
    ws.onmessage = (ev) => {
      try {
        const parsed = JSON.parse(ev.data);
        onMessage(parsed);
      } catch (e) {
        console.error('WS parse error', e);
      }
    };
    return ws;
  }
  