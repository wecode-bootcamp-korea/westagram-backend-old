#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jwt

access_token = jwt.encode({'email':5}, 'secret', algorithm='HS256')
access_token
