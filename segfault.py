#!/usr/bin/env python
"""Script failing with segmentation fault"""

compile("()" * 2 ** 17, "", "exec")
