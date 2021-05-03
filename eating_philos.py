import uasyncio
from uasyncio import Lock
import random

class Philo:
    global forks
    def __init__(self, id, fork_left_id, fork_right_id):
        self.id = id
        self.fork_left = fork_left_id
        self.fork_right = fork_right_id
    
    async def eating(self):
        #handle Lock with Context Manager, the you must not release the Lock by yourself
        async with forks[self.fork_left]:
            async with forks[self.fork_right]:
                print('Philo_{} eating...'.format(self.id))
                await uasyncio.sleep(random.randint(5, 10))
        
    async def sleeping(self):
        print('Philo_{} sleeping...'.format(self.id))
        await uasyncio.sleep(random.randint(7, 15))
    
    async def philo_forever(self):
        while True:
            await self.eating()
            await self.sleeping()
    
forks = [Lock() for i in range(5)]
philos = [Philo(0,4,0), Philo(1,0,1), Philo(2,1,2), Philo(3,2,3), Philo(4,3,4)]


def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = uasyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)



async def main():
    set_global_exception()
    for philo in range(len(philos)):
        uasyncio.create_task(philos[philo].philo_forever())
    while(True):
        await uasyncio.sleep_ms(10000)

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()


