# Simulating the image producing by KTA OVL

For testing the **imageloader** performance, we need to mimic the environment of **imageloader** working on.
This code will create the XML file together with TIF, which like KTA metrology tool do in the fab.

## The suspection here:
We suspect the metrology tool measure one lot(_2 wafers_) in 5 minutes, and wait 2 minutes for nest lot.
* **Serial wafer measure time:**
  Start from 2019/08/01 00:00:00. It is the first lot(LotID = 00001) start time. And the next lot's measurement time +7 mins.
  ```
  mimicFilesGenVirtualTime = datetime.datetime.strptime('00:00:00:000000 08/01/2019', '%H:%M:%S:%f %m/%d/%Y') + datetime.timedelta(seconds = (i-1)*7*60)
  ```
