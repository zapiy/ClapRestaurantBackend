class AsyncLock {
  constructor() {
    this.free = () => null;
    this._wait = null;
  }

  async lock(lock = false) {
    if (this._wait == null) {
      this._wait = new Promise((resolve) => (this.free = resolve));
      if (!lock) return;
    }
    await this._wait;
  }
}

export default AsyncLock;
