#include <Keyboard.h>
#include <MouseTo.h>
#include <Mouse.h>

void setup()
{
  Serial.begin(115200);
  Serial.setTimeout(1);
  Keyboard.begin();
  Mouse.begin();
  MouseTo.setCorrectionFactor(1);
}

void loop()
{
  while (!Serial.available());
  String command = Serial.readStringUntil('\n');
  if (command.substring(0, 1) == "u")
  { // key press
    Keyboard.press(command[1]);
    return;
  }
  if (command.substring(0, 1) == "y")
  { // key release
    Keyboard.release(command[1]);
    return;
  }
  if (command.substring(0, 1) == "k")
  { // key click
    Keyboard.print(command.substring(1));
    return;
  }
  if (command.substring(0, 1) == "r")
  { // mouse reset
    MouseTo.home();
    while (MouseTo.move() == false);
    Serial.print("HOMED ");
    Serial.print(MouseTo.getScreenResolutionX());
    Serial.print("/");
    Serial.print(MouseTo.getScreenResolutionY());
    Serial.print("\n");
  }
  if (command.substring(0, 1) == "m")
  { // mouse move
    MouseTo.setTarget(command.substring(1, 5).toInt(), command.substring(5, 9).toInt(), false);
    while (MouseTo.move() == false);
    Serial.print("MOVED\n");
    return;
  }
  if (command.substring(0, 1) == "p")
  { // mouse press
    Mouse.press();
    return;
  }
  if (command.substring(0, 1) == "b")
  { // mouse right click
    Mouse.click(MOUSE_RIGHT);
    return;
  }
  if (command.substring(0, 1) == "h")
  { // mouse release
    Mouse.release();
    return;
  }
}
