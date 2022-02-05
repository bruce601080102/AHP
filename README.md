# AHP
*  輸入X為負代表 = 1/X
*  輸入X為正代表 = X
*  輸入為一個Dict型態

<img src="images/scale.jpg" alt="Logo" width="600" height="100">

<br/>
<br/>

```python
ahp_weight = {
    "test1": 1.6,
    "test2": 2.7,
    "test3": 1,
    "test4": 4,
    "test5": 4,
    "test6": 4,
    "test7": 2,
    "test8": 1.2
}
ahpw = AHPWeight(ahp_weight)
dict_weight = ahpw.output_weight()
print("AHP Weight:", dict_weight)
print("AHP evaluate:", ahpw.ahp_evaluate())
```

