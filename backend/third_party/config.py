import asyncio, orjson
from typing import Any
from pathlib import Path


class Configurator:
    def __init__(
        self, path: str, *, 
        default: dict = None
    ):
        self._lock = asyncio.Lock()
        self._path = Path(path)
        self._data = default or {}
        
        if self._path.exists():
            try:
                with open(str(self._path), 'rb') as f:
                    self._data = orjson.loads(f.read())
            except:
                pass
        else:
            self._path.parent.mkdir(exist_ok=True)        

    async def __aenter__(self):
        return self.data

    async def __aexit__(self, *args):
        await self.save()

    def __getitem__(self, name: str) -> Any:
        return self.data[name]

    def __setitem__(self, name: str, value: Any):
        self.data[name] = value

    def get(self, name: str, *, default: Any = None) -> Any:
        return self.data.get(name, default)
    
    @property
    def data(self):
        return self._data

    async def save(self):
        async with self._lock:
            with open(str(self._path), 'wb') as f:
                f.write(orjson.dumps(self._data))
