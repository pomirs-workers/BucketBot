import RPi.GPIO as GPIO
from lib.pi_pwm.module import PWM


class Motor:

    @staticmethod
    def apply_requirements():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def __init__(self, config):
        self.__config__ = config
        self.__pwm_ch__ = PWM(self.__config__.pin_pwm)
        self.__angle__ = 0.0
        self.__speed__ = 0.0

        self.__gpio_init__()
        self.__apply__(0)

    def __gpio_init__(self):
        GPIO.setup(self.__config__['pin_a'], GPIO.OUT)
        GPIO.setup(self.__config__['pin_b'], GPIO.OUT)

    def __apply__(self, speed):
        self.__speed__ = speed
        if speed == 0:
            self.self.__pwm_ch__.set(0)
            GPIO.output(self.__config__['pin_a'], False)
            GPIO.output(self.__config__['pin_b'], False)
        elif speed > 0:
            self.self.__pwm_ch__.set(speed)
            GPIO.output(self.__config__['pin_a'], True)
            GPIO.output(self.__config__['pin_b'], False)
        else:
            self.self.__pwm_ch__.set(-1 * speed)
            GPIO.output(self.__config__['pin_a'], False)
            GPIO.output(self.__config__['pin_b'], True)

    def go(self, speed):
        if self.config['log']:
            print('[go] speed = ' + str(speed))
        self.__apply__(speed)

    def stop(self):
        if self.config['log']:
            print('[stop]')
        self.go(0)

    def reset(self):
        if self.config['log']:
            print('[reset]')
        self.__angle__ = 0

    def update(self):
        old_angle = self.__angle__
        new_angle = 0  # TODO
        self.__angle__ = new_angle
        if self.config['log']:
            print('[update] O/N/D = ' + str(old_angle) + '/' + str(new_angle) + '/' + str(new_angle - old_angle))
        return new_angle - old_angle

    def get_angle(self):
        return self.__angle__
    
    def get_speed(self):
        return self.__speed__
    
    def get_config(self):
        return self.__config__
