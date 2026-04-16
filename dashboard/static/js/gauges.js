class AttitudeIndicator {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.cx = this.canvas.width / 2;
        this.cy = this.canvas.height / 2;
        this.r = Math.min(this.cx, this.cy) - 4;
        this.roll = 0;
        this.pitch = 0;
        this.draw();
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

        ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        ctx.save();
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.clip();
        ctx.translate(cx, cy);
        ctx.rotate((-this.roll * Math.PI) / 180);

        const pitchOffset = this.pitch * 2;
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
        ctx.font = '10px Courier New';
        ctx.textAlign = 'center';
        ctx.lineWidth = 1;
        for (let deg = -30; deg <= 30; deg += 10) {
            if (deg === 0) continue;
            const y = pitchOffset - deg * 2;
            const w = Math.abs(deg) >= 20 ? 30 : 20;
            ctx.beginPath();
            ctx.moveTo(-w, y);
            ctx.lineTo(w, y);
            ctx.stroke();
            ctx.fillText(Math.abs(deg).toString(), w + 14, y + 3);
        }
        ctx.restore();

        ctx.strokeStyle = '#00ccff';
        ctx.lineWidth = 3;
        ctx.beginPath(); ctx.moveTo(cx - 40, cy); ctx.lineTo(cx - 15, cy); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(cx + 15, cy); ctx.lineTo(cx + 40, cy); ctx.stroke();
        ctx.beginPath(); ctx.arc(cx, cy, 4, 0, Math.PI * 2); ctx.stroke();

        ctx.strokeStyle = '#1e3a5f';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(cx, cy, r, 0, Math.PI * 2);
        ctx.stroke();
    }
}
