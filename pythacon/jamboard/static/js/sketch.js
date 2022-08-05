let isOnCanvas = false;
let colors = ["black", "red", "yellow", "blue", "green", "white"],
  idc = 0;
let weight = 1;
let initvar=true;

function setup() {
  let c = createCanvas(700, 700);
  c.parent("sketch");
  c.elt.addEventListener("mouseleave", () => {
    isOnCanvas = false;
  });
  c.elt.addEventListener("mouseenter", () => {
    isOnCanvas = true;
  });
}

function draw() {
  if(initvar && cood){
    cood.forEach(serverDraw);
    initvar=false;
  }
  if (mouseIsPressed && isOnCanvas && notResizing) {
    let px = pmouseX,
      py = pmouseY,
      x = mouseX,
      y = mouseY;
    strokeWeight(weight);
    stroke(colors[idc]);
    line(px, py, x, y);
    chatSocket.send(
      JSON.stringify({
        type: "draw",
        px,
        py,
        x,
        y,
        w: weight,
        c: colors[idc],
      })
    );
  }
}

function serverDraw(data) {
  strokeWeight(data.w);
  stroke(data.c);
  line(data.px, data.py, data.x, data.y);
}

function changeColor(color) {
  idc = colors.indexOf(color);
}

function changeWeight() {
  weight = document.querySelector("#weights").value;
}

function clearCan() {
  clearC();
  chatSocket.send(
    JSON.stringify({
      type: "clear",
    })
  );
}

function clearC() {
  noStroke();
  fill("white");
  rect(0, 0, width, height);
}
