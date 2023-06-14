# validation for jsonline
change name of the `shape_management.py` into `json_val.py` since this is a validation module
- check `types`: 3 shapes only, can add more shapes
- check `keys`: no extra added key, and only supported key, no n/a
- check `values`: no extra value, no wrong data type (float and int only), no nagative value, no n/a

error handling not to interrupt because I want to capture all the data

```bash
python -m src.v4.area_cal_val
```

![](../../Pictures/Pasted%20image%2020230610183958.png)
