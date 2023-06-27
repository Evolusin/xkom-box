from functions import (
    try_template_match,
    load_templates,
    click_and_hold_on_match,
    take_screenshot_of_area,
    create_folder,
)
import pyautogui
import sys
import time


def process_box(templates_box_close, templates_open_2, templates_roll, box_number):
    """
    Processes a single box by performing a series of operations.

    Parameters:
    templates_box_close (list): List of box close templates for image matching.
    templates_open_2 (list): List of open_2 templates for image matching.
    templates_roll (list): List of roll templates for image matching.
    box_number (int): The number representing the box being processed.

    Returns:
    None

    Note:
    The function will terminate the program with an error code 1 if any template is not found.
    """

    print(f"Processing box {box_number}")
    print("Looking for 'open_2' and clicking on it...")
    success, screen, match = try_template_match(
        "templates", templates_open_2, click=True, time_to_wait=1
    )
    if not success:
        print("Error: 'Open_2' not found.")
        sys.exit(1)
    print("'Open_2' has been found and clicked.")
    time.sleep(2)
    print(f"Looking for 'roll_{box_number}' and clicking and holding on it...")
    success, screen, match = try_template_match(
        "templates", templates_roll, click=False, time_to_wait=1
    )
    if not success:
        print(f"Error: 'Roll_{box_number}' not found.")
        sys.exit(1)
    print(f"'Roll_{box_number}' has been found.")
    click_and_hold_on_match(match)
    time.sleep(3)

    print("Looking for 'box_close' and taking screenshot...")
    success, screen, match = try_template_match(
        "templates", templates_box_close, click=False, time_to_wait=1
    )
    if not success:
        print("Error: 'Box_close' not found.")
        sys.exit(1)
    print("'Box_close' has been found.")

    screenshot = take_screenshot_of_area(
        match, "box_close.png", width=485, height=290, offset_x=30, offset_y=80
    )
    screenshot.save(f"out/box_{box_number}.png")


def main():
    """
    Main function to control the flow of the program.

    Parameters:
    None

    Returns:
    None

    Note:
    The function initializes the templates, attempts to find 'promocja' and 'open' on the screen, 
    and processes three boxes. The program is terminated with an error code 1 if 'promocja' or 'open' 
    cannot be found, or if 'next_box' cannot be found before the third box has been processed.
    """
    
    time.sleep(2)
    create_folder("out")

    print("Loading templates...")

    templates_promocja = load_templates("templates", "box")
    templates_open = load_templates("templates", "open")
    templates_open_2 = load_templates("templates", "open_2")
    templates_box_close = load_templates("templates", "box_close")
    templates_next_box = load_templates("templates", "next_box")
    templates_roll = [load_templates("templates", f"roll_{i}") for i in range(1, 4)]

    print("Looking for 'promocja'...")
    for _ in range(10):
        pyautogui.scroll(-5)  # Scroll down
        success, screen, match = try_template_match(
            "templates", templates_promocja, click=True, time_to_wait=1
        )
        if success:
            print("'Promocja' has been found and clicked.")
            break
        print("Promocja not found. Trying again...")
    else:
        print("Error: 'Promocja' not found.")
        sys.exit(1)

    print("Looking for 'open'...")
    time.sleep(2)  # Wait for a second
    success, screen, match = try_template_match(
        "templates", templates_open, click=True, time_to_wait=1
    )
    if not success:
        print("Error: 'Open' not found.")
        sys.exit(1)
    print("'Open' has been found.")

    for i in range(3):
        process_box(templates_box_close, templates_open_2, templates_roll[i], i + 1)
        print("Looking for 'next_box' and clicking on it...")
        success, screen, match = try_template_match(
            "templates", templates_next_box, click=True, time_to_wait=1
        )
        if not success:
            if i == 3:
                print("Done.")
                sys.exit(0)
            else:
                print("Error: 'next_box' not found.")
                sys.exit(1)
        print("'Next_box' has been found and clicked.")


if __name__ == "__main__":
    main()
