import RPi.GPIO as GPIO
from lib.pi_pwm.module import PWM


class Motor:

    @staticmethod
    def apply_requirements():
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

    def __init__(self, config):
        self.pin_a = config['pin_a']
        self.pin_b = config['pin_b']
        self.pin_pwm = config['pin_pwm']
        self.pin_enc_a = config['pin_enc_a']
        self.pin_enc_b = config['pin_enc_b']
        self.log = config['log']
        self.pwm_channel = PWM(self.pin_pwm)
        self.angle = 0.0
        GPIO.setup(self.pin_a, GPIO.OUT)
        GPIO.setup(self.pin_b, GPIO.OUT)
        self.__apply__(0)

    def __apply__(self, speed):
        if speed == 0:
            self.pwm_channel.set(0)
            GPIO.output(self.pin_a, False)
            GPIO.output(self.pin_b, False)
        elif speed > 0:
            self.pwm_channel.set(speed)
            GPIO.output(self.pin_a, True)
            GPIO.output(self.pin_b, False)
        else:
            self.pwm_channel.set(-1 * speed)
            GPIO.output(self.pin_a, False)
            GPIO.output(self.pin_b, True)

    def go(self, speed):
        if self.log:
            print('[go] speed = ' + str(speed))
        self.__apply__(speed)

    def stop(self):
        if self.log:
            print('[stop]')
        self.go(0)

    def reset(self):
        if self.log:
            print('[reset]')
        self.angle = 0

    def update(self):
        old_angle = self.angle
        new_angle = 0  # TODO
        self.angle = new_angle
        if self.log:
            print('[update] O/N/D = ' + str(old_angle) + '/' + str(new_angle) + '/' + str(new_angle - old_angle))
        return new_angle - old_angle

    def get_angle(self):
        return self.angle
