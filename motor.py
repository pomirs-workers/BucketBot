import RPi.GPIO as GPIO
from lib.pi_pwm.module import PWM
import time

UPD_FREQ = 0.005  # in seconds


class Motor:
    @staticmethod
    def apply_requirements():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def __init__(self, config):
        self.__config__ = config
        self.__pwm_ch__ = PWM(self.__config__['pin_pwm'])
        self.__angle__ = 0.0
        self.__speed__ = 0.0

        self.__gpio_init__()
        self.__apply__(0)

        self.__angle_t__ = 0
        self.__l_en_a__ = 0

    def __gpio_init__(self):
        GPIO.setup(self.__config__['m_a'], GPIO.OUT)
        GPIO.setup(self.__config__['m_b'], GPIO.OUT)
        GPIO.setup(self.__config__['en_a'], GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__config__['en_b'], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def __apply__(self, speed):
        self.__speed__ = speed
        if speed == 0:
            self.__pwm_ch__.set(0)
            GPIO.output(self.__config__['m_a'], False)
            GPIO.output(self.__config__['m_b'], False)
        elif speed > 0:
            self.__pwm_ch__.set(speed)
            GPIO.output(self.__config__['m_a'], True)
            GPIO.output(self.__config__['m_b'], False)
        else:
            self.__pwm_ch__.set(-1 * speed)
            GPIO.output(self.__config__['m_a'], False)
            GPIO.output(self.__config__['m_b'], True)

    def go(self, speed):
        if self.__config__['log']:
            print('[go] speed = ' + str(speed))
        self.__apply__(speed)

    def stop(self):
        if self.__config__['log']:
            print('[stop]')
        self.__apply__(0)

    def reset(self):
        if self.__config__['log']:
            print('[reset]')
        self.__angle__ = 0

    def update(self):
        time_mow = time.time()
        if time_mow - self.__angle_t__ > UPD_FREQ:
            en_a = GPIO.input(self.__config__['en_a'])
            en_b = GPIO.input(self.__config__['en_b'])
            if not en_a and self.__l_en_a__:
                if en_b:
                    self.__angle__ += 1
                else:
                    self.__angle__ -= 1
            self.__l_en_a__ = en_a
            if self.__config__['log']:
                print('[update] angle = ' + str(self.__angle__))

    def get_angle(self):
        return self.__angle__
    
    def get_speed(self):
        return self.__speed__
    
    def get_config(self):
        return self.__config__
