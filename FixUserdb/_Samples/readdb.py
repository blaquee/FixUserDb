import os
import ConfigParser
import codecs
import numpy


CODE = """
USE32
global _mainexe
extern _mainCRTStartup

section .text
_mainexe:
db %s
call _mainCRTStartup
ret
"""
cfg = ConfigParser.ConfigParser()

cfg.readfp(codecs.open("userdb-new.txt", "r", "utf8"))
print len(cfg.sections())
eps = list()
packers = dict()
sections = cfg.sections()

for section in sections:
    options = cfg.options(section)
    for option in options:
        if "ep_only" in option:
            if cfg.getboolean(section, option):
                # print "Ep Only"
                for option in options:
                    if "signature" in option:
                        # print "found"
                        bytes = cfg.get(section, option)
                        bytes = bytes.replace(u" ", u"")

                        if u'??' in bytes:
                            continue
                        # print "{}-{}".format(len(bytes), len(bytes) % 2)
                        bytes = ["0" + str(bytes[b:b+2]) + "h" for b in range(0, len(bytes), 2)]
                        eps.append(bytes)
                        packers[section] = bytes

for sig in eps:
    asm_code = CODE % ",".join(sig)
    with codecs.open("packer_"+ str(numpy.random.randint(1, 1000)) + ".asm", "w") as w:
        w.write(asm_code)



print "num no wildcard elements {}".format(len(eps))
'''
for i, ep in enumerate(eps):
    ep_s = ep.strip(' ')
    for c in ep_s:
        if '?' in c:
for i,ep in enumerate(eps):
    if i < 20:
        print "{}:{}".format(type(ep), ep)
'''
