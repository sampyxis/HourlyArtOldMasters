/*
  Doing another version of hourly art
  I like the ones I was doing earlier where I could kind of see the image.
  Will try for that.
*/
// GUI
import java.awt.Frame;
import java.awt.BorderLayout;
import java.util.Calendar;
import processing.pdf.*;
import gifAnimation.*;


int x,y;
int curvePointX = 0;
int curvePointY = 0;
int pointCount = 2;
int loopNum = 0;
int numOpp = 100;
int loopNumLine = 0;
int numOppLine = 100;
float lineWeight = 0;
float diffusion = 50;
int sliderNumOpp=0;
int pixelIndex;
color c;
int timeToRun = 15000;
int framesRan = 0;

boolean save = false;
boolean pause = false;
boolean drawLines = false;
boolean drawSmLines = false;
boolean drawCurves = true;

boolean smCurves = true;
boolean smLines = true;

boolean showTint = false;

boolean painterly = false;
PImage img;
GifMaker gifExport;
int gifRate = 250;
int drawCount = 0;
static int   FRAME_RATE = 30;

//ImageFrame imageFrame;

void setup() {

  gifExport = new GifMaker(this, "newImage.gif");
  // make it a looping animation
  gifExport.setRepeat(0);
  
  textSize(32);
  img = loadImage("newImage.jpg");
  size(img.width, img.height);
  x = width/2;
  y = height/2;

 save = false;
 pause = false;
}

void draw() {
  colorMode(HSB, 360,100,100);    
  smooth();
  noFill();
    
  pixelIndex = ( x+ (y*img.width ));
  c = img.pixels[pixelIndex];
  color(c,random(1,255));

  // The last random function adds more thickness to the line
  if(painterly == true) {
    lineWeight = hue(c)/(int)random(30,50) * random(1,5);
  } else {
    lineWeight = (int)random(.1, 4);
  }  
  strokeWeight(lineWeight/2);
  stroke(c);
    
//    println("loop: " +loopNum);
//    // Every numOpp times - get the opposite color
//    if( loopNum == numOpp) {
//      loopNum = 0;
//      float R = red(c);
//      float G = green(c);
//      float B = blue(c);
//      float minRGB = min(R,min(G,B));
//      float maxRGB = max(R,max(G,B));
//      float minPlusMax = minRGB + maxRGB;
//      color complement = color(minPlusMax-R, minPlusMax-G, minPlusMax-B);
//      stroke(complement);
//    } else {
//      stroke(c);
//      loopNum ++;
//    }
    
    // how to draw
    // Default all to true to start
    drawLines = true;
    drawSmLines = true;
    drawCurves = true;
  
    if(!pause) {
      if( drawLines ) {
        drawLines();
      }
      if(drawSmLines) {
       drawSmallLines();
      }
      if(drawCurves) {
        drawCurves();
      }
    }
    
    // change the size
    pointCount = (int)random(.1,3);
  
    // Only take a picture every gifRate (starting at a minute) since it takes so long to make the picture
    // we make the gif-"framerate" the same as the sketch framerate.
    // Change the below line to increase the delay, so I don't need to add so many frames to the picture
    gifExport.setDelay(100/FRAME_RATE);//1000/FRAME_RATE);
    if (gifRate == drawCount){
//        println("adding gliff");
        // Taking the same frame more than once in order for it to be more smooth...
        //gifExport.addFrame();
        //gifExport.addFrame();
        gifExport.addFrame();
        drawCount =0;
    }
    drawCount ++;
    
    framesRan ++;
    // check if we're done
    if(framesRan == timeToRun){
      cleanUp();
    }
}

void cleanUp(){
  //saveFrame(timestamp()+"_##.png");
  saveFrame("newImage.png");
  gifExport.finish();
  println("gif exported");
  exit();
}

void drawSmallLines(){
  //strokeWeight(random(.1,5));
  if (loopNumLine >= numOppLine) {
    if(smLines){
      line(x,y, x+ random(-width, width)/8, y + random(-height, height)/8);
    } else {
      line(x,y, x+ random(-width, width)/2, y + random(-height, height)/2);
    }
    loopNumLine = 0;
  } else {
    line(x, y, x+ random(1,10), y+ random(1,10));
    loopNumLine = loopNumLine + (int)random(-1,5);
    x = (int)random(0, width);
    y  = (int)random(0, height);
  }
}

void drawCurves() {
    // every numOpp times - do a stright line
  if( loopNumLine >= numOppLine ) {
    if(smLines){
      line(x,y, x+ random(-width, width)/8, y + random(-height, height)/8);
    } else {
      line( x, y, x + random(-width,width)/2, y + random(-height,height)/2);
    }
    loopNumLine = 0;
  } else {
    beginShape();
    curveVertex(x,y);
    curveVertex(x,y);
    for( int i = 0; i<pointCount; i++) {
      if(smCurves) {
        curvePointX = (int)constrain(x+random(-10, 10), 0, width-1);
        curvePointY = (int)constrain(y+random(-10,10),0, height-1);        
      } else {
        curvePointX = (int)constrain(x+random(-50, 50), 0, width-1);
        curvePointY = (int)constrain(y+random(-50,50),0, height-1);
      }
      curveVertex(curvePointX, curvePointY);
    }   
    curveVertex(curvePointX, curvePointY);
    endShape();
    x = curvePointX;
    y = curvePointY;
    loopNumLine = loopNumLine + (int)random(-1,5);
  }
}

void drawLines() {
  //strokeWeight(random(.1,1));
  if (loopNumLine >= numOppLine) {
    if(smLines){
      line(x,y, x+ random(-width, width)/8, y + random(-height, height)/8);
    } else {
      line(x,y, x+ random(-width, width)/2, y + random(-height, height)/2);
    }
    loopNumLine = 0;
  } else {
    line(x, y, x+ random(1,50), y+ random(1,50));
    loopNumLine = loopNumLine + (int)random(-1,5);
    x = (int)random(0, width);
    y  = (int)random(0, height);
  }
  
}

void printText(String text, int locationX, int locationY) {
  //text(text, locationX, locationY);
  println(text);
}

void keyReleased(){
  if (key == 's' || key == 'S') saveFrame(timestamp()+"_##.png");
  
  if (key == 'r' || key == 'R'){  
    background(360);
    beginRecord(PDF, timestamp()+".pdf");
  }
  if (key == 'e' || key == 'E'){  
    endRecord();
  }

  if (key == 'q' || key == 'S') noLoop();
  if (key == 'w' || key == 'W') loop();
  
  if (keyCode == UP) pointCount = min(pointCount+1, 30);
  if (keyCode == DOWN) pointCount = max(pointCount-1, 1); 
  
  if (keyCode == 'g') {
      gifExport.finish();
  println("gif exported");
  }

}

// timestamp
String timestamp() {
  Calendar now = Calendar.getInstance();
  return String.format("%1$ty%1$tm%1$td_%1$tH%1$tM%1$tS", now);
}
