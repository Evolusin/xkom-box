import mss
import numpy as np
import time
import cv2 as cv
import pyautogui
import os


def get_screenshot(monitor):
    with mss.mss() as sct:
        # Get raw pixels from the screen, save it to a Numpy array
        img = np.array(sct.grab(monitor))
        return img


def cut_image(image, x, y, x1, y1):
    return np.array(image[y:y1, x:x1])


def define_monitor():
    monitor = {"top": 0, "left": 0, "width": 1800, "height": 1040}
    return monitor


def get_and_cut_screenshot(x, y, x1, y1):
    monitor = define_monitor()
    # get screenshot from monitor
    screen = get_screenshot(monitor)
    # create new screenshot from point (x, y) to (x1, y1)
    screenshot = cut_image(screen, x, y, x1, y1)

    return screen, screenshot


def check_if_is_match(match):
    for _, rects in match.items():
        if len(rects) > 0:
            return True
        else:
            return False


def find_templates_on_screenshot(screen, path_for_templates, templates, threshold=0.7):
    img = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)
    matches = {}
    for x in templates:
        template = cv.imread(
            f"{path_for_templates}/{x}",
            cv.IMREAD_GRAYSCALE,
        )
        # print template name and path
        print(f"Searching for {path_for_templates}/{x}...")
        res = cv.matchTemplate(img, template, cv.TM_CCOEFF_NORMED)

        loc = np.where(res >= threshold)

        # For each match we draw a rectangle around it on our screenshot
        rects = []
        for pt in zip(*loc[::-1]):
            rects.append((pt[0], pt[1], template.shape[1], template.shape[0]))

        rects, _ = cv.groupRectangles(rects, 1, 0.2)
        matches[x] = rects

    return matches


def click_on_match(match, x_offset=0, y_offset=0):
    for _, rects in match.items():
        for x, y, w, h in rects:
            x = x + x_offset
            y = y + y_offset
            x1 = x + w
            y1 = y + h
            x_center = int((x + x1) / 2)
            y_center = int((y + y1) / 2)
            print(f"Clicking on {x_center}, {y_center}")
            pyautogui.moveTo(x_center, y_center)
            time.sleep(1)
            pyautogui.click(x_center, y_center, button="left")
            time.sleep(2)


def try_template_match(
    path_for_template, template, click=False, max_attempts=1, time_to_wait=0
):
    """
    Try to find a template match on the screen.

    Args:
        path_for_template (str): The folder path for the template.
        template (str): The filename of the template.
        click (bool, optional): Whether to click on the template match. Default is False.
        max_attempts (int, optional): The maximum number of attempts to find the template. Default is 3.
        time_to_wait (int, optional): The time in seconds to wait before searching for the template. Default is 0.

    Returns:
        A tuple containing a boolean indicating whether a match was found, the screenshot image, and the match coordinates.
    """
    success = False
    # print(f"Waiting {time_to_wait} seconds before trying to match {template}")
    time.sleep(time_to_wait)
    for attempt in range(max_attempts):
        screen, screenshot = get_and_cut_screenshot(0, 0, 1920, 1080)

        match = find_templates_on_screenshot(screenshot, path_for_template, template)
        if check_if_is_match(match):
            if click:
                click_on_match(match)
            success = True
            break
        else:
            print(f"No match found for {template}")
            time.sleep(1)

    if success:
        print(f"Successfully matched {template}")
    else:
        print(f"Failed to match - {path_for_template} - {template}")

    return success, screen, match


def load_templates(path_for_templates, template=None):
    """
    Load image templates from a folder and return a list of names.

    Args:
        path (str): Path to the folder containing the templates.
        template (str, optional): Name of a specific template to return.

    Returns:
        List of template names as strings.
    """
    templates = os.listdir(f"{path_for_templates}")
    if template is not None:
        # add .png to template name
        # name = template.split(".")[0]
        name = f"{template}.png"
        return [name]
    return templates


def press_key(switch):
    if switch == "W":
        print("Pressing W")
        pyautogui.keyDown("w")
        time.sleep(1)
        pyautogui.keyUp("w")
        return "S"
    else:
        print("Pressing S")
        pyautogui.keyDown("s")
        time.sleep(1)
        pyautogui.keyUp("s")
        return "W"


def click_and_hold_on_match(match, x_offset=0, y_offset=0, hold_duration=2):
    for _, rects in match.items():
        for x, y, w, h in rects:
            x = x + x_offset
            y = y + y_offset
            x1 = x + w
            y1 = y + h
            x_center = int((x + x1) / 2)
            y_center = int((y + y1) / 2)
            print(f"Clicking and holding on {x_center}, {y_center}")
            pyautogui.moveTo(x_center, y_center)
            time.sleep(1)
            pyautogui.mouseDown(button="left")
            time.sleep(hold_duration)
            pyautogui.mouseUp(button="left")
            time.sleep(2)


def take_screenshot_of_area(match, template_name, width, height, offset_x, offset_y):
    """Take a screenshot of a specific area.

    The area is determined by the position of the match, the width and height of the area,
    and the offsets in the x and y direction from the match position.
    """
    match_info = match[template_name][0]  # This is the array [[x, y, w, h]]
    x, y, _, _ = match_info  # We only need the x and y coordinates
    return pyautogui.screenshot(region=(x + offset_x, y + offset_y, width, height))


def create_folder(name):
    # try creating folder named 'out' if it doesn't exist
    try:
        os.mkdir(name)
    except FileExistsError:
        pass
