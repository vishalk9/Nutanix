# red-pool
The container of red-fish api module that will help in foundation.

## Installation

* Get the source code:
```
https://drt-it-github-prod-1.eng.nutanix.com/vishal-kumar/red-pool.git
```
* Install Redfish :
```
sudo pip install python-ilorest-library
```

## Running Red-pool:
* Run redpool.py
```
python redpool.py
```
This module is used to do the following operation needed for imaging:
1. Get power status
2. Power off Node
3. Change boot mode (legacy/Uefi) [optional]
4. Check virtual media status
5. Attach virtual Media (can involve enabling virtual drive, attaching iso)
6. Change boot order to boot from CD. (Note: Please Eject inserted Virtual Media (if any) using option 8 before calling it)
7. Power On Node
8. Eject virtual media

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
