import threading
import json
import time
import os

class TrapsService:
    def __init__(self, routers):
        self.routers = routers
        self.trap_threads = {}  # {(host, interfaz): thread}

    def get_interface_trap_status(self, host, interfaz):
        key = (host, interfaz)
        activo = key in self.trap_threads
        filename = f"data/traps_{host.replace('.', '_')}_{interfaz.replace('/', '_')}.json"
        hay_datos = os.path.exists(filename)
        return {
            "router": host,
            "interfaz": interfaz,
            "captura_activa": activo,
            "archivo_datos": hay_datos
        }

    def start_trap_capture(self, host, interfaz):
        key = (host, interfaz)
        if key in self.trap_threads:
            return False  # ya hay captura

        def capture():
            filename = f"data/traps_{host.replace('.', '_')}_{interfaz.replace('/', '_')}.json"
            traps = []
            while key in self.trap_threads:
                # Simula traps cada 10s alternando linkUp y linkDown
                trap_type = "linkUp" if len(traps) % 2 == 0 else "linkDown"
                traps.append({
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "type": trap_type
                })
                with open(filename, "w") as f:
                    json.dump(traps, f, indent=2)
                time.sleep(10)

        t = threading.Thread(target=capture, daemon=True)
        self.trap_threads[key] = t
        t.start()
        return True

    def stop_trap_capture(self, host, interfaz):
        key = (host, interfaz)
        if key in self.trap_threads:
            del self.trap_threads[key]
            return True
        return False
