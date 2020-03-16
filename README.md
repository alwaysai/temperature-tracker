# Temperature Tracker App
This app demonstrates how to use a temperature tracking utility class for the Raspberry Pi. 

## Requirements
To run this app, you will need an alwaysAI account. Please register at https://alwaysai.co/auth?register=true

## Setup
Easy start up guides can be found following registration. Please see the docs page for more information: https://alwaysai.co/docs/getting_started/introduction.html

### Models
The default detection model for the realtime_object_detector start app is used (alwaysai/mobilenet_ssd), and more details can be found at https://alwaysai.co/model-catalog?model=alwaysai/agenet


You can alter the code to used different detection and classification models: https://alwaysai.co/docs/application_development/changing_the_model.html


## Troubleshooting
If you are having trouble connecting to your edge device, use the CLI configure command to reset the device. Please see the following page for more details: https://alwaysai.co/docs/reference/cli_commands.html

You can also post questions and comments on our Discord Community at: https://discord.gg/R2uM36U


## Usage
A table of utility functions and their usage is provided below. 

| Function |Arguments | Return Value| Usage |
| minimum | () | (float, time) | Finds and returns the minimum temperature gathered so far as well as the corresponding time stamp, using the instance list. |
| minimum_from | [(float, time)] | (float, time) | Finds and returns the minimum temperature gathered so far as well as the corresponding time stamp, using the input list. |
| maximum | () | (float, time) | Finds and returns the maximum temperature gathered so far as well as the corresponding time stamp, using the instance list. |
| maximum_from | [(float, time)] | (float, time) | Finds and returns the maximum temperature gathered so far as well as the corresponding time stamp, using the input list. |
| update | () |  | Determines the current internal temperature of the Raspberry Pi and updates the internal temperature tracking instance list with the latest reading. | 
| update_from | (float, time), [(float, time)] |  | Updates the input list with the new reading and sets this new list as the temperature trackers current instance list. Used to reset the temperature tracker if input list is empty. |
| now | () |   | Determines the current reading and returns a tuple with the reading and the time struct object with the corresponding timestamp. |
| average | () | float | Calculates and returns the average of all temperature readings gathered so far, using the instance list. | 
| average_from | [(float, time)] | float | Calculates and returns the average of all temperature readings gathered so far, using the input list. | 
| count | () | int | Calculates and returns the number of readings taken so far, using the instance list. |
| count_from | [(float, time)] | int | Calculates and returns the number of readings taken so far, using the input list. |
| temperatures | () | [(float, time)] | Returns the instance list of all gathered temperature and corresponding timestamp data. |
| start | () |  | Sets the start_timestamp for the instance to the time of invocation, recording the start time of the tracker. |
| stop | () |  | Sets the stop_timestamp for the instance to the time of invocation, recording the stop time of the tracker. |
| get_start | () | time | Returns the recorded start time for the instance. |
| get_stop | () |  | Returns the recorded stop time for the instance. |
| summary | () | String | Returns a string containing all of the readings and corresponding timestamps, and the minimum, the maximum, and the average temperature readings, along with start and stop data of the instance temperature list. All temperature readings are displayed in Celsius and Fahrenheit. |
| summary_from | [(float, time)] | String | Returns a string containing all of the readings and corresponding timestamps, and the minimum, the maximum, and the average temperature readings, along with start and stop data of the input temperature list. All temperature readings are displayed in Celsius and Fahrenheit. |