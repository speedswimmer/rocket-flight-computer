class AttitudeIndicator {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.roll = 0;
        this.pitch = 0;
        this._resize();
        this.draw();

        window.addEventListener('resize', this._onResize.bind(this));
    }

    _onResize() {
        this._resize();
        this.draw();
    }

    _resize() {
        // Match canvas resolution to its CSS display size
        var rect = this.canvas.getBoundingClientRect();
        var size = Math.round(Math.min(rect.width, rect.height)) || 300;
        this.canvas.width = size;
        this.canvas.height = size;
        this.cx = size / 2;
        this.cy = size / 2;
        this.r = Math.min(this.cx, this.cy) - 4;
    }

    update(roll, pitch) {
        this.roll = roll || 0;
        this.pitch = pitch || 0;
        this.draw();
    }

    draw() {
        const ctx = this.ctx;
        const cx = this.cx;
        const cy = this.cy;
        const r = this.r;
        const scale = r / 146; // scale relative to original 300px (r=146)

        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.clip();
        ctx.translate(cx, cy);
        ctx.rotate((-this.roll * Math.PI) / 180);

        const pitchOffset = this.pitch * 2 * scale;
        ctx.fillStyle = '#1a3a6a';
        ctx.fillRect(-r, -r + pitchOffset, r * 2, r);
        ctx.fillStyle = '#4a2a0a';
        ctx.fillRect(-r, pitchOffset, r * 2, r);

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(-r, pitchOffset);
        ctx.lineTo(r, pitchOffset);
        ctx.stroke();

        ctx.strokeStyle = '#ffffff';
        ctx.fillStyle = '#ffffff';
        ctx.font = Math.round(10 * scale) + 'px Courier New';
        ctx.textAlign = 'center';
        ctx.lineWidth = 1;
        for (let deg = -30; deg <= 30; deg += 10) {
            if (deg === 0) continue;
            const y = pitchOffset - deg * 2 * scale;
            const w = (Math.abs(deg) >= 20 ? 30 : 20) * scale;
            ctx.beginPath();
            ctx.moveTo(-w, y);
            ctx.lineTo(w, y);
            ctx.stroke();
            ctx.fillText(Math.abs(deg).toString(), w + 14 * scale, y + 3 * scale);
        }
        ctx.restore();

        ctx.strokeStyle = '#00ccff';
        ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(cx - 40 * scale, cy); ctx.lineTo(cx - 15 * scale, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx + 15 * scale, cy); ctx.lineTo(cx + 40 * scale, cy); ctx.stroke();
        ctx.beginPath(); ctx.arc(cx, cy, 4 * scale, 0, Math.PI * 2); ctx.stroke();

        ctx.strokeStyle = '#1e3a5f';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();
    }
}
