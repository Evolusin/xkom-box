# X-KOM Box Opener
## Description

This Python project automates a series of GUI operations. Using template matching, the script identifies and interacts with elements on the screen, aiming to streamline certain repetitive tasks. The primary use case is for box opening in a X-Kom application using Bluestacks emulation.

## Dependencies
This project uses the following Python libraries:

- pyautogui
- time
- sys
  
## Setup & Usage
Clone this repository to your local machine.
Install the necessary dependencies:
```bash
pip install -r requirements.txt
```

1. Add your template images to the templates directory. The script currently looks for the following templates:

- 'box' (promocja)
- 'open'
- 'open_2'
- 'box_close'
- 'next_box'
- 'roll_{i}', where i is a number from 1 to 3
Each template image should correspond to an element on the screen that you want the script to interact with.

2. Run the script:


```bash
python main.py
```
The script will look for 'promocja' on the screen, scroll until it finds it, and then perform a series of operations on three boxes (open, roll, close). After each box, it will look for 'next_box' and continue to the next one. The script will exit if it cannot find any of the necessary elements on the screen.

## Note
Ensure that the correct images are placed in the templates directory, and that they match the screen elements exactly. Otherwise, the script may not work as expected.

## Contributing
If you wish to contribute to this project, please submit a pull request.

## License
MIT