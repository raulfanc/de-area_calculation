# Best practice to run tests
- make sure each folder contains a `__init__.py` file, it could be empty, Python uses them to recognize directories as containing packages.
- run test from the main directory
```bash
python -m unittest discover tests
```

![](../../Pictures/Pasted%20image%2020230610021816.png)