python_library(
    name = "spouts-bolts-py",
    sources=globs('*.py'),
)

python_binary(
    name = "departament-expenditure-indicator",
    source='departament-expenditure-indicator.py',
    dependencies = [
        ':spouts-bolts-py',
        '3rdparty/python:heronpy',
        '3rdparty/python:six',
        '3rdparty/python:msgpack',
        '3rdparty/python:redis',
	    '3rdparty/python:kafka-python'
    ],
)
