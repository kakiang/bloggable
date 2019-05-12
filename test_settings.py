from selenium import webdriver

SELENIUM_WEBDRIVERS = {
    'default' :{
        'callable': webdriver.Chrome,
        'args':(),
        'kwargs':{},
    },
    'firefox':{
        'callable':webdriver.Firefox,
        'args':(),
        'kwargs':{},
    },
}