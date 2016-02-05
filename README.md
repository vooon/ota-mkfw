ota-mkfw: fimrware image packer
===============================

Simple proof-of-concept firmware image packer.
It works similar to [`px_mkfw.py`][1] from PX4 firmware,
except it uses [RFC-7049 (CBOR)][2] instead of JSON.
Thanks to binay format we may omit base64 encoding, and gzip is optional.


File format
-----------

For CBOR there exists own CDDL, but JSON-like is easier to understood:

```json
// File (header)
{
	"magic": "OTAFWv1",
	"description": "",
	"build_date": Tag(0, "<RFC3339 time>"),
	"version": "0.1.0",
	"revision": "<git hash>",
	"git-identity": "<optional git describe>",
	"board": "<some id>",
	"data": {
		"firmware.bin": Image{}, // required
		"parameters.xml": Image{}, // optional
		...
	}
}

// Image
{
	"size": 123,				// to verify payload
	"sha1sum": "<byte string (20 bytes)>",	// optional
	"payload": "<non compressed byte string>"
	// Alternative: Tag(22, "<byte stirng>") -> text exporter will use base64 (like in PX4 JSON)
	// Gzipped: Tag(12222, "<defalted byte string>") -> tag mark that inflating is required, base64 for exporter
}
```


[1]: https://github.com/PX4/Firmware/blob/master/Tools/px_mkfw.py
[2]: https://tools.ietf.org/html/rfc7049
