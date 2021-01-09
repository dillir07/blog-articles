# highres
A python package to download high resolution image using Google Search by Image feature

## Prerequisites:
Instructions are below
- Python with pip selenium package
- A browser with Webdriver

### Install selenium via pip

```bash
pip install selenium
```

### Webdriver Setup
Click and download the driver from their official websites.
- [Chrome](https://chromedriver.chromium.org/downloads)
- [Firefox](https://github.com/mozilla/geckodriver/releases)
- [Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

### Add webdriver folder path to System path
Add downloaded driver folder path to System path.

## Todo
Now, before we start coding, lets break down our goal into smaller components.

Set up Code for:
- Input & Output folders
- Identify image files in a folder.
- Detect browser and launch
- Navigate and use Google's 'Search by Image'
- Download image based on it's URL and save in a folder
- Create a pip package

### Code for Input & Output folders
Nomally we can simply use string variable to store paths, but using `Path` from `pathlib` is OS neutral and has many useful features. Like for combining paths, we can simply use `/` instead `+ "//" +` like we do with strings.

so, lets import that one.

```python
import os
from pathlib import Path
# this is come as command line input for completed code.
images_folder_path = Path(r'/home/dr/Pictures/low-res')
highres_folder_name = Path(r'highres')
success_folder_name = Path(r'old')
error_folder_name = Path(r'error')

if not os.path.exists(images_folder_path / highres_folder_name):
    os.mkdir(images_folder_path / highres_folder_name)
if not os.path.exists(images_folder_path / success_folder_name):
    os.mkdir(images_folder_path / success_folder_name)
if not os.path.exists(images_folder_path / error_folder_name):
    os.mkdir(images_folder_path / error_folder_name)

image_extensions = [".jpeg", ".jpg", ".png", ".bmp"]

if not os.path.exists(images_folder_path):
    raise SystemExit("{} is a invalid folder".format(images_folder_path))
```

### Identify image files in a folder.

As I mentioned before `Path` from `pathlib` has lot of features,
one of them is getting the file extention easily.
like

```python
Path('/home/dr/Pictures/image.jpeg').suffix # returns ".jpeg"
```

```python
# lets get all the images in the folder
files = os.listdir(images_folder_path)

# lets filter all the files having this extensions,
# using list comprehension here
image_extensions = [".jpeg", ".jpg", ".png", ".bmp"]

files = [file for file in files if Path(file).suffix.lower() in image_extensions]
if len(files) == 0:
    raise SystemExit("No images found in the input folder")
```

### Detect Browser and define code

Normally, we can launch a webpage simpy with following three lines...

```python
from selenium import webdriver
browser = webdriver.Firefox()
browser.get("https://dev.to")
```

But we want to support most popular browsers. So, will try to launch with a browser, if we get an error, we will try to check next browser.

```python
browser = None
url = r"https://google.com/images"

if browser is None:
    try:
        browser = webdriver.Chrome()
        browser.get(google_images_url)
    except (Exception) as err:
        print(err)
if browser is None:
    try:
        browser = webdriver.Firefox()
        browser.get(google_images_url)
    except (Exception) as err:
        print(err)
if browser is None:
    try:
        browser = webdriver.Safari()
        browser.get(google_images_url)
    except (Exception) as err:
        print(err)
if browser is None:
    try:
        browser = webdriver.Edge()
        browser.get(google_images_url)
    except (Exception) as err:
        print(err)
if browser is None:
    raise SystemExit(
        "Browser is not available or Webdriver is not set up properly")
```

## Navigation in Google Image Search

Now, for this, we will be waiting for few elements to load completely, before we click on that.
For this reason, we will define a re-usable method, which we will reuse later.

```python
def wait_for_element(driver, byType, byValue, maxWait: int):
    """
    This method, takes properties of an element and looks for the element in page.
    if the element is found, it will return the element else None is returned

    Args:
        driver ([webdriver]): [Selenium webdriver]
        byType ([By Type]): [Which property we are using to get element. ex: By.XPATH or BY.Id]
        byValue ([type]): [value of property]
        maxWait (int): [wait for element to be found]

    Returns:
        [webdriverelement]: [identified element]
    """
    try:
        element = WebDriverWait(driver, maxWait).until(
            EC.presence_of_element_located((byType, byValue)))
        return element
    except TimeoutException:
        print("Element not found")
        return None
```

Now the actual code for navigation, we are just getting the element and clicking the element, one by one.

```python
dr.get(url)
print("working on file:", file)
file_name = Path(file)
image_icon = wait_for_element(dr,
                              By.XPATH, "/html/body/div[2]/div[2]/div[2]/form/div[2]/div[1]/div[1]/div/div[3]/div[2", 10)
image_icon.click()
upload_image_link = wait_for_element(dr,
                                     By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/form/div[1]/div/a", 10)
upload_image_link.click()
browse_image_button = wait_for_element(dr,
                                       By.XPATH, '//*[@id="awyMjb"]', 10)
browse_image_button.send_keys(str(images_folder_path) + "/" + file)
try:
    all_sizes_button = wait_for_element(dr,
                                            By.XPATH, '/html/body/div[7]/div[2]/div[10]/div[1]/div[2]/div/div[2]/div[1]div/div[1]/div[2]/div[2]/span[1]/a', 10)
    all_sizes_button.click()
    first_image = wait_for_element(dr,
                                       By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[1]/div[1]/di[1]/a[1]/div[1]/img', 10)
    first_image.click()
    time.sleep(wait_time)
    preview_image_link = wait_for_element(dr,
                                              By.XPATH, '/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/di[2]/c-wiz/div[1]/div[1]/div/div[2]/a/img', 10)
    src = preview_image_link.get_attribute('src')
```

## Save image file

```python
import urllib.request

urllib.request.urlretrieve(
    src, images_folder_path / highres_folder_name / file_name)
# os.renames is used to move the file, which will automatically create folders if not exits already.
os.renames(images_folder_path / file_name,
           images_folder_path / success_folder_name / file_name)
print("success for file:", file)
```

## creating a pip package
for this we want our script to execute from command line, so we will put above codes in appropriate functions and create a `handler` method, then put them in a module and create a command-line entry point as follows.

Note: for simplicity, the function definition and argparse code is not included here, completed code at Github is linked at the end.

```python
# command_line.py
from highresmodule import highres

def main():
    highres.highres_handler()
```

Finaly the most important pip setup code, we will use built-in setuptools to create a pip package, as follows.

```python
# setup.py
import os
import setuptools


def read(fname):
    # for reading the description
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setuptools.setup(
    name='highres',
    version='1.0.3',
    author="Dilli Babu R",
    author_email="dillir07@outlook.com",
    description='A script to download hi-resolution images using google search by image feature',
    long_description=read('pip-readme.rst'),
    long_description_contect_type="text/markdown",
    url="https://dillir07.github.io/highres/",
    packages=['highresmodule'],
    install_requires=['selenium'], #specifying dependency
    entry_points={
        "console_scripts": ['highres=highresmodule.command_line:main']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
```

now, finally we can have the package created and installed locally with the following command.

```bash
python setup.py develop
```

Once we are okay, we can upload to pypi registry by following instructions at [pip package creation](https://packaging.python.org/tutorials/packaging-projects)

The final code is available at [Github](https://github.com/dillir07/highres) and demo at [highres](https://dillir07.github.io/highres/)

As usaul comments are welcome, thanks for reading :)