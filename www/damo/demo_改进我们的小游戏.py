import random

secret = random.randint(1,10)
guess = input("不妨猜一下现在心里想的是哪个数字");
guess = int(guess);

i = 0
while guess != secret:
    if(i == 3):
        print("游戏次数只能玩3次")
        break
    if guess == secret:
        print("恭喜你")
    else:
        if guess < secret:
            print("小了")
        else:
            print("大了")
        guess = input("不妨猜重新猜一下");
        guess = int(guess);
    i += 1
print("游戏结束");




