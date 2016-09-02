#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyV8

ctxt = PyV8.JSContext()
ctxt.enter()

def get_DigestAuthentication():
    func = ctxt.eval()
    return func
