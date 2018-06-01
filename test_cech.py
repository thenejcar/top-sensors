import dionysus
from cech import cech
from vietoris import vietoris

# test ce nam cech pravilno dela

a = (0.852087358103031, 0.23155082323200207, -0.46312932131356)
b = (0.991364358103031, 0.013072923232002081, 0.019666178686440015)
c = (0.862015358103031, 0.4904558232320021, 0.019666178686440015)
r = 0.275

vr = vietoris([a,b,c], r*2)
results, results_flat = cech([a, b, c], r)

print(vr)
print()

print(results)
print(results_flat)