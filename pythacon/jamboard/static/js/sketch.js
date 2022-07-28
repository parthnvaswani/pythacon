function setup() {
  createCanvas(600, 600);

    chatSocket.onmessage = function (e) {
        let data = JSON.parse(e.data);
        if(data.type == 'draw') 
            serverDraw(JSON.parse(e.data));
    };
}

function draw() {
  if (mouseIsPressed) {
    let px = pmouseX, py = pmouseY, x = mouseX, y = mouseY;
    stroke(0);
    line(px, py, x, y);
  }
}

function serverDraw(data) {
  stroke(0);
  line(data.px, data.py, data.x, data.y);
}

function mouseDragged() {
  chatSocket.send(JSON.stringify({'type': 'draw','px': pmouseX, 'py': pmouseY, 'x': mouseX, 'y': mouseY}));
}
