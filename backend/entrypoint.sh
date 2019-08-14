#!/usr/bin/env bash
flask db upgrade
gunicorn --reload -b "0.0.0.0:80" -t 600 arthas_networth:app

