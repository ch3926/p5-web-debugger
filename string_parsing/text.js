let x = 0; const m = 67;
let blet = "false"; 
const c = 10;

function setup() { 
  x++;
  createCanvas(400, 400);
  createButton('click  me'); // comment

  
  background(220);
  
  x++;
  fill(255);
  for(let i = 0; i < 15; i++) {
    ellipse(random(width), random(height), random(100), random(100));
  }

}

let g = "abc"; let zf = 'def';


function draw() {
  for(let i = 0; i < 15; i++) {
    fill(random(255), random(255), random(255));
    ellipse(random(width), random(height), random(100), random(100));
  }
  x++;
} 


function do_stuff () {
  var key = false;
}