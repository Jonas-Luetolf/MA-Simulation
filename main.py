from src.main import main
import time

t1 = time.time()
main(30,100,30,100,2,10, 500_000,1,"sim-500_000-1-neg-30-sensors-1.csv", sensor_angle=1, negative_probability=30)

print(time.time()-t1)
