// Common classes
function Point(pos, canvas) {
    this.x = pos.x - canvas.width / 2 || 0;
    this.y = pos.y - canvas.height / 2 || 0;
    this.z = pos.z || 0;

    this.cX = 0;
    this.cY = 0;
    this.cZ = 0;

    this.xPos = 0;
    this.yPos = 0;
    this.canvas = canvas;
    this.focal = canvas.width / 2;
    this.vpx = canvas.width / 2;
    this.vpy = canvas.height / 2;
    this.map2D();
}

Point.prototype.rotateZ = function (angleZ) {
    var cosZ = Math.cos(angleZ),
        sinZ = Math.sin(angleZ),
        x1 = this.x * cosZ - this.y * sinZ,
        y1 = this.y * cosZ + this.x * sinZ;

    this.x = x1;
    this.y = y1;
}

Point.prototype.map2D = function () {
    var scaleX = this.focal / (this.focal + this.z + this.cZ),
        scaleY = this.focal / (this.focal + this.z + this.cZ);

    this.xPos = this.vpx + (this.cX + this.x) * scaleX;
    this.yPos = this.vpy + (this.cY + this.y) * scaleY;
};

function Square(z, canvas) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d");
    this.width = canvas.width / 2;

    if (canvas.height < 200) {
        this.width = 200;
    }

    this.height = canvas.height;
    z = z || 0;

    this.points = [
        new Point({
            x: (canvas.width / 2) - this.width,
            y: (canvas.height / 2) - this.height,
            z: z
        }, canvas),
        new Point({
            x: (canvas.width / 2) + this.width,
            y: (canvas.height / 2) - this.height,
            z: z
        }, canvas),
        new Point({
            x: (canvas.width / 2) + this.width,
            y: (canvas.height / 2) + this.height,
            z: z
        }, canvas),
        new Point({
            x: (canvas.width / 2) - this.width,
            y: (canvas.height / 2) + this.height,
            z: z
        }, canvas)
    ];
    this.dist = 0;
}

Square.prototype.update = function () {
    for (var p = 0; p < this.points.length; p++) {
        this.points[p].rotateZ(0.001);
        this.points[p].z -= 3;
        if (this.points[p].z < -300) {
            this.points[p].z = 2700;
        }
        this.points[p].map2D();
    }
}

Square.prototype.render = function () {
    this.ctx.beginPath();
    this.ctx.moveTo(this.points[0].xPos, this.points[0].yPos);
    for (var p = 1; p < this.points.length; p++) {
        if (this.points[p].z > -(this.points[p].focal - 50)) {
            this.ctx.lineTo(this.points[p].xPos, this.points[p].yPos);
        }
    }
    this.ctx.closePath();
    this.ctx.stroke();
    this.dist = this.points[this.points.length - 1].z;
};

// Canvas 1: 3D Squares
function initCanvasSquares() {
    const canvas = document.querySelector(".hacker-3d-shiz");
    const ctx = canvas.getContext("2d");

    let squares = [];
    let focal = canvas.width / 2;
    let vpx = canvas.width / 2;
    let vpy = canvas.height / 2;

    function render() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        squares.sort(function (a, b) {
            return b.dist - a.dist;
        });
        for (var i = 0, len = squares.length; i < len; i++) {
            squares[i].update();
            squares[i].render();
        }

        requestAnimationFrame(render);
    }

    function resize(){
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        focal = canvas.width / 2;
        vpx = canvas.width / 2;
        vpy = canvas.height / 2;

        for (var i = 0; i < squares.length; i++) {
            squares[i].canvas = canvas;
        }
    }

    window.addEventListener('resize', resize);

    resize();

    for (var i = 0; i < 15; i++) {
        squares.push(new Square(-300 + (i * 200), canvas));
    }

    ctx.strokeStyle = '#00FF00';

    render();
}
document.addEventListener("DOMContentLoaded", function () {
    initCanvasSquares();
});
