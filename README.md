ota-mkfw: fimrware image packer
===============================

Simple proof-of-concept firmware image packer.
It works similar to [`px_mkfw.py`][1] from PX4 firmware,
except it uses [RFC-7049 (CBOR)][2] instead of JSON.
Thanks to binay format we may omit base64 encoding, and gzip is optional.

[1]: https://github.com/PX4/Firmware/blob/master/Tools/px_mkfw.py
[2]: https://tools.ietf.org/html/rfc7049
