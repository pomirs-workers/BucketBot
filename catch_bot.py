class CatchBot:

    # Static method 'test': None - Stuff for testing
    # -- no arguments --
    @staticmethod
    def test():
        print('OK!')

    # Constructor: <CatchBot instance>
    # -- arguments --
    # config: Dict - initialization options
    def __init__(self, config):
        self.__C = config
        (self.__rw_angle, self.__lw_angle) = (0, 0)
        (self.__pos_x, self.__pos_y) = (0, 0)
        (self.__rw_spd, self.__lw_spd) = (0, 0)
        self.__driver = None

    # Method 'bind': None - binds low-level motors-control callback to class instance
    # -- arguments --
    # driver: Function - callback, which is called to start movement
    def bind(self, driver):
        self.__driver = driver

    # Method 'go': None - sets the speed for a <applyFor> wheel(-s)
    # -- arguments --
    # applyTo: String (left|right|both: default) - movement for which wheel
    # speed: Float [-1;1] - bi-direction movement speed
    def go(self, apply_to='both', speed=0):
        if apply_to == 'left' or apply_to == 'both':
            self.__lw_spd = speed
        if apply_to == 'right' or apply_to == 'both':
            self.__rw_spd = speed

        # low level control method call
        self.__driver(apply_to, speed)

    # Method 'feedback': None - sets motors feedback values
    # -- arguments --
    # angles: Tuple<Integer, Integer> - tuple of total angles of motors. Left, then right
    def feedback_angles(self, angles):
        # tuple destructuring
        (new_lw_angle, new_rw_angle) = (angles[0], angles[1])

        delta_lw_angle = new_lw_angle - self.__lw_angle
        delta_rw_angle = new_rw_angle - self.__rw_angle
        # TODO count current position

    # Method 'stop': None - sets the 0 speed for a <applyFor> wheel(-s)
    # -- arguments --
    # applyTo: String (left|right|both: default) - stop for which wheel
    def stop(self, apply_to='both'):
        self.go(apply_to, 0)

    # Method 'get_position': Tuple<Integer, Integer> - returns current position
    # -- no arguments --
    def get_position(self):
        return self.__pos_x, self.__pos_y

