#!/bin/bash

#coverage erase
coverage run -a --branch main.py 
coverage report -m
