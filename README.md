# **BuretMotor** #

## **Program** ##

> Using Raspberry Pi to control the step motor that is installed on a burette, thus mixing two wines in a specific ratio.  

## **Settings** ##

- **Environment Module:** Python3, tkinter, RPi.GPIO

- **Hardware**

   - raspberry pi 3B+,
   
   - step motor: 28BYJ-48-5V,
   
   - driver: ULN2003
   
- **Routing** (BCM)

   - motor1: 
   
         IN1 -> 17 
         IN2 -> 18 
         IN3 -> 27
         IN4 -> 22      
      
   - motor2: 
   
         IN1 -> 10 
         IN2 -> 9
         IN3 -> 11
         IN4 -> 8      

## **Instruction** ##

- ### GUI_main.py ### 

   Run `GUI_main.py` to launch the wine-mixing program with GUI. 
   
   ( `GUI_function.py` and `motor_function.py` are imported in `GUI_main.py` )
    
   #### GUI ####
   
   - **Initial Windows**
      
      The initial window enables users to choose which mode to run, auto mode or custom mode? 
     
      <img height="100" src="https://user-images.githubusercontent.com/89720769/162132113-23826edc-8384-4a5c-9b29-9fefc447299b.png"> 
   
   - **Auto Mode** 
      
      If the user selects "Auto Mode", this window pops out to inform user. And the program will automatically mix two wines with the ratio that yields the highest score.
   
      <img height="100" src="https://user-images.githubusercontent.com/89720769/162134602-4e8a02b3-14eb-4e18-bf15-4cf7695d5a6f.png">
      
   - **Custom Mode**
      
      Seleting "Custom Mode" enables user to customize their flavor according to their own taste in the following instructions.
      
      1. Choose what you would like to adjust, sweetness or acidity.
    
         <img height="100" src="https://user-images.githubusercontent.com/89720769/162134943-dc7698b3-fc89-4bb2-b2b1-7d26e5c5edfe.png">
      
      2. Customize your flavor from the combo box.
      
         <center class="half">
            <img height="200" src="https://user-images.githubusercontent.com/89720769/162134968-dd1d4120-3440-4148-9878-2f5b7da665a8.png"><img width="2" src="https://user-images.githubusercontent.com/89720769/162136570-e6ee67e5-529c-4921-ac0d-bad1658d6818.png"><img height="200"  src="https://user-images.githubusercontent.com/89720769/162134985-0b83d196-6470-45ff-bff3-b91a1d27384e.png">
         </center>
     
      3. Confirm that you have chosen "Custom Mode" and the mixing process is going to begin.
   
         <img height="100" src="https://user-images.githubusercontent.com/89720769/162135000-3f7f0cd8-9761-44a2-a9c3-f1667bf77938.png">

   - **Finish Windows** 
   
      Inform the user that the process is finished and show the score of mixing.
      
      <center class="half">
         <img height="100" src="https://user-images.githubusercontent.com/89720769/162138284-f0f9e876-eb9e-4fc0-a116-a80c9be0427c.png"><img width="2" src="https://user-images.githubusercontent.com/89720769/162136570-e6ee67e5-529c-4921-ac0d-bad1658d6818.png"><img height="100"  src="https://user-images.githubusercontent.com/89720769/162138293-d0cc0749-4e2a-49e1-afc1-92c726cf2898.png">
      </center>
     
- ### motor_main.py & motor_function.py ### 

   Run `motor_main.py` to control the total volume of the fluid that passes through burette.
   
   ( `motor_function.py` is imported in `motor_main.py` )
 
   ``` python
   $ python3 motor_main.py <motor1 steps> <motor2 steps>
   ```
   
    Add some additional parameters to customize the steps of the step motor when opening and closing burette.
    
    The motor steps decide the extent the burette opens and closes.
      
         Parameters:
            <motor1 steps> is the steps needed when motor1 open or close the burette. (defualt 100)
            <motor2 steps> is the steps needed when motor2 open or close the burette. (default 100)
   
   Follow the instuction to designate which motor to run, adjust the direction of motor and assaign the duration time that the burette remains open.
   
   The duration time, which the burette remains open, influences the total volume of the fluid that passes through the burette.
   
   > TotalVolume(ml) = FlowSpeed(ml/s) x Duration(s) + VolumeWhenOpenAndClose(ml)
   
      [which motor to run] (1: motor1, 2: motor 2):
      [duration time> (unit: second): -> In our case, volume(ml) = 5.46 \* duration(s) + 3.19
      [MODE] (mode1: clockwise -> counterwise, mode2 counterwise -> clockwise ):
      
   The process will automatically begin after seeting these parameters.

- ### MotorTesting ###  
    
   These codes are used to check if our burette motor works proporly and measure the relationship between volume and the duration time that the burette stays open. 
   
   > TotalVolume(ml) = FlowSpeed(ml/s) x Duration(s) + VolumeWhenOpenAndClose(ml)
   
   - ### motor_main_test.py & motor_function_test.py ###

      Run `motor_main_test.py` to open and close burette.  
      ( `motor_function_test.py` is imported in `motor_main_test` )
     
      ``` python
      $ python3 motor_main_test.py <motor1 speed> <motor1 duration> <motor2 speed> <motor2 duration>
      ```
         
      Add some additional parameters to customize the speed and the steps of the step motor.
      
      The speed determines how fast the burette open and close.
      
      The steps decide the extent the burette opens and closes.
      
         Parameters:
            <motor1 speed> is the rotating speed of motor1. (default 10)
            <motor1 duration> is the steps that motor1 rotates. (default 100)
            <motor2 speed> is the rotating speed of motor2. (default 10)
            <motor2 duration> is the steps that motor2 rotates. (default 100)
    
      Follow the instuction to select motor and its direction.
      
         Select which motor to run (1: motor1, 2: motor 2): 
         Select which direction to run (1: clockwise, -1: counterwise): 
       
      And the motor will start to rotate after these.
      
## **Authors** ## 

- **bobo** - *Initial work* -

## **License** ##

This project is licensed under MIT License - see the [LICENSE.md](https://github.com/Atatakaze/BuretteMotor/blob/main/LICENSE) file for details.
