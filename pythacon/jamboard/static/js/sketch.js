let isOnCanvas=false;
function setup() {
  let c=createCanvas(600, 600);
  c.parent("sketch");
  c.elt.addEventListener('mouseleave', ()=> {isOnCanvas=false;});
  c.elt.addEventListener('mouseenter', ()=> {isOnCanvas=true;});
  
}

function draw() {
  if (mouseIsPressed && isOnCanvas && notResizing) {
    let px = pmouseX,
      py = pmouseY,
      x = mouseX,
      y = mouseY;
    stroke(0);
    line(px, py, x, y);
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
}

function serverDraw(data) {
  stroke(0);
  line(data.px, data.py, data.x, data.y);
}
