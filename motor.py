import RPi.GPIO as GPIO
from lib.pi_pwm.module import PWM

class Motor:
    @staticmethod
    def apply_requirements():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(22, GPIO.OUT)

    @staticmethod
    def lock_all():
        GPIO.output(22, False)

    @staticmethod
    def unlock_all():
        GPIO.output(22, True)

    def __init__(self, config):
        self.__config__ = config
        self.__pwm_ch__ = PWM(self.__config__['pin_pwm'])
        self.__angle__ = 0.0
        self.__speed__ = 0.0

        self.__gpio_init__()
        self.__apply__(0)

        self.__prev_code__ = 0

    def __gpio_init__(self):
        GPIO.setup(self.__config__['m_a'], GPIO.OUT)
        GPIO.setup(self.__config__['m_b'], GPIO.OUT)
        GPIO.setup(self.__config__['en_a'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.__config__['en_b'], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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

    def __graydecode__(self, _gray):
        bin = 0
        gray = _gray
        while gray > 0:
            bin ^= gray
            gray >>= 1
        return bin

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
        en_a = GPIO.input(self.__config__['en_a'])
        en_b = GPIO.input(self.__config__['en_b'])
        code = self.__graydecode__(en_a | (en_b << 1))
        if code == 0:
            if self.__prev_code__ == 3:
                self.__angle__ += self.__config__['deg_per_tick']
            if self.__prev_code__ == 1:
                self.__angle__ -= self.__config__['deg_per_tick']
        self.__prev_code__ = code
        if self.__config__['log']:
            print('[update] angle = ' + str(self.__angle__))

    def get_angle(self):
        return self.__angle__
    
    def get_speed(self):
        return self.__speed__
    
    def get_config(self):
        return self.__config__
