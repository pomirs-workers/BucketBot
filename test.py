from bucket_bot import BucketBot


def me(a, b):
    print('Move test:', a, b)


opts = {
    'ini_x': 0,
    'ini_y': 0,
    'wheel_rad': 10
}


test = BucketBot(opts)
test.bind(me)

test.go('left', 10)
test.stop()