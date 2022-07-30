let isOnCanvas=false;
function setup() {
  let c=createCanvas(600, 600);
  c.parent("sketch");
  c.elt.addEventListener('mouseleave', ()=> {isOnCanvas=false;});
  c.elt.addEventListener('mouseenter', ()=> {isOnCanvas=true;});
  chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data);
    if (data.type == "draw") serverDraw(JSON.parse(e.data));
  };
}

function draw() {
  if (mouseIsPressed && isOnCanvas && notResizing) {
    let px = pmouseX,
      py = pmouseY,
      x = mouseX,
      y = mouseY;
    stroke(0);
    line(px, py, x, y);
  }
}

function serverDraw(data) {
  stroke(0);
  line(data.px, data.py, data.x, data.y);
}

function mouseDragged() {
  if(isOnCanvas && notResizing)
    chatSocket.send(
      JSON.stringify({
        type: "draw",
        px: pmouseX,
        py: pmouseY,
        x: mouseX,
        y: mouseY,
      })
    );
}
