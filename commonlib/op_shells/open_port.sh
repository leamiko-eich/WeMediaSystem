#!/bin/bash

ufw allow 22
ufw allow 22/tcp
ufw allow 3306
ufw allow 3306/tcp
ufw reload
