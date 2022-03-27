from plane_sprites import *


class PlaneGame(object):
    """飞机大战主游戏"""

    # 初始化方法
    def __init__(self):
        print("游戏初始化")

        # 1.创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)

        # 2.创建游戏的时钟
        self.clock = pygame.time.Clock()

        # 3.调用私有方法，创建精灵与精灵组
        self.__create_sprites()

        # 4.设置定时器事件 - 创建敌机 1000ms - 发射子弹 500ms
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 500)

    # 游戏开始方法
    def start_game(self):
        print("游戏开始。。。 ")

        # 游戏循环 ->意味着游戏正式开始
        while True:
            # 1.设置刷新率
            self.clock.tick(FRAME_PER_SEC)
            # 2.事件监听
            self.__even_handler()
            # 3.碰撞检测
            self.__check_collide()
            # 4.更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()

    # 私有方法,创建精灵与精灵组
    def __create_sprites(self):

        # 创建背景精灵
        bg1 = Background()
        bg2 = Background(True)

        # 创建精灵组
        self.back_group = pygame.sprite.Group(bg1, bg2)

        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    # 私有方法,事件监听
    def __even_handler(self):
        # 使用监听方法，捕获用户动作事件并且遍历事件内容
        for event in pygame.event.get():

            # 判断事件类型是否是退出事件
            if event.type == pygame.QUIT:
                print("退出游戏。。。")

                # 调用退出游戏的静态方法结束游戏
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场。。。。")
                # 创建敌机精灵组
                enemy = Enemy()

                # 将敌机精灵添加到敌机精灵组中
                self.enemy_group.add(enemy)

            elif event.type == HERO_FIRE_EVENT:
                # 英雄发射子弹
                self.hero.fire()

        # 使用提供的获取键盘按键方法获取键盘按键 - 返回值为一个元组
        keys_pressde = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值，相同返回“1”
        # 按键为右方向键向右移动
        if keys_pressde[pygame.K_RIGHT]:
            self.hero.speed = 3
        # 按键为左方向键向左移动
        elif keys_pressde[pygame.K_LEFT]:
            self.hero.speed = -3
        # 其他按键不移动
        else:
            self.hero.speed = 0

    # 私有方法,碰撞检测
    def __check_collide(self):
        # 1.子弹精灵摧毁敌机精灵
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        # 2.敌机精灵摧毁飞机, 该方法返回一个列表。
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 3. 判断列表是否有内容
        if len(enemies) > 0:
            # 让英雄牺牲
            self.hero.kill()

            # 结束游戏
            PlaneGame.__game_over()

    # 私有方法,更新/绘制精灵组
    def __update_sprites(self):

        # 更新背景精灵组并且绘制到屏幕上
        self.back_group.update()
        self.back_group.draw(self.screen)

        # 更新敌机精灵组并且绘制到屏幕上
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        # 更新英雄精灵组并且绘制到屏幕上
        self.hero_group.update()
        self.hero_group.draw(self.screen)

        # 更新子弹精灵组并且绘制到屏幕上
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    # 私有方法,没有使用对象属性与类属性，所以用静态方法,结束游戏
    @staticmethod
    def __game_over():
        print("游戏结束")

        # 调用quit方法卸载所有模块
        pygame.quit()

        # 使用exit()直接终止当前正在执行的程序
        exit()


if __name__ == '__main__':
    game = PlaneGame()
    game.start_game()
