
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import datetime
import time
from datetime import timedelta

import os
import json

import asyncio
import pandas as pd
import csv


import mysql.connector
from mysql.connector import Error

from dotenv import load_dotenv


import re
import unicodedata