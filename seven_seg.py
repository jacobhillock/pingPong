def seven_seg(number, x: int, y: int, scale: float) -> list:
    segments = [
       #(x, y, horiz, vert),
        (x + 2*scale, y, 10*scale, 2*scale),                # 0 top hoiz
        (x + 2*scale, y + 12*scale, 10*scale, 2*scale),     # 1 mid hoiz
        (x + 2*scale, y + 12*scale, 10*scale, 2*scale),     # 2 bot hoiz
        (x, y + 2*scale, 2*scale, 10*scale),                # 3 top left
        (x + 12*scale + 2*scale, y, 2*scale, 10*scale),     # 4 top right
        (x, y + 14*scale, 2*scale, 10*scale),               # 5 bot left
        (x + 12*scale, y + 14*scale, 2*scale, 10*scale)     # 6 bot right
    ]

    retList = []
    nums = []

    if number == "0":
        nums = [0,2,3,4,5,6]
    elif number == "1":
        nums = [4,6]
    elif number == "2":
        nums = [0,1,2,4,5]
    elif number == "3":
        nums = [0,1,2,4,6]
    elif number == "4":
        nums = [1,3,4,6]
    elif number == "5":
        nums = [0,1,2,3,6]
    elif number == "6":
        nums = [0,1,2,3,5,6]
    elif number == "7":
        nums = [0,4,6]
    elif number == "8":
        nums = [0,1,2,3,4,5,6]
    elif number == "9":
        nums = [0,1,3,4,6]
    
    for i in nums:
        retList.append(segments[i])
    
    return retList

print(seven_seg("4",0,0,1))
