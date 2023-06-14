# JSONSCHEMA
validating JSON data against a particular schema. It can improve readability and also makes your validation logic more 
modular, extensible, and maintainable. This can be particularly useful as you plan to add more shape types in the future.

- easier for other developers to understand the code
- oop mind-set: separete shape management, data validation, and area calculation scripts
- stop at the first error or generate the full list of errors? depends on business use case
- full report can help address the issue, further investigation, and fix the data (upstream issue?)
- what if there is 1 million jsonl??? multiprocessing? spark?

- install `jsonschema` lib
```bash
pip install jsonschema
```

#### what I did for this development?
- separate `json_val.py` into 2 to improve modularity, only handle json valid issues
- `shape_management.py` only handles the future extensive of adding more shapes
- modified `area_cal_val.py` in case there is a `missing value`, even this is uncommon in real-world app, as it usually
get a `null` or `default value`, but data might miss or go wrong during transmission.
- terminal output more readable with `jsonschema`'s error handling.

![](../../Pictures/Pasted%20image%2020230610192810.png)